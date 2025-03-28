#!/bin/bash

input_dir="/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/CombineHarvester/CombineTools/XYHto4b/workspace_v4"

for file in $input_dir/workspace*.root; do
    
    file_name=$(basename "$file")

    comb=$(echo "$file_name" | sed -n 's/.*4b_\([0-9]*\)_.*/\1/p')

    mx_value=$(echo "$file_name" | sed -n 's/.*MX-\([0-9]*\)_MY-[0-9]*.*/\1/p')
    my_value=$(echo "$file_name" | sed -n 's/.*MX-[0-9]*_MY-\([0-9]*\).*/\1/p')

    if [[ -n "$mx_value" && -n "$my_value" ]]; then
        output_name="${comb}_${mx_value}_${my_value}"
        combine -t -1 "$file" -n "$output_name" --rMin -100 --rMax 100

    fi
done

