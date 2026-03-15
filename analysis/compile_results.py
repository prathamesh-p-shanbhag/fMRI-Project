import pandas as pd
import os

dmn_variance_results = {
    'sub-08': ..,
    'sub-09': .., 
    .....
}

base_dir = '/home/your_username'
compiled_data = []

for sub, var in dmn_variance_results.items():
    tsv_path = f'{base_dir}/{sub}/ses-2/func/{sub}_ses-2_scans.tsv'
    if os.path.exists(tsv_path):
        df_behav = pd.read_csv(tsv_path, sep='\t')
        if 'past' in df_behav.columns and 'future' in df_behav.columns:
            p_score = df_behav['past'].mean()
            f_score = df_behav['future'].mean()
            compiled_data.append({
                'Subject': sub,
                'Past_Score': p_score,
                'Future_Score': f_score,
                'Temporal_MW_Score': (p_score + f_score) / 2,
                'DMN_Variance': var
            })
            print(f" Paired {sub}: MW={((p_score+f_score)/2):.2f}, Var={var}")
    else:
        print(f"Missing file: {tsv_path}")

if len(compiled_data) > 0:
    final_df = pd.DataFrame(compiled_data)
    final_df.to_csv('/home/your_username/master_dmn_study.csv', index=False)
    print(f"\n SUCCESS: Saved {len(compiled_data)} subjects to master_dmn_study.csv")
else:
    print("\n ERROR: No data was collected. Check your folder paths!")
