# **Predicting U.S. Hospital Financial & Operational Efficiency**
### **A Machine Learning Approach Using CMS Cost Reports (2011–2022)**

![Python](https://img.shields.io/badge/Python-3.13-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)
![Institution](https://img.shields.io/badge/St.%20Clair%20College-Group%208-lightgrey)

**Course:** Capstone Project 1 & 2 &nbsp;|&nbsp; **Institution:** St. Clair College &nbsp;|&nbsp; **Instructor:** Prof. Manjari Maheshwari &nbsp;|&nbsp; **Semester:** Winter 2026

**GitHub:** https://github.com/muthinenimanjunath/hospital-provider-cost-analysis

---

## Table of Contents

- [Project Overview](#project-overview)
- [Part 1 — EDA & Dashboards](#part-1--eda--dashboards)
- [Part 2 — Machine Learning & Deployment](#part-2--machine-learning--deployment)
- [Dataset](#dataset)
- [Repository Structure](#repository-structure)
- [Workflow Summary](#workflow-summary)
- [Key Performance Indicators](#key-performance-indicators)
- [Machine Learning Models](#machine-learning-models)
- [Hospital Clustering](#hospital-clustering)
- [Flask Web Application](#flask-web-application)
- [Power BI Dashboards](#power-bi-dashboards)
- [Dashboard Preview](#dashboard-preview)
- [Key Findings](#key-findings)
- [Tools and Technologies](#tools-and-technologies)
- [How to Run the Project](#how-to-run-the-project)
- [Team Members](#team-members)
- [References](#references)

---

## Project Overview

This two-part capstone project analyzes 12 years of CMS Hospital Provider Cost Reports (2011–2022) to understand the financial and operational dynamics of U.S. hospitals, and builds machine learning models to predict hospital financial performance.

**Part 1** establishes the analytical foundation: raw CMS data is consolidated, cleaned, and explored through EDA. Key performance indicators are engineered and Power BI dashboards are developed to surface actionable insights for administrators and policymakers.

**Part 2** extends the framework into predictive analytics: the CMS dataset is enriched with three external data sources — RUCC geographic classifications, BLS healthcare wage data, and U.S. Census ACS socioeconomic indicators — producing a unified dataset of **75,870 hospital-year observations across 56 variables**. Supervised models predict Profit Margin and Charity Care Ratio, unsupervised K-Means clustering identifies six hospital archetypes, and a Flask web application deploys all models for interactive use.

---

## Part 1 — EDA & Dashboards

**Report:** `docs/Capstone_Interim_Report_Group_8.pdf` &nbsp;|&nbsp; **Submitted:** December 8, 2025

### Objectives
- Consolidate and clean CMS cost report data across 12 years into a single analytics-ready dataset
- Engineer KPIs for financial, operational, and geographic performance
- Analyze trends in revenue, expenses, margins, occupancy, and staffing
- Build Power BI dashboards for executive and operational use

### Key Results
- Net patient revenue grew from **$0.77 trillion (2011) to $1.18 trillion (2022)**, but profit margins held flat at **3–4%** as expenses consistently absorbed 94–99% of revenue
- Occupancy rates stayed at **50–52%**, well below traditional benchmarks, reflecting a structural shift toward outpatient and ambulatory care
- Specialty hospitals consistently outperformed general hospitals in profitability and operational efficiency
- Highest profit margins found in South Dakota, Utah, and Alaska; revenue was concentrated in California and New York but not matched by proportional profitability
- Staffing levels showed misalignment with patient demand in several facility types

---

## Part 2 — Machine Learning & Deployment

**Report:** `docs/Final_Report_Group_8.pdf` &nbsp;|&nbsp; **Submitted:** April 21, 2026

### Objectives
- Build a multi-source data engineering pipeline merging CMS, RUCC, BLS, and Census datasets
- Engineer interpretable financial, operational, workforce, and socioeconomic features
- Implement and compare baseline, ensemble, gradient boosting, and kernel-based models
- Apply K-Means clustering to segment hospitals into operational archetypes
- Deploy final models via a Flask web application

### Key Results

**Supervised Models**

| Target | Best Model | Test R² | CV R² |
|--------|-----------|---------|-------|
| Profit Margin | Random Forest | 0.406 | 0.389 ± 0.012 |
| Charity Care Ratio | ExtraTrees | 0.595 | 0.557 ± 0.007 |

**Unsupervised Clustering:** K-Means with K=6, silhouette score = 0.175

---

## Dataset

### Data Sources

| Source | Granularity | Scope | Coverage |
|--------|-------------|-------|----------|
| CMS HCRIS | Hospital–Year | Institutional operations & finance | 2011–2022 |
| RUCC | County | Geographic rurality classification | Static |
| BLS OEWS | State–Year–Occupation | Healthcare workforce wage data | 2011–2022 |
| U.S. Census ACS | County–Year | Community socioeconomic context | 2012–2022 |

### Final ML Dataset
- **75,870** hospital-year observations, **56** variables (pre-selection)
- **69,555** rows used for ML (2012–2022; 2011 excluded due to Census structural missingness)
- **27 predictors** — 23 numerical, 4 categorical
- **Rural/Urban split:** 45,062 urban | 23,022 rural (89–92% RUCC match rate)
- **Train/Test split:** 80/20 using `GroupShuffleSplit` by hospital ID to prevent longitudinal data leakage (all records for a given hospital are isolated to either training or testing)

---

## Repository Structure

```
hospital-provider-cost-analysis/
│
├── data_collection/
│   ├── cms_raw/                          # Raw CMS annual CSVs (2011–2022)
│   ├── combined/
│   │   └── cms_hospital_costs_2011_2022.csv
│   └── data_collection.ipynb
│
├── data_processing/
│   ├── cleaned/
│   │   └── cms_hospital_costs_2011_2022_cleaned.csv
│   └── data_cleaning.ipynb
│
├── eda/
│   ├── kpi_ready/
│   │   └── hospital_kpi_ready.csv
│   └── eda.ipynb
│
├── ml_dataset/
│   └── ml_dataset.csv                    # Final ML-ready merged dataset
│
├── notebooks/
│   ├── Baseline_ML_Model.ipynb           # Linear Regression, KNN, Decision Tree
│   ├── Advanced_ML_Model.ipynb           # XGBoost, LightGBM, SVM, ANN, stacking
│   ├── Advanced_ML_Models_V2.ipynb
│   ├── Advanced_Modelling_V3.ipynb
│   ├── Final_ML_Model.ipynb              # Production: Random Forest + ExtraTrees
│   ├── ML_Dataset_Creation.ipynb         # CMS + BLS + Census + RUCC merge pipeline
│   ├── hospital_clustering.ipynb         # K-Means (K=6), DBSCAN, Hierarchical
│   ├── BLS_Healtcare_Data.ipynb
│   ├── Aggregated_BLS.ipynb
│   ├── combined_bls_files.ipynb
│   ├── CMS_BLS_Census.ipynb
│   ├── CMS_Urban_Rural_BLS_Dataset.ipynb
│   ├── CMS_Urban_Rural_Dataset.ipynb
│   ├── Census_data.ipynb
│   └── [cluster visualizations]          # PCA scatter, heatmap, radar, boxplots, etc.
│
├── flask/
│   ├── app.py                            # Flask application entry point
│   ├── fix_scaler.py                     # Scaler compatibility utility
│   ├── requirements.txt
│   ├── data/
│   │   ├── clustered_data.csv
│   │   └── full_clustered_data.csv
│   ├── static/styles.css
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── predict.html
│   │   ├── result.html
│   │   ├── about.html
│   │   ├── segment.html
│   │   ├── supervised_result.html
│   │   └── unsupervised_result.html
│   └── README.md
│
├── powerbi/
│   ├── Preliminary_Dashboard_Group_8.pbix
│   ├── Final_Dashboard_Group_8.pbix
│   └── images/
│       ├── financial_view.jpg
│       ├── operational_view.jpg
│       └── geographic_view.jpg
│
├── docs/                                 # Interim report, presentation, meeting minutes
├── documents/                            # Business case, project charter, full minutes
├── README.md
└── requirements.txt
```

---

## Workflow Summary

### Part 1 Pipeline

#### 1. Data Collection
**Notebook:** `data_collection/data_collection.ipynb`
- Downloaded and loaded 12 annual CMS cost report files
- Standardized column names and data types across years
- Merged all annual files into a single master dataset
- Output: `data_collection/combined/cms_hospital_costs_2011_2022.csv`

#### 2. Data Cleaning
**Notebook:** `data_processing/data_cleaning.ipynb`
- Missing value imputation and removal
- Duplicate record removal
- Date standardization and numeric conversion
- Outlier detection using IQR thresholds
- Normalization of categorical fields (ownership type, hospital category)
- Output: `data_processing/cleaned/cms_hospital_costs_2011_2022_cleaned.csv`

#### 3. Exploratory Data Analysis
**Notebook:** `eda/eda.ipynb`
- Revenue, expense, and margin trend analysis (2011–2022)
- Facility-type and ownership-type comparisons
- Geographic revenue and profitability mapping
- Staffing vs. utilization analysis
- KPI feature engineering
- Output: `eda/kpi_ready/hospital_kpi_ready.csv`

---

### Part 2 Pipeline

#### 4. Multi-Source Dataset Construction
**Notebook:** `notebooks/ML_Dataset_Creation.ipynb`

Built through a staged merge:
- **Stage 1:** CMS records + RUCC county classifications (by normalized state/county name; ~89–92% match rate)
- **Stage 2:** + U.S. Census ACS indicators (by FIPS code and year; 2012–2022)
- **Stage 3:** + BLS employment-weighted healthcare wage data (by state and year)

BLS data was filtered to SOC codes `29-xxxx` and `31-xxxx`, grouped into five occupation categories (Physician, RN, Practitioner, Support, Other), and aggregated using an employment-weighted formula: W = Σ(wage × employment) / Σ(employment). Census features were retrieved via the ACS API and transformed into `poverty_rate` and `higher_education_rate`.

Output: `ml_dataset/ml_dataset.csv`

#### 5. ML Modelling
Run notebooks in order: `Baseline_ML_Model.ipynb` → `Advanced_ML_Model.ipynb` → `Final_ML_Model.ipynb`

#### 6. Clustering
**Notebook:** `notebooks/hospital_clustering.ipynb`

#### 7. Flask Deployment
**Directory:** `flask/`

---

## Key Performance Indicators

### Financial KPIs

| KPI | Formula |
|-----|---------|
| Profit Margin | (Total Revenue − Total Expenses) / Total Revenue |
| Expense Ratio | Total Expenses / Total Revenue |
| Current Ratio | Current Assets / Current Liabilities |
| Debt-to-Asset Ratio | Total Liabilities / Total Assets |
| Revenue per Bed | Net Patient Revenue / Number of Beds |

### Operational KPIs

| KPI | Formula |
|-----|---------|
| Occupancy Rate | Total Patient Days / Total Bed Days Available |
| Staff-to-Bed Ratio | FTE Employees / Number of Beds |
| Discharges per Bed | Total Discharges / Number of Beds |
| Average Length of Stay | Total Patient Days / Total Discharges |

---

## Machine Learning Models

### Preprocessing Pipeline
A `ColumnTransformer`-based sklearn pipeline was applied consistently across training, cross-validation, and testing with no data leakage:
- **Categorical (4 features):** `SimpleImputer(most_frequent)` → `OneHotEncoder(handle_unknown='ignore')`
- **Numerical (23 features):** `SimpleImputer(median)`

### Feature Set (27 Predictors)

**Numerical (23):** `year`, `number_of_beds`, `total_bed_days_available`, `occupancy_rate`, `total_discharges`, `total_days`, `fte_employees_on_payroll`, `staff_to_bed_ratio`, `revenue_per_bed`, `discharges_per_bed`, `avg_length_of_stay`, `total_other_expenses`, `rucc_code`, `wage_physician`, `wage_practitioner`, `wage_rn`, `wage_support`, `other_healthcare_occupations_wages`, `population`, `median_age`, `median_income`, `poverty_rate`, `higher_education_rate`

**Categorical (4):** `provider_type`, `ccn_facility_type`, `type_of_control`, `rural_urban`

### Leakage Controls
Variables directly involved in target computation were excluded — e.g. `net_income` and `expense_ratio` for Profit Margin; `cost_of_charity_care` and `uncompensated_care_percent` for Charity Care Ratio. High-cardinality geographic identifiers (`fips`, `medicare_cbsa_number`) were also dropped to prevent overfitting.

### Model Comparison

**Profit Margin**

| Model | Train R² | Test R² |
|-------|---------|---------|
| Linear Regression | 0.189 | 0.189 |
| K-Nearest Neighbors | 0.598 | 0.370 |
| Decision Tree | 1.000 | −0.062 |
| **Random Forest (Final)** | **0.831** | **0.406** |
| XGBoost | 0.493 | 0.493 |

**Charity Care Ratio**

| Model | Train R² | Test R² |
|-------|---------|---------|
| Linear Regression | 0.094 | 0.102 |
| K-Nearest Neighbors | 0.429 | 0.136 |
| Decision Tree | 1.000 | 0.161 |
| Random Forest | 0.940 | 0.608 |
| **ExtraTrees (Final)** | **1.000** | **0.595** |
| LightGBM | 0.900 | 0.479 |

### Production Models

**Model 1 — Profit Margin (Random Forest Regressor)**
- `n_estimators=300`, `max_features='sqrt'`, `min_samples_leaf=2`, `random_state=42`
- 5-fold CV R²: **0.389 ± 0.012**
- Saved to: `models/profit_margin_model.pkl`

**Model 2 — Charity Care Ratio (ExtraTrees Regressor)**
- `n_estimators=300`, `max_features='sqrt'`, `min_samples_leaf=1`, `random_state=42`
- 5-fold CV R²: **0.557 ± 0.007**
- Saved to: `models/charity_care_model.pkl`

### Feature Importance Findings
- **Profit Margin** is driven by internal efficiency: `revenue_per_bed`, `debt_to_asset_ratio`, `net_patient_revenue`, `total_costs`, `occupancy_rate`
- **Charity Care Ratio** reflects external context: `cost_to_charge_ratio`, geographic identifiers, `population`, `higher_education_rate`, `wage_rn`

---

## Hospital Clustering

**Notebook:** `notebooks/hospital_clustering.ipynb`

### Approach
13 continuous features spanning capacity, efficiency, financial, and socioeconomic dimensions were standardized using `StandardScaler` before clustering. Three algorithms were evaluated:

| Algorithm | Silhouette Score | Notes |
|-----------|-----------------|-------|
| **K-Means (K=6)** | **0.175** | Selected — best interpretability and separation |
| Hierarchical (Ward, K=6) | 0.091 | Run on 3,000-record sample |
| DBSCAN | 0.062 | 15 clusters, 3.7% noise |

K=6 was selected using the Elbow method (inertia), Silhouette score, Calinski-Harabasz index, and Davies-Bouldin index. The moderate silhouette of 0.175 is consistent with real-world healthcare data, where hospital characteristics vary along continuous gradients rather than forming sharply separable groups.

### Cluster Profiles

| Cluster | Archetype | Key Characteristics |
|---------|-----------|---------------------|
| 0 | Small community hospitals | ~54 beds, low occupancy, ~46% rural |
| 1 | Large teaching hospitals | ~208 beds, high occupancy, 100% urban |
| 2 | Mid-size efficient urban hospitals | High discharges/bed, high revenue/bed |
| 3 | High-revenue specialized facilities | Very high revenue/bed, ~49% rural |
| 4 | Large regional centers | ~193 beds, highest occupancy (~80%) |
| 5 | Large high-volume hospitals | ~291 beds, highest discharges/bed |

> **Scaler note:** The K-Means model uses `StandardScaler` (fitted during training). A separate `MinMaxScaler` (`perf_scaler`) is used only for the performance scoring calculation and must not be confused with the clustering scaler. When exporting `scaler.pkl` for Flask, ensure it references the `StandardScaler` from cell 6 of `hospital_clustering.ipynb`. See `flask/README.md` for details.

---

## Flask Web Application

**Directory:** `flask/` &nbsp;|&nbsp; **Entry point:** `flask/app.py`

### Features
- **Supervised Prediction** — Input hospital characteristics to predict Profit Margin and Charity Care Ratio in real time using the pre-trained sklearn pipelines
- **Unsupervised Segmentation** — Assign a hospital to one of 6 performance clusters using the K-Means model
- **Dynamic Feature Engineering** — The app derives `occupancy_rate`, `revenue_per_bed`, `staff_to_bed_ratio`, and other features from raw user inputs before model inference

### Setup

```bash
cd flask
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Required Model Files

Run notebooks 5 and 6 first to generate these exports, then place them in `flask/models/`:

```
flask/models/
├── profit_margin_model.pkl      # From Final_ML_Model.ipynb
├── charity_care_model.pkl       # From Final_ML_Model.ipynb
├── feature_metadata.pkl         # From Final_ML_Model.ipynb
├── kmeans_model.pkl             # From hospital_clustering.ipynb
└── scaler.pkl                   # StandardScaler from hospital_clustering.ipynb (cell 6)
```

---

## Power BI Dashboards

### Part 1 — Preliminary Dashboard
`powerbi/Preliminary_Dashboard_Group_8.pbix` — Four views built from cleaned CMS data:
- **Executive Summary** — High-level KPI snapshot across all years
- **Financial Performance** — Revenue, expense, and margin trends (2011–2022)
- **Geographic Insights** — State-level revenue and profitability mapping
- **Operational Efficiency** — Occupancy, staffing, and discharge trends

### Part 2 — Final Dashboard
`powerbi/Final_Dashboard_Group_8.pbix` — Extended with the full enriched ML dataset:
- Financial performance with ownership-type breakdowns
- Operational efficiency across rural/urban classifications
- Geographic mapping with drill-down hospital analytics

---

## Dashboard Preview

### Financial Overview
![Financial Overview](powerbi/images/financial_view.jpg)

### Operational Overview
![Operational Overview](powerbi/images/operational_view.jpg)

### Geographic Analysis
![Geographic Analysis](powerbi/images/geographic_view.jpg)

---

## Key Findings

**Financial**
- Revenue grew from $0.77T (2011) to $1.18T (2022), but profit margins remained at 3–4% because expenses absorbed 94–99% of revenue throughout the period
- Specialty hospitals consistently outperformed general hospitals financially and operationally

**Geographic**
- Highest margins in South Dakota, Utah, and Alaska; highest revenue in California and New York, though high revenue does not correlate with higher margins due to elevated operating costs in those states
- Rural hospitals face structural financial disadvantages that internal efficiency alone cannot overcome

**Operational**
- Occupancy rates at 50–52% reflect a long-term structural shift from inpatient to outpatient care delivery
- Staffing misalignment with patient demand was observed across multiple facility types

**Machine Learning**
- Internal efficiency metrics (revenue/bed, staff ratio) dominate Profit Margin prediction — hospitals can most directly influence margins through throughput and resource utilization
- Charity Care Ratio requires both internal financial features and external socioeconomic context to predict accurately — it is partially constrained by regional labor and demand conditions that individual hospitals cannot control
- Tree-based ensembles substantially outperform linear and kernel-based models, confirming strong nonlinear interactions in hospital financial data

---

## Tools and Technologies

| Category | Tools |
|----------|-------|
| Language | Python 3.13 |
| Data Processing | pandas, numpy |
| Visualization | matplotlib, seaborn |
| Machine Learning | scikit-learn (RandomForest, ExtraTrees, KMeans, DBSCAN), XGBoost, LightGBM, joblib |
| External Data | BLS OEWS, U.S. Census ACS API, USDA RUCC |
| Web App | Flask 3.x, Jinja2, HTML/CSS |
| BI & Dashboards | Power BI Desktop |
| Version Control | Git & GitHub |
| Environment | Jupyter Notebook |

---

## How to Run the Project

### Step 1 — Clone the repository
```bash
git clone https://github.com/muthinenimanjunath/hospital-provider-cost-analysis.git
cd hospital-provider-cost-analysis
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run Part 1 notebooks (in order)
```
1. data_collection/data_collection.ipynb
2. data_processing/data_cleaning.ipynb
3. eda/eda.ipynb
```

### Step 4 — Run Part 2 notebooks (in order)
```
4. notebooks/ML_Dataset_Creation.ipynb
5. notebooks/Final_ML_Model.ipynb          ← exports .pkl model files
6. notebooks/hospital_clustering.ipynb     ← exports kmeans + scaler .pkl files
```

### Step 5 — Launch the Flask app
```bash
cd flask
pip install -r requirements.txt
python app.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Step 6 — Open Power BI dashboards
```
powerbi/Final_Dashboard_Group_8.pbix      # Requires Power BI Desktop
```

---

## Team Members

| Name | Role |
|------|------|
| Manjunath Muthineni | Team Lead & Data Integration |
| Abhishekh Choudhary | Data Cleaning Lead |
| Krishna Chaitanya Venuturumilli | Visualization Lead |
| Neha Oberoi | Research & Methodology Lead |
| Rajesh Thota | Documentation Lead |

---

## References

- Centers for Medicare & Medicaid Services. (2023). Healthcare Cost Report Information System (HCRIS). https://data.cms.gov/provider-compliance/cost-report/hospital-provider-cost-report
- Bureau of Labor Statistics. (2023). Occupational Employment and Wage Statistics. https://www.bls.gov/oes
- United States Census Bureau. (2023). American Community Survey 5-Year Estimates. https://www.census.gov
- USDA Economic Research Service. Rural-Urban Continuum Codes. https://www.ers.usda.gov/data-products/rural-urban-continuum-codes
- Bazzoli, G. J., Fareed, N., & Waters, T. M. (2014). Hospital financial performance in the recent recession. *Health Affairs, 33*(5), 739–745.
- Joynt Maddox, K. E., & Sequist, T. D. (2017). The rural hospital crisis. *JAMA, 317*(23), 2369–2370.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning* (2nd ed.). Springer.
- Microsoft Power BI Documentation. https://learn.microsoft.com/en-us/power-bi/
- scikit-learn Documentation. https://scikit-learn.org/stable/
