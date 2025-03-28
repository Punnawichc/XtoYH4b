#######################################################

# This script calculates and plots signal significance for combinations of b-tagging working points (WP) 
# using histograms from signal and background ROOT files. 
# It computes significance using two formulas: the full Poisson-based significance and the approximate S/sqrt(B), 
# The script supports both standard and optimized combinations (the "new" or "New" mode), 
# (1 = pass loose but fail medium ... 2, 3, 4 ,5) and (1 = pass loose ... 2, 3, 4 ,5) respectively.
# filters bin selections, and saves outputs as .pdf, .txt, and .csv files. 

# command to run this scripts:
# python3 Significance.py -s signal/WP_Histogram*.root -b background/combine_background.root -New [True/False]
# please check input file names before running

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################

import ROOT
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import csv


def getHist(signal_file, background_file, isNew="False"):

    sig = ROOT.TFile.Open(signal_file, "READ")
    bg = ROOT.TFile.Open(background_file, "READ")

    if isNew == "True":
        branch_name = "hist_wp_combinations_new"
    else:
        branch_name = "hist_wp_combinations"

    hist_sig = sig.Get(branch_name)
    hist_bg = bg.Get(branch_name)
    print(f"Branch: {branch_name}")

    nbins = hist_sig.GetNbinsX()

    sig_center, sig_content = [], []
    bg_center, bg_content = [], []
    sig_err, bg_err = [], []
    for i in range(1, nbins + 1):
        sig_center.append(hist_sig.GetBinCenter(i))
        sig_content.append(hist_sig.GetBinContent(i))
        sig_err.append(hist_sig.GetBinError(i) / hist_sig.GetBinContent(i) if hist_sig.GetBinContent(i) != 0 else 0)

        bg_center.append(hist_bg.GetBinCenter(i))
        bg_content.append(hist_bg.GetBinContent(i))
        bg_err.append(hist_bg.GetBinError(i) / hist_bg.GetBinContent(i) if hist_bg.GetBinContent(i) != 0 else 0)

    return [sig_center, sig_content, sig_err, bg_center, bg_content, bg_err]

def significance(s, b, sqrt_b=False):
    if sqrt_b:
        return s/np.sqrt(b)
    else:
        return np.sqrt(2 * ((s + b)*np.log(1 + (s/b)) - s))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-s", "--signal", nargs="+", required=True, help="signal files")
    parser.add_argument("-b", "--background", required=True, help="a background file")
    parser.add_argument("-New", "--New", required=True, help="Is new combinations definition?")

    args = parser.parse_args()

    background_file = args.background

    nwp = 6
    rejected_wp = (0.0,)
    label = [[i, j, k, m] for i in range(nwp) if i not in rejected_wp
                          for j in range(nwp) if j <= i and j not in rejected_wp
                          for k in range(nwp) if k <= j and k not in rejected_wp
                          for m in range(nwp) if m <= k and m not in rejected_wp]

    # label = {tuple(l): idx + 1 for idx, l in enumerate(label)}

    # combination selection for optimization, only use for New
    selected_label = [row for row in label if (row[0] - row[1] <= 1 and 
                                               row[0] - row[2] <= 1 and 
                                               row[0] - row[3] <= 1)]

    selected_bins = [label.index(row) + 1 for row in selected_label]
    selected_bins = np.array(selected_bins)

    for signal_file in args.signal:

        sig_bg_hist = getHist(signal_file, background_file, isNew=args.New)
        sig_center  = sig_bg_hist[0]
        sig_content = sig_bg_hist[1]
        sig_err     = sig_bg_hist[2]
        bg_center   = sig_bg_hist[3]
        bg_content  = sig_bg_hist[4]
        bg_err      = sig_bg_hist[5]

        sfc, sfc_sqrtB = [], []
        sfc_b0, sfc_b0_sqrt = [], []
        bin_center, bin_center_b0 = [], []
        combine_sfc, combine_sfc_sqrtB, combine_bin_center = [], [], []
        for idx, num_sig in enumerate(sig_content):
            num_bg = bg_content[idx]

            if num_bg == 0:
                # print(f"{signal_file}")
                # print(f"{idx}, {num_sig}, {num_bg}")
                num_bg = 1e-9
                # num_sig *= 5
                sfc_b0.append(significance(num_sig, num_bg, sqrt_b=False))
                sfc_b0_sqrt.append(significance(num_sig, num_bg, sqrt_b=True))
                bin_center_b0.append(bg_center[idx])
            else:
                sfc.append(significance(num_sig, num_bg, sqrt_b=False))
                sfc_sqrtB.append(significance(num_sig, num_bg, sqrt_b=True))
                bin_center.append(bg_center[idx])
            
            combine_sfc.append(significance(num_sig, num_bg, sqrt_b=False))
            combine_sfc_sqrtB.append(significance(num_sig, num_bg, sqrt_b=True))
            combine_bin_center.append(bg_center[idx])

        filename = os.path.basename(signal_file)
        filename, _ = os.path.splitext(filename)

        if args.New == "True":

            hep.style.use("CMS")
            hep.cms.text("", loc=0)

            bin_center = np.array(bin_center)
            sfc = np.array(sfc)
            sfc_sqrtB = np.array(sfc_sqrtB)

            bin_center_b0 = np.array(bin_center_b0)
            sfc_b0 = np.array(sfc_b0)
            sfc_b0_sqrt = np.array(sfc_b0_sqrt)

            combine_bin_center          = np.array(combine_bin_center)
            combine_sfc                 = np.array(combine_sfc)
            combine_sfc_sqrtB           = np.array(combine_sfc_sqrtB)

            bin_center_selected         = bin_center[np.isin(bin_center, selected_bins)]
            sfc_selected                = sfc[np.isin(bin_center, selected_bins)]
            sfc_sqrtB_selected          = sfc_sqrtB[np.isin(bin_center, selected_bins)]

            bin_center_b0_selected      = bin_center_b0[np.isin(bin_center_b0, selected_bins)]
            sfc_b0_selected             = sfc_b0[np.isin(bin_center_b0, selected_bins)]
            sfc_b0_sqrt_selected        = sfc_b0_sqrt[np.isin(bin_center_b0, selected_bins)]

            combine_bin_center_selected = combine_bin_center[np.isin(combine_bin_center, selected_bins)]
            combine_sfc_selected        = combine_sfc[np.isin(combine_bin_center, selected_bins)]
            combine_sfc_sqrtB_selected  = combine_sfc_sqrtB[np.isin(combine_bin_center, selected_bins)]

            # fig, ax = plt.subplots(figsize=(8, 6))

            plt.scatter(bin_center_selected, sfc_selected, label="sqrt(2 * ((S + B)*log(1 + (S/B)) - S))")
            plt.scatter(bin_center_selected, sfc_sqrtB_selected, label="S/sqrt(B)")
            plt.scatter(bin_center_b0_selected, sfc_b0_selected, label="sqrt(2 * ((S + B)*log(1 + (S/B)) - S)), B = 0")
            plt.scatter(bin_center_b0_selected, sfc_b0_sqrt_selected, label="S/sqrt(B), B = 0")

            plt.xticks(combine_bin_center_selected, np.array(label)[selected_bins - 1], fontsize=12, rotation=90)
            plt.tick_params(axis='x', which='minor', bottom=False, top=False)

            plt.xlabel("bins")
            plt.ylabel("Signal Significance")
            # plt.legend(loc="upper left")

            output_file = f"New_significance_{filename}"

            plt.savefig(output_file + ".pdf")
            plt.clf()

            with open(output_file + ".txt", "w") as output_txt:
                output_txt.write(f"Signal: {signal_file}\n")
                for idx, value in enumerate(combine_sfc_selected):    
                    output_txt.write(f"bin {combine_bin_center_selected[idx]} {selected_label[idx]}: {value}, {combine_sfc_sqrtB_selected[idx]}\n") 

            with open(output_file + ".csv", "w", newline="") as output_csv:
                writer = csv.writer(output_csv)
                writer.writerow(["Bin_Center", "Combination", "Long_Significance", "Short_Significance"])
                for idx, value in enumerate(combine_sfc_selected):
                    writer.writerow([combine_bin_center_selected[idx], selected_label[idx], value, combine_sfc_sqrtB_selected[idx]])


        else:
            output_file = f"significance_{filename}"

            with open(output_file + ".txt", "w") as output_txt:
                output_txt.write(f"Signal: {signal_file}\n")
                for idx, value in enumerate(combine_sfc):    
                    output_txt.write(f"bin {combine_bin_center[idx]} {label[idx]}: {value}, {combine_sfc_sqrtB[idx]}\n") 

            with open(output_file + ".csv", "w", newline="") as output_csv:
                writer = csv.writer(output_csv)
                writer.writerow(["Bin_Center", "Combination", "Long_Significance", "Short_Significance"])
                for idx, value in enumerate(combine_sfc):
                    writer.writerow([combine_bin_center[idx], label[idx], value, combine_sfc_sqrtB[idx]])

            hep.style.use("CMS")
            hep.cms.text("", loc=0)

            bin_center = np.array(bin_center)
            sfc = np.array(sfc)
            sfc_sqrtB = np.array(sfc_sqrtB)

            bin_center_b0 = np.array(bin_center_b0)
            sfc_b0 = np.array(sfc_b0)
            sfc_b0_sqrt = np.array(sfc_b0_sqrt)

            combine_bin_center = np.array(combine_bin_center)
            # combine_sfc = np.array(combine_sfc)
            # combine_sfc_sqrtB = np.array(combine_sfc_sqrtB)

            bin_cut = 1
            cut = bin_center >= bin_cut
            cut_b0 = bin_center_b0 >= bin_cut
            cut_combine = combine_bin_center >= bin_cut

            plt.scatter(bin_center[cut], sfc[cut], label="sqrt(2 * ((S + B)*log(1 + (S/B)) - S))")
            plt.scatter(bin_center[cut], sfc_sqrtB[cut], label="S/sqrt(B)")
            plt.scatter(bin_center_b0[cut_b0], sfc_b0[cut_b0], label="sqrt(2 * ((S + B)*log(1 + (S/B)) - S)), B = 0")
            plt.scatter(bin_center_b0[cut_b0], sfc_b0_sqrt[cut_b0], label="S/sqrt(B), B = 0")

            # plt.scatter(bin_center, sfc, label="sqrt(2 * ((S + B)*log(1 + (S/B)) - S))")
            # plt.scatter(bin_center, sfc_sqrtB, label="S/sqrt(B)")
            # plt.scatter(bin_center_b0, sfc_b0, label="sqrt(2 * ((S + B)*log(1 + (S/B)) - S)), B = 0")
            # plt.scatter(bin_center_b0, sfc_b0_sqrt, label="S/sqrt(B), B = 0")

            # due to too many bins, so we show only even bins in x tick labels
            plt.xticks(combine_bin_center[cut_combine][::2], label[bin_cut-1:][::2], fontsize=12, rotation=90)
            plt.tick_params(axis='x', which='minor', bottom=False, top=False)

            plt.xlabel("bins")
            plt.ylabel("Signal Significance")
            # plt.legend(loc="upper left")
            plt.savefig(output_file + ".pdf")
            plt.clf()

            # fig, axs = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]}, figsize=(8, 8))

            # axs[0].scatter(bin_center, sfc, label="sqrt(2 * ((S + B)*log(1 + (S/B)) - S))")
            # axs[0].scatter(bin_center, sfc_sqrtB, label="S/sqrt(B)")
            # axs[0].scatter(bin_center_b0, sfc_b0, label="sqrt(2 * ((S + B)*log(1 + (S/B)) - S)), B = 0")
            # axs[0].scatter(bin_center_b0, sfc_b0_sqrt, label="S/sqrt(B), B = 0")
            # axs[0].xlabel("bins")
            # axs[0].ylabel("Signal Significance")
            # axs[0].legend(loc="upper left")

            # axs[1].scatter(bin_center, bg_err, color="black", label="Background Error")
            # axs[1].set_ylabel("bg error")
            # # axs[1].set_xlabel("Bins")

            # plt.tight_layout()
            # plt.savefig(output_file + ".pdf")
            # plt.clf()
        
        print(f"Output: {output_file}")
        
        
