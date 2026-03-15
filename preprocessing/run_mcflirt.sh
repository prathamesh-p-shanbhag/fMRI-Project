#!/bin/bash
BASE_DIR="/home/your_username/ds001168"
for sub in 08 09....; do
    echo "RUNNING MCFLIRT: sub-${sub} | SESSION 2 | RUN 1"
    FUNC_DIR="${BASE_DIR}/sub-${sub}/ses-2/func"
    
    if [ -d "$FUNC_DIR" ]; then
        cd "$FUNC_DIR"
        INPUT_BOLD="sub-${sub}_ses-2_task-rest_acq-fullbrain_run-1_bold.nii.gz"
        OUTPUT_NAME="sub-${sub}_ses2_run1_mcf"
        
        if [ -f "$INPUT_BOLD" ]; then
            mcflirt -in "$INPUT_BOLD" -out "$OUTPUT_NAME" -plots
            fsl_tsplot -i "${OUTPUT_NAME}.par" -t "sub-${sub} Ses-2 Rotations (rad)" \
                -u 1 --start=1 --finish=3 -a x,y,z -w 640 -h 144 -o sub-${sub}_ses2_rot_plot.png
            fsl_tsplot -i "${OUTPUT_NAME}.par" -t "sub-${sub} Ses-2 Translations (mm)" \
                -u 1 --start=4 --finish=6 -a x,y,z -w 640 -h 144 -o sub-${sub}_ses2_trans_plot.png
            echo "SUCCESS: sub-${sub} session 2 plots generated."
        else
            echo "ERROR: File INPUT_BOLD not found in FUNC_DIR"
        fi
    else
        echo "SKIP: Session 2 functional directory not found for sub-${sub}."
    fi
done
