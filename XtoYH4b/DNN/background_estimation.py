#######################################################

# This script evaluates model performance by displaying variable distributions. 
# Weight calculation and application are also performed.

# command to run this scripts:
# python3 background_estimation.py

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################

import pandas as pd
import numpy as np
import uproot
import vector
import mplhep as hep
import matplotlib.pyplot as plt

def addMX(df_):

    df_ = df_.copy()

    p4 = vector.arr({
                    "pt": df_[["JetAK4_pt_1", "JetAK4_pt_2", "JetAK4_pt_3", "JetAK4_pt_4"]].to_numpy(),
                    "eta": df_[["JetAK4_eta_1", "JetAK4_eta_2", "JetAK4_eta_3", "JetAK4_eta_4"]].to_numpy(),
                    "phi": df_[["JetAK4_phi_1", "JetAK4_phi_2", "JetAK4_phi_3", "JetAK4_phi_4"]].to_numpy(),
                    "mass": df_[["JetAK4_mass_1", "JetAK4_mass_2", "JetAK4_mass_3", "JetAK4_mass_4"]].to_numpy(),
                    })

    mx = (p4[:, 0] + p4[:, 1] + p4[:, 2] + p4[:, 3]).mass
    df_.insert(len(df_.columns)-1, "MX", mx)

    return df_

def plotting(df_3T, df_2T, bins_=None, add_bins_=True, var="MX", suffix="reweight", ratio_ylim=[0, 2]):

    if add_bins_:

        if bins_ is None:
            raise ValueError("bins_ must be provided when add_bin=True")

        bins = bins_

    else:
        bins = np.linspace(df_3T[var].min(), df_3T[var].max(), 51)

    xlim = [bins[0], bins[-1]]

    hep.style.use("CMS")
    fig, (ax, rax) = plt.subplots(2, 1, gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)
    hep.cms.label("Preliminary", data=True, loc=0, ax=ax) # com= , lumi=
    ax.set_ylabel("Entries")
    rax.set_xlabel(var)

    hist_3T, _ = np.histogram(df_3T[var], bins=bins, density=True)
    hist_2T, _ = np.histogram(df_2T[var], bins=bins, density=True)
    hist_2T_weighted, _ = np.histogram(df_2T[var], weights=df_2T["Weights"], bins=bins, density=True)

    hep.histplot([hist_3T, hist_2T, hist_2T_weighted], bins=bins, ax=ax, histtype='step', label=["3T", "2T", "2T_weighted"])

    ratio_3T_2T = hist_3T / np.where(hist_2T > 0, hist_2T, 1)
    ratio_3T_2TWeighted = hist_3T / np.where(hist_2T_weighted > 0, hist_2T_weighted, 1)

    # calculating yerr_ratio (normolize)

    hist_3T_raw, _ = np.histogram(df_3T[var], bins=bins, density=False)
    hist_2T_raw, _ = np.histogram(df_2T[var], bins=bins, density=False)
    hist_2T_weighted_raw, _ = np.histogram(df_2T[var], weights=df_2T["Weights"], bins=bins, density=False)

    bin_widths = np.diff(bins)

    I = len(df_3T[var]) * bin_widths

    yerr_3T = np.sqrt(hist_3T_raw) / I
    yerr_2T = np.sqrt(hist_2T_raw) / I
    yerr_2Tweighted = np.sqrt(hist_2T_weighted_raw) / I

    s_3T_2T = np.sqrt((np.where(hist_3T != 0, yerr_3T / hist_3T, 0))**2 + 
                      (np.where(hist_2T != 0, yerr_2T / hist_2T, 0))**2)  

    s_3T_2Tweighted = np.sqrt((np.where(hist_3T != 0, yerr_3T / hist_3T, 0))**2 +
                              (np.where(hist_2T_weighted != 0, yerr_2Tweighted / hist_2T_weighted, 0))**2)

    ## s_3T_2T and s_3T_2Tweighted maybe got RuntimeWarning but it can be ignored
        
    yerr_ratio_3T_2T = ratio_3T_2T * s_3T_2T
    yerr_ratio_3T_2TWeighted = ratio_3T_2TWeighted * s_3T_2Tweighted

    hep.histplot(ratio_3T_2T, yerr=yerr_ratio_3T_2T, bins=bins, ax=rax, label="3T/2T",
                 histtype='errorbar', color='r', capsize=2)
    hep.histplot(ratio_3T_2TWeighted, yerr=yerr_ratio_3T_2TWeighted, bins=bins, ax=rax, label="3T/2T_weighted",
                 histtype='errorbar', color='b', capsize=2)

    rax.axhline(1, ls='--', color='k')
    rax.set_ylim(ratio_ylim[0], ratio_ylim[1])
    ax.set_xlabel("")
    ax.set_xlim(xlim[0], xlim[1])
    # ax.set_ylim(0, 6000)
    handles_ax, labels_ax = ax.get_legend_handles_labels()
    handles_rax, labels_rax = rax.get_legend_handles_labels()

    handles = handles_ax + handles_rax
    labels = labels_ax + labels_rax

    ax.legend(handles, labels)
    plt.savefig(f"{var}_{suffix}.png", dpi=300, bbox_inches="tight")
    plt.savefig(f"{var}_{suffix}.pdf", bbox_inches="tight")
    print("Output Saved!")
    plt.close()

if __name__ == "__main__":

    df = pd.read_csv("data_add_dnn_score.csv")

    df = addMX(df)

    dnn_score = np.array(df["DNN_Score"])

    weight_method = 2   ### used for weight method selection

    if weight_method == 1:
        ## first method to compute weight: bin weight
        print("First weight method")

        tf_file = uproot.open("transfer_factor.root")
        tf = tf_file["ratio"]
        weights = tf.values()
        bin_edges = tf.axis().edges()

        bin_indices = np.digitize(dnn_score, bins=bin_edges, right=True) - 1

        dnn_weights = weights[bin_indices]

        suff = "bin_weight"

    else:
        ## second method to compute weight: dnn_score (almost) directly weight
        print("second weight method")

        dnn_weights = dnn_score / (1 - dnn_score) # DNN(signal_score)/DNN(backgorund_score)
        bin_edges = np.linspace(0, 1, 51)

        suff = "reweight_v2"

    df["Weights"] = dnn_weights

    df_3T = df[df.iloc[:, 0] == 1]
    df_2T = df[df.iloc[:, 0] == 0]

    mx_bin_edges = np.array([100,120,140,160,180,200,225,250,275,300,330,360,400,450,500,550,600,650,700,750,800,850,900,950,1000,1100,1200,1300,1400,1500,1600,1800,2000,2250,2500,2750,3000,3500,4000,4500])

    plotting(df_3T, df_2T, add_bins_=True, bins_=bin_edges, var="DNN_Score", suffix=suff, ratio_ylim=[-2, 4])
    # plotting(df_3T, df_2T, add_bins_=True, bins_=mx_bin_edges, var="MX", suffix=suff, ratio_ylim=[0, 2])
    # plotting(df_3T, df_2T, add_bins_=False, bins_=None, var="JetAK4_pt_3", suffix=suff, ratio_ylim=[0, 2])
    # plotting(df_3T, df_2T, add_bins_=False, bins_=None, var="JetAK4_eta_3", suffix=suff, ratio_ylim=[0, 2])
    # plotting(df_3T, df_2T, add_bins_=False, bins_=None, var="JetAK4_phi_3", suffix=suff, ratio_ylim=[0, 2])
    # plotting(df_3T, df_2T, add_bins_=False, bins_=None, var="JetAK4_mass_3", suffix=suff, ratio_ylim=[0, 2])
