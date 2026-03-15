import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr
import os

subjects = [f'sub-{i:02d}' for i in range(8, 16)]
base_dir = '/home/your_username'
data_list = []
print("--- Data Extraction Started ---")

for sub in subjects:
    try:
        tsv_path = f'{base_dir}/{sub}/ses-2/func/{sub}_ses-2_scans.tsv'
        if os.path.exists(tsv_path):
            behav_df = pd.read_csv(tsv_path, sep='\t')
            avg_past = behav_df['past'].mean()
            avg_future = behav_df['future'].mean()
            combined_mw = (avg_past + avg_future) / 2
            
            dmn_var = 1.0 # Placeholder: Insert variance extraction logic/results here
            data_list.append({
                'Subject': sub,
                'Past_Score': avg_past,
                'Future_Score': avg_future,
                'Temporal_MW_Score': combined_mw,
                'DMN_Variance': dmn_var
            })
            print(f"Loaded: {sub}")
    except Exception as e:
        print(f"Error processing {sub}: {e}")

master_df = pd.DataFrame(data_list)

plt.figure(figsize=(8, 6))
corr = master_df[['Past_Score', 'Future_Score', 'DMN_Variance']].corr(method='spearman')
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, cmap='RdYlBu_r', center=0, square=True, linewidths=.5, cbar_kws={"shrink": .8})
plt.title("Behavior-Brain Connectivity Matrix (N=8)", fontsize=14, pad=20)
plt.savefig('/home/avyas_kavya/sub08_15_heatmap.png', dpi=300)

g = sns.jointplot(x='Temporal_MW_Score', y='DMN_Variance', data=master_df, kind="reg", color="teal", height=7, marginal_kws=dict(bins=8, fill=True))
g.fig.suptitle("DMN Flux vs. Mental Time Travel (Sub 08-15)", y=1.03)
plt.savefig('/home/your_username/sub08_15_jointplot.png', dpi=300)
print("\n--- Visuals Generated: sub08_15_heatmap.png and sub08_15_jointplot.png ---")
