"""

Run this script ONCE to fix the scaler.pkl file.

Problem: Your clustering notebook's cell 32 overwrites the StandardScaler 
(used for KMeans training) with a MinMaxScaler (used for performance scoring).
Cell 33 then exports the WRONG scaler.

This script re-creates the correct StandardScaler by fitting it on
clustered_data.csv using the same 13 cluster features.

Usage:
  1. Place clustered_data.csv in the data/ folder
  2. Run: python fix_scaler.py
  3. It will overwrite models/scaler.pkl with the correct one
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CLUSTER_FEATURES = [
    'number_of_beds', 'occupancy_rate', 'revenue_per_bed',
    'discharges_per_bed', 'staff_to_bed_ratio', 'avg_length_of_stay',
    'profit_margin_calc', 'cost_to_charge_ratio', 'charity_care_ratio',
    'wage_rn', 'median_income', 'poverty_rate', 'population',
]

# Load the clustered data
csv_path = os.path.join(BASE_DIR, "data", "clustered_data.csv")
df = pd.read_csv(csv_path)
print(f"Loaded {df.shape[0]:,} rows from clustered_data.csv")

# Extract the 13 cluster features and drop NaN
X = df[CLUSTER_FEATURES].dropna()
print(f"Using {X.shape[0]:,} rows after dropping NaN")

# Clip outliers at 1st/99th percentile (same as your notebook cell 6)
for col in CLUSTER_FEATURES:
    lo, hi = X[col].quantile(0.01), X[col].quantile(0.99)
    X[col] = X[col].clip(lo, hi)

# Fit StandardScaler (this is what your notebook cell 6 did)
scaler = StandardScaler()
scaler.fit(X)

# Save
out_path = os.path.join(BASE_DIR, "models", "scaler.pkl")
joblib.dump(scaler, out_path)
print(f"Saved fixed scaler to {out_path}")
print(f"  n_features: {scaler.n_features_in_}")
print(f"  feature_names: {list(scaler.feature_names_in_)}")
print("\nDone! The scaler now matches the 13 features KMeans expects.")
