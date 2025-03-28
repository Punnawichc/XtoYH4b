#!/bin/bash

input_dir="/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/CombineHarvester/CombineTools/XYHto4b/datacards_v3"
output_dir="/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/CombineHarvester/CombineTools/XYHto4b/workspace_v6"

for file in "$input_dir"/*.txt; do
    file_name=$(basename "$file")

    output_workspace="${file_name/.txt/.root}"

    text2workspace.py "$file" -o "$output_dir/workspace_$output_workspace"
done

