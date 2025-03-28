#######################################################

# This script processes signal or background in root files containing jet-level information 
# to analyze the combinations of b-tagging working points (WP) for 4 jets 
# using either the PNetB or RobustParTAK4B taggers. 
# It loops over events in the JetTree, extracts tagging decisions and weights, 
# categorizes events based on combinations of WP indices, and show in histograms.
# The script supports both standard and optimized combinations (the "new" mode),
# (1 = pass loose but fail medium ... 2, 3, 4 ,5) and (1 = pass loose ... 2, 3, 4 ,5) respectively.
# And saves the outputs in both .txt and .root. 

# command to run this scripts:
# python3 CombineHist.py -i [path/file*.root] -isSignal [1 or 0] (1 = signal, 0 = background)

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################

import argparse
import os
import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep


def Make_Hist(input_file, output_file, isPNet=True):

    file = ROOT.TFile.Open(input_file, "READ")

    tree = file.Get("JetTree")

    all_branches = [branch.GetName() for branch in tree.GetListOfBranches()]

    if isPNet:
        method = "PNetB"
    else:
        method = "RobustParTAK4B"

    jet_branch    = [name for name in all_branches if name.startswith(f"jetAK4_btag_{method}")]
    weight_branch = [name for name in all_branches if name.startswith("Weight")]

    b_tag_pass = {suffix: [] for suffix in ["L", "M", "T", "XT", "XXT"]}

    for name in all_branches:
        if name.startswith(f"b_tag_{method}_pass_"):
            for suffix in b_tag_pass.keys():
                if name.endswith(f"_{suffix}"):
                    b_tag_pass[suffix].append(name)

    b_tag_pass_L   = b_tag_pass["L"]
    b_tag_pass_M   = b_tag_pass["M"]
    b_tag_pass_T   = b_tag_pass["T"]
    b_tag_pass_XT  = b_tag_pass["XT"]
    b_tag_pass_XXT = b_tag_pass["XXT"]

    njets = 4  # max = 6
    nwp = 6
    rejected_wp = (0.0,) # for a single rejected please use (num,)
    # event_wp = [[getattr(event, branch_name) for branch_name in branches[:njets]] for event in tree]

    event_wp, event_weights = [], []
    event_pass = []
    for event in tree:

        jet_wp = [getattr(event, jet) for jet in jet_branch[:njets]]
        
        weight = [getattr(event, weight) for weight in weight_branch[:njets]]

        # if all(value not in rejected_wp for value in jet_wp):  # 0 == not pass loose wp
        #     event_wp.append(jet_wp)
        #     event_weights.append(weight)

        pass_L   = [getattr(event, b) for b in b_tag_pass_L[:njets]]
        pass_M   = [getattr(event, b) for b in b_tag_pass_M[:njets]]
        pass_T   = [getattr(event, b) for b in b_tag_pass_T[:njets]]
        pass_XT  = [getattr(event, b) for b in b_tag_pass_XT[:njets]]
        pass_XXT = [getattr(event, b) for b in b_tag_pass_XXT[:njets]]

        event_wp.append(jet_wp)
        event_weights.append(weight)

        event_pass.append([pass_L, pass_M, pass_T, pass_XT, pass_XXT])

    # this is bin label and also conditions for the new histogram
    label = [[i, j, k, m] for i in range(nwp) if i not in rejected_wp
                          for j in range(nwp) if j <= i and j not in rejected_wp
                          for k in range(nwp) if k <= j and k not in rejected_wp
                          for m in range(nwp) if m <= k and m not in rejected_wp]

    # adding a section for optimization histogram
    new_hist = {}
    for condition in label:
        count = 0
        sum_weight = 0
        for idx, matrix in enumerate(event_pass):
            check = 0
            for idxcond, cond in enumerate(condition):
                if matrix[cond-1][idxcond] == 1:
                    check += 1
            if check == len(condition):
                count += 1
                sum_weight += event_weights[idx][0] 

        mod_weight = sum_weight / count if count != 0 else 0
        new_hist[tuple(condition)] = [count, mod_weight]

    label = {tuple(l): idx + 1 for idx, l in enumerate(label)}

    event_wp_labeled = [label[tuple(wp)] for wp in event_wp if tuple(wp) in label]

    event_weights_labeled = [event_weights[i][0] for i, wp in enumerate(event_wp) if tuple(wp) in label]

    print(f"rejected wp: {rejected_wp}")
    print(f"Events: {len(event_wp_labeled)}")

    if len(event_wp_labeled) == 0: # len(event_wp_labeled) must be == len(event_weights_labeled)
        print(f"Check the input file ------> {input_file}")
        event_wp_labeled = [0]
        event_weights_labeled = [0]

    transformed_new_hist = {label[key]: value for key, value in new_hist.items() if key in label}

    with open(f"{output_file}.txt", "w") as file:
        file.write(f"Label: {len(label)}\n")
        for key, value in label.items():
            file.write(f"{key}: {value}\n")

        # new section here
        file.write(f"Redefining the combinations of WP: {len(new_hist)}\n")
        for key, value in new_hist.items():
            file.write(f"{key}: {value}\n")
        
        file.write(f"\nEvent WP Labeled: {len(event_wp_labeled)}\n")
        for item in event_wp_labeled:
            file.write(f"{item}\n")
        
        file.write(f"\nEvent Weights Labeled: {len(event_weights_labeled)}\n")
        for item in event_weights_labeled:
            file.write(f"{item}\n")

    # hep.style.use("CMS")
    # hep.cms.text("", loc=0)

    # plt.hist(event_wp_labeled, bins=range(min(event_wp_labeled), max(event_wp_labeled)+1), weights=event_weights_labeled, density=False)
    # plt.xlabel("combination WP of 4 jets")
    # plt.ylabel("Entries")
    # plt.savefig(output_file)
    # plt.clf()

    output = ROOT.TFile(f"{output_file}.root", "RECREATE")

    event_wp_labeled_array = ROOT.std.vector('double')(event_wp_labeled)
    event_weights_labeled_array = ROOT.std.vector('double')(event_weights_labeled)

    # min_bin = min(event_wp_labeled)
    # max_bin = max(event_wp_labeled)

    min_bin = 0.5
    max_bin = len(label)
    n_bins = len(label)

    hist = ROOT.TH1D("hist_wp_combinations", "Combination WP of 4 Jets", n_bins, min_bin, max_bin + 0.5)
    new_hist_root = ROOT.TH1D("hist_wp_combinations_new", "New Combination WP of 4 Jets", n_bins, min_bin, max_bin + 0.5)

    hist.Sumw2()
    new_hist_root.Sumw2()

    for wp_labeled, weights_labeled in zip(event_wp_labeled, event_weights_labeled):
        hist.Fill(wp_labeled, weights_labeled)

    for bin_center, count_and_weight in transformed_new_hist.items():
        num_events = count_and_weight[0]
        weight_sum = count_and_weight[1]
        for i in range(num_events):
            new_hist_root.Fill(bin_center, weight_sum)

    hist.GetXaxis().SetTitle("Combination WP of 4 Jets")
    hist.GetYaxis().SetTitle("Entries")

    canvas_hist = ROOT.TCanvas("canvas_hist", "WP Combinations", 800, 600)
    canvas_hist.Draw()
    hist.Draw("HIST") 
    hist.Write()

    new_hist_root.GetXaxis().SetTitle("Combination WP of 4 Jets")
    new_hist_root.GetYaxis().SetTitle("Entries")

    canvas_new_hist = ROOT.TCanvas("canvas_new_hist", "WP Combinations", 800, 600)
    canvas_new_hist.Draw()
    new_hist_root.Draw("HIST") 
    new_hist_root.Write()

    output.Close()

def Uncertainty_Hist(input_hist):

    hist_ = ROOT.TFile.Open(f"{input_hist}.root", "READ")
    hist = hist_.Get("hist_wp_combinations")

    nbins = hist.GetNbinsX()

    hist_center, hist_content = [], []
    hist_err = []
    for i in range(1, nbins + 1):
        hist_center.append(hist.GetBinCenter(i))
        hist_content.append(hist.GetBinContent(i))
        hist_err.append(hist.GetBinError(i) / hist.GetBinContent(i) if hist.GetBinContent(i) != 0 else 0)

    hep.style.use("CMS")
    hep.cms.text("", loc=0)

    plt.scatter(hist_center, hist_err)
    plt.xlabel("bins")
    plt.ylabel("Statistical Uncertainty")

    directory, filename = os.path.split(input_hist)
    output_name = os.path.join(directory, f"Stat_Unc_{filename}.pdf")

    plt.savefig(output_name)
    plt.clf()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-i", "--input", nargs="+", required=True, help="Input ROOT files")
    parser.add_argument("-isSignal", "--isSignal", required=True, help="signal = 1, background = 0")

    args = parser.parse_args()

    for input_ in args.input:
        name = os.path.splitext(os.path.basename(input_))[0]
        if int(args.isSignal):
            dir_path = "signal/"
        else:
            dir_path = "background/"
        output_PNetB = dir_path + "WP_PNetB_" + name
        output_RobustParTAK4B = dir_path + "WP_RobustParTAK4B_" + name

        print(f"Input file: {input_}")

        Make_Hist(input_, output_PNetB, isPNet=True)

        print(f"Output file: {output_PNetB}\n")

        Make_Hist(input_, output_RobustParTAK4B, isPNet=False)

        print(f"Output file: {output_RobustParTAK4B}\n")

        # Uncertainty_Hist(output_)
