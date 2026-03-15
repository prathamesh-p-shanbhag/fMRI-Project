import pandas as pd
from scipy import stats
import os

file_path = '/home/your_username/master_dmn_study.csv'
if not os.path.exists(file_path):
    print("Error: master_dmn_study.csv not found.")
else:
    df = pd.read_csv(file_path).dropna()

    shapiro_past = stats.shapiro(df['Past_Score'])
    shapiro_future = stats.shapiro(df['Future_Score'])
    shapiro_var = stats.shapiro(df['DMN_Variance'])

    print("--- Normality Check (p>0.05 means Normal) ---")
    print(f"Past Score: p = {shapiro_past.pvalue:.4f}")
    print(f"Future Score: p = {shapiro_future.pvalue:.4f}")
    print(f"DMN Variance: p = {shapiro_var.pvalue:.4f}\n")

    rho_past, p_past = stats.spearmanr(df['Past_Score'], df['DMN_Variance'])
    rho_future, p_future = stats.spearmanr(df['Future_Score'], df['DMN_Variance'])

    print("--- Correlation with DMN Variance (N=8) ---")
    print(f"Past Thoughts: r = {rho_past:.4f}, p = {p_past:.4f} {'*' if p_past < 0.05 else ''}")
    print(f"Future Thoughts: r = {rho_future:.4f}, p = {p_future:.4f} {'*' if p_future < 0.05 else ''}")

    if p_past < 0.05 or p_future < 0.05:
        print("\nResult: Significant relationship found in at least one component!")
    else:
        print("\nResult: No significant relationship found (p>0.05).")
