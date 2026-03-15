import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os

file_path = '/home/your_username/master_dmn_study.csv'
if not os.path.exists(file_path):
    print("Error: master_dmn_study.csv not found.")
else:
    df = pd.read_csv(file_path).dropna()
    x = df['Temporal_MW_Score']
    y = df['DMN_Variance']
    
    shapiro_x = stats.shapiro(x)
    shapiro_y = stats.shapiro(y)
    is_normal = (shapiro_x.pvalue > 0.05) and (shapiro_y.pvalue > 0.05)
    
    if is_normal:
        corr_type = "Pearson"
        r, p = stats.pearsonr(x, y)
    else:
        corr_type = "Spearman"
        r, p = stats.spearmanr(x, y)
        
    print(f"\n--- Statistical Rigor Report (N={len(df)}) ---")
    print(f"Normality (Shapiro): X_p={shapiro_x.pvalue:.4f}, Y_p={shapiro_y.pvalue:.4f}")
    print(f"Distribution: {'Normal' if is_normal else 'Non-Normal'}")
    print(f"Selected Test: {corr_type}")
    print(f"Correlation ({corr_type} r): {r:.4f}")
    print(f"P-value: {p:.4f}")
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    sns.kdeplot(x, fill=True, ax=axes[0], color="blue", label="MW Score")
    sns.kdeplot(y, fill=True, ax=axes[0], color="red", label="DMN Var")
    axes[0].set_title("Data Distribution (Normality Check)")
    axes[0].legend()
    
    sns.regplot(x=x, y=y, data=df, ax=axes[1], scatter_kws={'s':80, 'alpha':0.6}, line_kws={'color':'red', 'label': f'{corr_type} r={r:.2f}'})
    axes[1].set_title(f"{corr_type} Correlation (p={p:.3f})")
    axes[1].set_xlabel("Temporal MW Score")
    axes[1].set_ylabel(r"DMN Temporal Variance (\sigma^2)")
    plt.tight_layout()
    plt.savefig('/home/your_username/rigorous_analysis_plot.png', dpi=300)
    print("\nVisualization saved: rigorous_analysis_plot.png")
