import numpy as np
import nibabel as nib
from nilearn import datasets, image
import matplotlib.pyplot as plt
import os
import glob

# 1. Setup Atlas and DMN indices
print("Loading Schaefer Atlas...")
atlas = datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7)
atlas_filename = atlas.maps
labels = atlas.labels
dmn_indices = [i + 1 for i, label in enumerate(labels) if 'Default' in str(label)]

# 2. Define Subjects and Paths
subjects = ['01', '02', '03', '04', '05', '06', '07']
base_dir = '/home/your_username/ds001168'
output_dir = '/home/your_directory'

all_subject_timecourses = []

print("\n--- Extracting DMN Timecourses for Aggregation ---")

for sub in subjects:
    mni_files = glob.glob(f"{base_dir}/sub-{sub}/ses-2/func/sub-{sub}_ses2_mni.nii.gz")
    
    if not mni_files:
        print(f"Skipping Subject {sub}: No files found.")
        continue
        
    run_file = mni_files[0]
    
    try:
        img = nib.load(run_file)
        
        # Resampling atlas and applying mask
        resampled_atlas = image.resample_to_img(atlas_filename, img, interpolation='nearest')
        atlas_data = resampled_atlas.get_fdata()
        data = img.get_fdata() 
        
        dmn_mask = np.isin(atlas_data, dmn_indices)
        dmn_voxels = data[dmn_mask]
        
        # Isolate top 1000 voxels 
        mean_int = np.mean(dmn_voxels, axis=1)
        top_1000 = dmn_voxels[np.argsort(mean_int)[-1000:]]
        
        # Calculate subject's mean BOLD signal and mean-center it
        dmn_timecourse = np.mean(top_1000, axis=0)
        dmn_timecourse_centered = dmn_timecourse - np.mean(dmn_timecourse)
        
        all_subject_timecourses.append(dmn_timecourse_centered)
        print(f"Successfully processed Subject {sub}")
        
    except Exception as e:
        print(f"Error processing Subject {sub}: {e}")

# 3. Calculate Aggregate Measures (Mean and Standard Deviation)
# Convert to a 2D numpy array: shape = (number_of_subjects, number_of_timepoints)
all_data_matrix = np.array(all_subject_timecourses)

# Calculate the mean across all subjects for each timepoint (axis=0)
group_mean_signal = np.mean(all_data_matrix, axis=0)

# Calculate the standard deviation across all subjects for each timepoint
group_std_signal = np.std(all_data_matrix, axis=0)

# 4. Plot the Aggregate Data
plt.figure(figsize=(12, 6))
time_array = np.arange(len(group_mean_signal))

# Plot the solid mean line
plt.plot(time_array, group_mean_signal, color='#1f77b4', linewidth=2, label='Group Mean BOLD Signal')

# Plot the shaded standard deviation region
plt.fill_between(time_array, 
                 group_mean_signal - group_std_signal, 
                 group_mean_signal + group_std_signal, 
                 color='#1f77b4', alpha=0.3, label='± 1 Standard Deviation')

# Format the plot
plt.title('Aggregate DMN BOLD Signal Fluctuation Across Subjects', fontsize=16, fontweight='bold')
plt.xlabel('Time (Volumes / TRs)', fontsize=14)
plt.ylabel('Mean-Centered BOLD Amplitude', fontsize=14)
plt.legend(loc='upper right', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(0, len(time_array))
plt.tight_layout()

# Save the figure
out_file = os.path.join(output_dir, 'aggregate_dmn_variance_plot.png')
plt.savefig(out_file, dpi=300)
plt.close()

print(f"\nClean aggregate plot successfully saved to: {out_file}")
