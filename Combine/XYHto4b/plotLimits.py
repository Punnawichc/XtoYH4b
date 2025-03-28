#######################################################

# This script extracts expected limits from Combine output ROOT files for various signal scenarios
# and plots the expected limits vs MX for each MY. 
# It saves both linear and log-scale plots. 

# command to run this scripts:
# python3 plotLimits.py
# please check "input_dir", "output_dir", "templates", "unavailable" and "label_list" before running

# Created by Punnawich Chokeprasert, punnawich.chokeprasert@cern.ch
# 27 Mar 2025

#######################################################

import ROOT
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep


def plotLimits(log=False):


    input_dir = "/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/CombineHarvester/CombineTools/XYHto4b/workspace_v3"
    output_dir = "/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/CombineHarvester/CombineTools/XYHto4b/ExpLimits_v3"
    
    templates = [1, 2, 3, 4, 5, 6]
    # templates = [6, 7, 8, 9] # for v6

    # v1, v2, v3 (no unavailable)
    unavailable = []

    # v4
    # unavailable = [[1, 4000, 60],  
    #                [2, 2500, 60],
    #                [2, 4000, 60],
    #                [2, 4000, 95],  
    #                [3, 4000, 60], 
    #                [4, 4000, 60], 
    #                [5, 4000, 60], 
    #                [6, 4000, 60]]

    # v5
    # unavailable = [[1, 4000, 60],   
    #                [3, 4000, 60], 
    #                [4, 4000, 60], 
    #                [5, 4000, 60], 
    #                [6, 4000, 60]]

    # v6
    # unavailable = [[8, 4000, 60], 
    #                [9, 4000, 60]]

    unavailable_df = pd.DataFrame(unavailable, columns=["Scenario", "MX", "MY"])

    file_list = []
    for template in templates:
        files = glob.glob(os.path.join(input_dir, f"higgsCombine{template}*"))
        file_list.extend([f for f in files])

    data = []
    # for root_file in args.input:
    for root_file in file_list:

        file_name = os.path.basename(root_file)

        scenario, MX, MY = file_name.split("higgsCombine")[1].split(".")[0].split("_")

        scenario = int(scenario)
        MX       = int(MX)
        MY       = int(MY)

        file = ROOT.TFile.Open(root_file)
        tree = file.Get("limit")

        limits = [confidence_level.limit for confidence_level in tree]

        if len(limits) != 6: # 6 -> 5 expected + 1 observed
            observed = limits[-1] # -1 = observed
            expected = observed
        else:
            expected = limits[2] # 2 = median

        data.append([scenario, MX, MY, expected])

    columns = ["Scenario", "MX", "MY", "Limits"]
    df = pd.DataFrame(data, columns=columns)

    unique_scenes = df["Scenario"].unique()
    unique_MY = df["MY"].unique()

    for my in unique_MY:
        df_my = df[df["MY"] == my]

        if not df_my.empty:

            hep.style.use("CMS")
            hep.cms.text("Preliminary", loc=0)

            exceed_limits = False

            label_list = ["XXT,XXT,>=XT,>=XT", "XXT,XXT,XT,XT", "XXT,XXT,XXT,XT", "XXT,XXT,XXT,XXT", "combined", ">=T,>=T,>=T,>=M"]
            # label_list = ["mX", "mX_mHcut", "mX_mY", "mX_mY_mHcut"] # for v6

            for idx_label, scene in enumerate(unique_scenes):
                df_filtered = df_my[df_my["Scenario"] == scene]
                df_filtered = df_filtered.sort_values(by="MX")
                unavailable_for_scene = unavailable_df[(unavailable_df["Scenario"] == scene) & (unavailable_df["MY"] == my)]

                new_rows = []
                for _, row in unavailable_for_scene.iterrows():
                    mX, mY = row["MX"], row["MY"]

                    if not ((df_filtered["MX"] == mX) & (df_filtered["MY"] == mY)).any():

                        prev_row = df_filtered[df_filtered["MX"] < mX].iloc[-1:]

                        if not prev_row.empty:
                            new_limit = prev_row["Limits"].values[0] * 10 
                        else:
                            new_limit = 0

                        new_rows.append({"Scenario": scene, "MX": mX, "MY": mY, "Limits": new_limit})

                if new_rows:
                    # print(new_rows)
                    df_filtered = pd.concat([df_filtered, pd.DataFrame(new_rows)], ignore_index=True)

                df_filtered = df_filtered.sort_values(by="MX")

                # print(df_filtered)

                if df_filtered["Limits"].max() > 30:
                    exceed_limits = True

                plt.plot(df_filtered["MX"], df_filtered["Limits"], marker="o", linestyle="-", label=f"{label_list[idx_label]}")

            plt.xlabel(fr"$M_X$ [GeV]")
            plt.ylabel("Expected limits at 95% CL [pb]")
            plt.legend(title=fr"$M_Y$ = {my} GeV", title_fontsize=18, fontsize=18)

            if exceed_limits:
                if log:
                    plt.ylim(0.001, 30)
                else:
                    plt.ylim(0, 30)

            if log:
                plt.yscale("log")
                plt.savefig(f"{output_dir}/Exp_limits_MX_MY{int(my)}_log.png") 
                plt.savefig(f"{output_dir}/Exp_limits_MX_MY{int(my)}_log.pdf")
            else:
                plt.savefig(f"{output_dir}/Exp_limits_MX_MY{int(my)}.png") 
                plt.savefig(f"{output_dir}/Exp_limits_MX_MY{int(my)}.pdf")

            plt.clf()


if __name__ == "__main__":

    plotLimits(log=False)
    plotLimits(log=True)
