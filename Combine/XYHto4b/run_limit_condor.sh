#!/bin/bash

input_dir="/afs/desy.de/user/c/chokepra/private/XtoYH4b/CMSSW_14_2_1/src/CombineHarvester/CombineTools/XYHto4b/workspace_v6"

templates=(1 2 3 4 5 6)  

submission_file="$input_dir/condor_submit.sh"

for temp in "${templates[@]}"; do  

    files="$input_dir/workspace_XYH_4b_${temp}_13p6TeV_2022_XtoYHto4B_MX-*_MY-*.root"

    for file in $files; do
        if [[ ! -f "$file" ]]; then
            echo "No files matching pattern for template $temp"
            continue
        fi

        file_name=$(basename "$file")

        comb=$(echo "$file_name" | sed -n 's/.*4b_\([0-9]*\)_.*/\1/p')
        mx_value=$(echo "$file_name" | sed -n 's/.*MX-\([0-9]*\)_MY-[0-9]*.*/\1/p')
        my_value=$(echo "$file_name" | sed -n 's/.*MX-[0-9]*_MY-\([0-9]*\).*/\1/p')

        if [[ -n "$mx_value" && -n "$my_value" ]]; then

            output_file="$input_dir/execute_${comb}_${mx_value}_${my_value}.csh"
            output_name="${comb}_${mx_value}_${my_value}"

            cat << EOF > "$output_file"

#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $input_dir
eval \`scramv1 runtime -sh\`
combine -t -1 $file -n $output_name --rMin -100 --rMax 100
EOF

            chmod +x "$output_file"
            echo "Created script: $output_file"

	    output_file_sub="$input_dir/submit_${comb}_${mx_value}_${my_value}.sh"

	    cat << EOF > "$output_file_sub"
universe = vanilla
executable = $output_file
getenv = TRUE
log = $input_dir/job_$output_name.log
output = $input_dir/job_$output_name.out
error = $input_dir/job_$output_name.err
notification = never
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
queue
+MaxRuntime = 100000
EOF
	echo "Created submission script: $output_file_sub"


	echo "condor_submit $output_file_sub" >>  $submission_file

	   fi
   done

done

chmod +x "$submission_file"
