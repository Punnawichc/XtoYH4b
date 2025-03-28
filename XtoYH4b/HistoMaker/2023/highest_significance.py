import ROOT
import os
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

# be careful at the line ###**

# python3 highest_significance.py -s significance_WP_PNetB*.csv -u background/Stat_Unc_combine_background_PNetB.csv -New [True/False]
# please check input file names before running

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-s", "--significance", nargs="+", required=True, help="")
    parser.add_argument("-u", "--uncertainty", required=True, help="")
    parser.add_argument("-New", "--New", required=True, help="")
    
    args = parser.parse_args()

    df_unc = pd.read_csv(args.uncertainty)

    df_unc = df_unc["Uncertainty"]

    highest_row_total = pd.DataFrame()
    for significance in args.significance:

        filename = os.path.basename(significance)
        filename, _ = os.path.splitext(filename)

        if args.New == "True":
            mass = filename.split("_")[7:9] ###
        else:
            mass = filename.split("_")[6:8]  ###

        mass_info = "_".join(mass)
        
        df_sig = pd.read_csv(f"{filename}.csv")

        df = pd.concat([df_sig, df_unc], axis=1)

        max_significance = df["Short_Significance"].max()
        if np.isinf(max_significance):
            print(f"Max significance is infinity. From {filename}")
            continue

        highest_row = df[df["Short_Significance"] == max_significance]

        highest_row.insert(0, "Mass", mass_info)

        highest_row_total = pd.concat([highest_row_total, highest_row], axis=0)

    if args.New == "True":
        output_name = "New_highest_significance_RobustParTAK4B"  ###**
    else:
        output_name = "highest_significance_RobustParTAK4B"  ###**
        
    highest_row_total.to_csv(f"{output_name}.csv", index=False)

    hep.style.use("CMS")
    hep.cms.text("", loc=0)
    plt.scatter(highest_row_total["Bin_Center"], highest_row_total["Long_Significance"], label="sqrt(2 * ((S + B)*log(1 + (S/B)) - S))")
    plt.scatter(highest_row_total["Bin_Center"], highest_row_total["Short_Significance"], label="S/sqrt(B)")
    plt.xticks(highest_row_total["Bin_Center"], highest_row_total["Combination"] , fontsize=11, rotation=90)
    plt.xlabel("bins")
    plt.ylabel("Highest Significance")
    plt.legend()
    plt.savefig(f"{output_name}.pdf")
    plt.clf()

        

        
        

