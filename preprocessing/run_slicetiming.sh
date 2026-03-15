#!/bin/bash
BASE_DIR="/home/your_username/ds001168"
for sub in 08 09 ...; do
    echo "RUNNING SLICE TIMING: sub-${sub} | SESSION 2"
    FUNC_DIR="${BASE_DIR}/sub-${sub}/ses-2/func"
    
    if [ -d "$FUNC_DIR" ]; then
        cd "$FUNC_DIR"
        INPUT_BOLD="sub-${sub}_ses2_run1_mcf.nii.gz"
        OUTPUT_NAME="sub-${sub}_ses2_run1_stc"
        
        if [ -f "$INPUT_BOLD" ]; then
            slicetimer -i "$INPUT_BOLD" -o "$OUTPUT_NAME" -r 1.96 --odd
            echo "SUCCESS: sub-${sub} slice timing complete."
        else
            echo "ERROR: Motion corrected file not found for sub-${sub}."
        fi
    else
        echo "SKIP: Directory not found for sub-${sub}."
    fi
done
