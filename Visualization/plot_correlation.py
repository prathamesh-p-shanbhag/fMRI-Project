import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

df = pd.read_csv('/home/your_username/dmn_variance_results.csv')

plt.figure(figsize=(8,6))
sns.regplot(x='Temporal_MW_Score', y='DMN_Variance', data=df,
            scatter_kws={'s': 100, 'color': 'blue'},
            line_kws={'color': 'red'})

plt.xlabel('Temporal Mind Wandering (Past + Future Mean)', fontsize=12)
plt.ylabel('DMN Temporal Variance', fontsize=12)
plt.title('Correlation: Mind Wandering vs. DMN Variability (H1)', fontsize=14)

r, p = pearsonr(df['Temporal_MW_Score'], df['DMN_Variance'])
plt.text(df['Temporal_MW_Score'].min(), df['DMN_Variance'].max(),
         f'r = {r:.3f}\np = {p:.3f}', fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig('/home/your_username/h1_correlation_plot.png', dpi=300)
print("Plot saved as h1_correlation_plot.png")
