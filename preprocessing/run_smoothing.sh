#!/bin/bash
BASE_DIR="/home/your_username/ds001168"
for sub in 08 09 . .; do
    echo "RUNNING SMOOTHING: sub-${sub} | 5mm FWHM"
    FUNC_DIR="${BASE_DIR}/sub-${sub}/ses-2/func"
    
    if [ -d "$FUNC_DIR" ]; then
        cd "$FUNC_DIR"
        INPUT_BOLD="sub-${sub}_ses2_run1_stc.nii.gz"
        OUTPUT_NAME="sub-${sub}_ses2_run1_smooth"
        
        if [ -f "$INPUT_BOLD" ]; then
            fslmaths "$INPUT_BOLD" -s 2.12 "$OUTPUT_NAME"
            echo "SUCCESS: sub-${sub} smoothing complete."
        else
            echo "ERROR: STC file not found for sub-${sub}."
        fi
    else
        echo "SKIP: Directory not found for sub-${sub}."
    fi
done
