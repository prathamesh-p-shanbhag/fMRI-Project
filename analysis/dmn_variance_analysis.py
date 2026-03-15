import numpy as np
import nibabel as nib
from nilearn import datasets, image
from scipy.stats import pearsonr
import pandas as pd
import os
import glob

print("Loading Schaefer Atlas...")
atlas = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7)
atlas_filename = atlas.maps
labels = atlas.labels
dmn_indices = [i+1 for i, label in enumerate(labels) if 'Default' in str(label)]

subjects = ['01', ..., '14', ..., '22']
base_dir = '/home/your_username/ds001168'
results = []
behavioral_scores = []
valid_sub_ids = []

print("\n--- Starting Analysis for 22 Subjects ---")
for sub in subjects:
    beh_path = f"{base_dir}/sub-{sub}/ses-2/sub-{sub}_ses-2_scans.tsv"
    if not os.path.exists(beh_path):
        print(f"Skipping Subject {sub}: Behavioral tsv file missing.")
        continue
    
    beh_df = pd.read_csv(beh_path, sep='\t')
    subject_beh_score = beh_df[['past', 'future']].mean().mean()
    
    mni_files = glob.glob(f"{base_dir}/sub-{sub}/ses-2/func/sub-{sub}_ses2_run*_mni.nii.gz")
    if not mni_files:
        print(f"Skipping Subject {sub}: No registered MNI NIFTI files found.")
        continue
        
    subject_run_variances = []
    for run_file in mni_files:
        try:
            img = nib.load(run_file)
            resampled_atlas = image.resample_to_img(atlas_filename, img, interpolation='nearest')
            atlas_data = resampled_atlas.get_fdata()
            data = img.get_fdata()
            dmn_mask = np.isin(atlas_data, dmn_indices)
            dmn_voxels = data[dmn_mask]
            
            mean_int = np.mean(dmn_voxels, axis=1)
            top_1000 = dmn_voxels[np.argsort(mean_int)[-1000:]]
            subject_run_variances.append(np.mean(np.var(top_1000, axis=1)))
        except Exception as e:
            print(f"Error processing {run_file}: {e}")
            
    if subject_run_variances:
        avg_variance = np.mean(subject_run_variances)
        results.append(avg_variance)
        behavioral_scores.append(subject_beh_score)
        valid_sub_ids.append(sub)
        print(f"Subject {sub}: Beh Score = {subject_beh_score:.2f} | DMN Variance = {avg_variance:.4f}")

final_df = pd.DataFrame({
    'Subject_ID': valid_sub_ids,
    'Temporal_MW_Score': behavioral_scores,
    'DMN_Variance': results
})
final_df.to_csv('/home/avyas_kavya/dmn_variance_results.csv', index=False)

if len(results) > 1:
    r, p = pearsonr(behavioral_scores, results)
    print("\n--- FINAL HYPOTHESIS TEST ---")
    print(f"Pearson Correlation (r): {r:.4f}")
    print(f"Significance (p-value): {p:.4f}")
    if p < 0.05:
        print("RESULT: H1 supported. Temporal Mind Wandering predicts DMN variability.")
    else:
        print("RESULT: No significant relationship found (p>0.05).")
