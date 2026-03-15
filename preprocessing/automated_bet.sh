# Ensure you are in the top-level directory of your BIDS dataset
for sub_dir in sub-*; do
    sub=$(basename "$sub_dir")
    input_file="${sub_dir}/ses-1/anat/${sub}_ses-1_T1w.nii.gz"
    
    if [ -f "$input_file" ]; then
        echo "Processing ${sub}..."
        robustfov -i "$input_file" -r "${sub_dir}/ses-1/anat/${sub}_ses-1_T1w_cropped.nii.gz"
        bet "${sub_dir}/ses-1/anat/${sub}_ses-1_T1w_cropped.nii.gz" \
            "${sub_dir}/ses-1/anat/${sub}_ses-1_brain.nii.gz" -R -f 0.35 -m
        echo "Finished ${sub}."
    else
        echo "Skipping ${sub}: File not found at $input_file"
    fi
done
