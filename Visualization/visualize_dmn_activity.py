import numpy as np
import nibabel as nib
from nilearn import datasets, image, plotting
from scipy.stats import pearsonr
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import imageio

base_dir = '/home/your_username/ds001168'
output_dir = '/home/your_username/analysis_plots'
os.makedirs(output_dir, exist_ok=True)
sns.set_theme(style="whitegrid")

print("Loading Schaefer Atlas...")
atlas = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7)
atlas_filename = atlas.maps
labels = atlas.labels
dmn_indices = [i+1 for i, label in enumerate(labels) if 'Default' in str(label)]

subjects = ['08', '09', '10', '11', '12', '13', '14', '15']
results, behavioral_scores, valid_sub_ids = [], [], []

print("\n--- Starting Analysis & Visualization ---")
for sub in subjects:
    beh_path = f"{base_dir}/sub-{sub}/ses-2/sub-{sub}_ses-2_scans.tsv"
    if not os.path.exists(beh_path): continue
    beh_df = pd.read_csv(beh_path, sep='\t')
    subject_beh_score = beh_df[['past', 'future']].mean().mean()
    
    mni_files = glob.glob(f"{base_dir}/sub-{sub}/ses-2/func/sub-{sub}_ses2_run*_mni.nii.gz")
    if not mni_files: continue
    
    subject_run_variances = []
    for run_idx, run_file in enumerate(mni_files):
        try:
            img = nib.load(run_file)
            resampled_atlas = image.resample_to_img(atlas_filename, img, interpolation='nearest')
            atlas_data = resampled_atlas.get_fdata()
            data = img.get_fdata()
            dmn_mask = np.isin(atlas_data, dmn_indices)
            dmn_voxels = data[dmn_mask]
            
            mean_int = np.mean(dmn_voxels, axis=1)
            top_indices = np.argsort(mean_int)[-1000:]
            top_1000 = dmn_voxels[top_indices]
            
            plt.figure(figsize=(10, 4))
            plt.plot(np.mean(top_1000, axis=0), color='royalblue', alpha=0.8)
            plt.title(f"Subject {sub} - Run {run_idx+1}: DMN Mean Timecourse")
            plt.xlabel("Timepoints (TR)")
            plt.ylabel("Signal Intensity")
            plt.savefig(f"{output_dir}/sub-{sub}_run-{run_idx+1}_timecourse.png")
            plt.close()
            
            frames = []
            for t in range(min(20, data.shape[-1])):
                masked_img = image.new_img_like(img, data[:,:,:,t] * dmn_mask)
                plot_file = f"{output_dir}/temp_frame.png"
                plotting.plot_stat_map(masked_img, display_mode='z', cut_coords=5, output_file=plot_file, title=f"Sub {sub} DMN - Frame {t}", colorbar=False)
                frames.append(imageio.imread(plot_file))
                
            imageio.mimsave(f"{output_dir}/sub-{sub}_run-{run_idx+1}_dmn_activity.gif", frames, fps=4)
            subject_run_variances.append(np.mean(np.var(top_1000, axis=1)))
            
        except Exception as e:
            print(f"Error processing {run_file}: {e}")
            
    if subject_run_variances:
        avg_variance = np.mean(subject_run_variances)
        results.append(avg_variance)
        behavioral_scores.append(subject_beh_score)
        valid_sub_ids.append(sub)

final_df = pd.DataFrame({
    'Subject_ID': valid_sub_ids,
    'Temporal_MW_Score': behavioral_scores,
    'DMN_Variance': results
})

plt.figure(figsize=(8,6))
sns.regplot(data=final_df, x='Temporal_MW_Score', y='DMN_Variance', scatter_kws={'s': 100, 'color': 'darkred'}, line_kws={'color': 'black'})
r, p = pearsonr(final_df['Temporal_MW_Score'], final_df['DMN_Variance'])
plt.title(f"Hypothesis Test: MW Score vs DMN Variance\nr ={r:.3f}, p={p:.3f}")
plt.savefig(f"{output_dir}/final_correlation_results.png")

plt.figure(figsize=(6,5))
sns.violinplot(y=final_df['DMN_Variance'], color="skyblue", inner="point")
plt.title("Distribution of DMN Variance Across Cohort")
plt.savefig(f"{output_dir}/dmn_variance_distribution.png")

print(f"\nAnalysis complete. All plots and GIFs saved to: {output_dir}")
