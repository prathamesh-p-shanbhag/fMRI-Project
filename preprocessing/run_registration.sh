#!/bin/bash
BASE_DIR="/home/your_username/ds001168"
MNI_TEMPLATE="$FSLDIR/data/standard/MNI152_T1_2mm_brain.nii.gz"

for sub in 08 09 . . .; do
    echo "REGISTERING: sub-${sub}"
    FUNC_DIR="${BASE_DIR}/sub-${sub}/ses-2/func"
    ANAT_DIR="${BASE_DIR}/sub-${sub}/ses-1/anat"
    STRUC_BRAIN="${ANAT_DIR}/sub-${sub}_ses-1_T1w_brain.nii.gz"
    INPUT_FUNC="${FUNC_DIR}/sub-${sub}_ses2_run1_smooth.nii.gz"
    
    if [ -f "$INPUT_FUNC" ] && [ -f "$STRUC_BRAIN" ]; then
        cd "$FUNC_DIR"
        echo "Aligning Functional to Structural..."
        flirt -in "$INPUT_FUNC" -ref "$STRUC_BRAIN" -out func_to_anat.nii.gz -omat func_to_anat.mat -dof 6
        
        echo "Aligning Structural to MNI Standard..."
        flirt -in "$STRUC_BRAIN" -ref "$MNI_TEMPLATE" -out anat_to_standard.nii.gz -omat anat_to_standard.mat -dof 12
        
        echo "Applying final transformation to MNI space..."
        convert_xfm -omat func_to_standard.mat -concat anat_to_standard.mat func_to_anat.mat
        applyxfm4D "$INPUT_FUNC" "$MNI_TEMPLATE" sub-${sub}_ses2_run1_mni.nii.gz func_to_standard.mat -singlematrix
        echo "SUCCESS: sub-${sub} is now in MNI space."
    else
        echo "ERROR: Missing files for sub-${sub}. Check your BET or Smoothing outputs."
    fi
done
