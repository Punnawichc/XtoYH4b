#######################################################

# This script computes and plots the statistical uncertainty of b-tagging working point (WP) combinations 
# from a ROOT histogram. It supports both original and newly defined WP combinations. 
# It reads histograms from ROOT files, calculates bin uncertainties, 
# and generates a scatter plot with bin labels. 
# It also saves the results in both .pdf and .csv formats. 

# command to run this scripts:
# python3 Stat_Unc.py -i [input.root] -New [True/False]

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################


import ROOT
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import csv


def Uncertainty_Hist(input_hist, isNew="False"):

    hist_ = ROOT.TFile.Open(f"{input_hist}.root", "READ")

    if isNew == "True":
        branch_name = "hist_wp_combinations_new"
    else:
        branch_name = "hist_wp_combinations"

    print(f"Branch: {branch_name}")

    hist = hist_.Get(branch_name)

    nbins = hist.GetNbinsX()

    hist_center, hist_content = [], []
    hist_err = []
    for i in range(1, nbins + 1):
        hist_center.append(hist.GetBinCenter(i))
        hist_content.append(hist.GetBinContent(i))
        hist_err.append(hist.GetBinError(i) / hist.GetBinContent(i) if hist.GetBinContent(i) != 0 else 0)

    nwp = 6 
    rejected_wp = (0.0,)
    label = [[i, j, k, m] for i in range(nwp) if i not in rejected_wp
                          for j in range(nwp) if j <= i and j not in rejected_wp
                          for k in range(nwp) if k <= j and k not in rejected_wp
                          for m in range(nwp) if m <= k and m not in rejected_wp]

    selected_label = [row for row in label if (row[0] - row[1] <= 1 and 
                                               row[0] - row[2] <= 1 and 
                                               row[0] - row[3] <= 1)]

    selected_bins = [label.index(row) + 1 for row in selected_label]

    hep.style.use("CMS")
    hep.cms.text("", loc=0)

    if isNew == "True":

        hist_center = np.array(hist_center)
        hist_err = np.array(hist_err)
        selected_bins = np.array(selected_bins)

        hist_center_selected = hist_center[np.isin(hist_center, selected_bins)]
        hist_err_selected = hist_err[np.isin(hist_center, selected_bins)]

        plt.scatter(hist_center_selected, hist_err_selected)
        plt.xlabel("bins")
        plt.ylabel("Statistical Uncertainty")
        plt.xticks(hist_center[np.isin(hist_center, selected_bins)], np.array(label)[selected_bins - 1], fontsize=12, rotation=90)
        plt.tick_params(axis='x', which='minor', bottom=False, top=False)

        directory, name = os.path.split(input_hist)
        output_name = os.path.join(directory, f"New_Stat_Unc_{name}")

        plt.savefig(output_name + ".pdf")
        plt.clf()

        with open(output_name + ".csv", "w", newline="") as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow(["Bin_Center", "Uncertainty"])
            for idx, value in enumerate(hist_err_selected):
                writer.writerow([hist_center_selected[idx], value])

    else:

        plt.scatter(hist_center, hist_err)
        plt.xlabel("bins")
        plt.ylabel("Statistical Uncertainty")
        plt.xticks(hist_center[::2], label[::2], fontsize=12, rotation=90)
        plt.tick_params(axis='x', which='minor', bottom=False, top=False)

        directory, name = os.path.split(input_hist)
        output_name = os.path.join(directory, f"Stat_Unc_{name}")
    
        plt.savefig(output_name + ".pdf")
        plt.clf()

        with open(output_name + ".csv", "w", newline="") as output_csv:
            writer = csv.writer(output_csv)
            writer.writerow(["Bin_Center", "Uncertainty"])
            for idx, value in enumerate(hist_err):
                writer.writerow([hist_center[idx], value])

    print(f"Output: {output_name}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-i", "--input", nargs="+", required=True, help="Input ROOT files")
    parser.add_argument("-New", "--New", required=True, help="New combinations definition")

    args = parser.parse_args()

    for input_file in args.input:
        directory, filename = os.path.split(input_file)
        name = os.path.splitext(filename)[0]
        input_path = os.path.join(directory, name)

        Uncertainty_Hist(input_path, isNew=args.New)


