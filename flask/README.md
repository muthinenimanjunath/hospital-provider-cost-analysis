# Hospital Financial Predictor — Flask App

## Setup Instructions

### 1. Export models from your notebooks

**From `Final_ML_Model.ipynb`** (run all cells), you'll get:
- `profit_margin_model.pkl` — sklearn Pipeline (ColumnTransformer + RandomForest)
- `charity_care_model.pkl` — sklearn Pipeline (ColumnTransformer + RandomForest)
- `feature_metadata.pkl` — dict with feature lists

**From `hospital_clustering.ipynb`** (run all cells), you'll get:
- `kmeans_model.pkl` — fitted KMeans (K=6)
- `scaler.pkl` — fitted StandardScaler (NOT MinMaxScaler)
- `clustered_data.csv` — full dataset with Cluster and performance_score columns

### 2. Place files in the correct folders

```
flask_app/
├── app.py
├── requirements.txt
├── models/
│   ├── profit_margin_model.pkl
│   ├── charity_care_model.pkl
│   ├── feature_metadata.pkl
│   ├── kmeans_model.pkl
│   └── scaler.pkl
├── data/
│   └── clustered_data.csv
└── templates/
    ├── index.html
    ├── result.html
    └── about.html
```

### IMPORTANT: Scaler Fix

Your clustering notebook currently exports a `MinMaxScaler` in cell 32, but the
KMeans model was trained on `StandardScaler` data (cell 6). You need to export
the **StandardScaler** that was used during training. Add this to cell 33:

```python
import joblib

# Save the StandardScaler used for KMeans training (from cell 6)
joblib.dump(scaler, 'scaler.pkl')         # This is the StandardScaler from cell 6
joblib.dump(kmeans, 'kmeans_model.pkl')
```

Make sure `scaler` refers to the StandardScaler from cell 6, NOT the MinMaxScaler
from cell 32. The variable name `scaler` gets overwritten in cell 32 — rename the
MinMaxScaler in cell 32 to something else (e.g., `perf_scaler`).

### 3. Install and run

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## What was wrong with the original app.py

1. **metadata key mismatch** — notebook saves `metadata['all_features']` but app read `metadata['all']`
2. **Scaler conflict** — cell 32 overwrites `scaler` with MinMaxScaler, but KMeans was trained on StandardScaler
3. **Missing templates** — no HTML files existed
4. **Feature input mismatch** — supervised Pipeline expects 26 features but app only built 5
5. **Data file mismatch** — app loaded `full_clustered_data.csv` which doesn't exist
6. **No error handling** — app crashed silently on bad inputs
