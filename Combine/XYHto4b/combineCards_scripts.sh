#!/bin/bash

path_dir="/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/CombineHarvester/CombineTools/XYHto4b/datacards_v5"

MX=(300 400 650 900 1200 1800 2500 4000)
MY=(60 95 125 200 400 600 1000)

for mx in "${MX[@]}"; do
    for my in "${MY[@]}"; do
        
        file_2="${path_dir}/XYH_4b_2_13p6TeV_2022_XtoYHto4B_MX-${mx}_MY-${my}_TuneCP5_13p6TeV_madgraph-pythia8.txt"
        file_3="${path_dir}/XYH_4b_3_13p6TeV_2022_XtoYHto4B_MX-${mx}_MY-${my}_TuneCP5_13p6TeV_madgraph-pythia8.txt"
        file_4="${path_dir}/XYH_4b_4_13p6TeV_2022_XtoYHto4B_MX-${mx}_MY-${my}_TuneCP5_13p6TeV_madgraph-pythia8.txt"

        if [[ -f "$file_2" && -f "$file_3" && -f "$file_4" ]]; then
            
            output_file="${path_dir}/XYH_4b_5_13p6TeV_2022_XtoYHto4B_MX-${mx}_MY-${my}_TuneCP5_13p6TeV_madgraph-pythia8.txt"

            combineCards.py \
            XYHto4b_5_5_4_4="$file_2" \
            XYHto4b_5_5_5_4="$file_3" \
            XYHto4b_5_5_5_5="$file_4" \
            > "$output_file"

            echo "Output: $output_file"
        fi
    done
done