# --- Customer Feedback Analysis (CSV version) ---
import pandas as pd
import matplotlib.pyplot as plt

# 0) Point to your CSV
FILE_PATH = r"C:\Users\zeuga\OneDrive\Desktop\Projects\SQL File for Python.csv"

# 1) Load
df = pd.read_csv(FILE_PATH)

# 2) Quick sanity: show columns so we can map names
print("\nColumns:", list(df.columns))

# 3) Try to find likely column names (adapt if your headers differ)
def find_col(df, key):
    key = key.lower()
    for c in df.columns:
        if key in c.lower():
            return c
    return None

sat_col    = find_col(df, "satisfaction")   # e.g., "Average_Satisfaction_Score"
tenure_col = find_col(df, "tenure_group")   # e.g., "Tenure_Group"
flag_col   = find_col(df, "customer_flag")  # optional

print(f"\nGuessed columns -> satisfaction: {sat_col}, tenure_group: {tenure_col}, customer_flag: {flag_col}")

if sat_col is None:
    raise ValueError("Couldn't find a satisfaction column. Open the CSV, pick the exact header that represents satisfaction, and set sat_col manually.")

# 4) Basic cleaning
df = df.copy()
df[sat_col] = pd.to_numeric(df[sat_col], errors="coerce")
df[sat_col].fillna(df[sat_col].median(), inplace=True)

# 5) Simple At-Risk rule (<=4 out of 10; tweak if your scale differs)
df["AtRisk"] = (df[sat_col] <= 4).astype(int)

# 6) Chart 1 — satisfaction distribution
plt.figure(figsize=(8,5))
plt.hist(df[sat_col].dropna(), bins=10, edgecolor="black")
plt.title("Distribution of Satisfaction Scores")
plt.xlabel("Satisfaction Score")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# 7) Chart 2 — At-Risk proportion by Tenure Group (if present)
if tenure_col:
    at_risk_by_tenure = df.groupby(tenure_col)["AtRisk"].mean().sort_values()
    print("\nAt-Risk by Tenure Group:\n", at_risk_by_tenure)

    plt.figure(figsize=(8,5))
    at_risk_by_tenure.plot(kind="bar", edgecolor="black")
    plt.title("At-Risk Customers by Tenure Group (Proportion)")
    plt.xlabel("Tenure Group")
    plt.ylabel("Proportion At Risk")
    plt.tight_layout()
    plt.show()
else:
    print("\nNo tenure_group-like column found. Skipping Chart 2.")

# 8) Retention summary (avg satisfaction & at-risk if flag exists)

