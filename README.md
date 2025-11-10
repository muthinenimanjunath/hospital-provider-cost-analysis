# 🏥 Financial and Operational Analysis of U.S. Hospitals  
### Using CMS Hospital Provider Cost Report Data (2011–2022)

## 📘 Project Overview
This project analyzes a decade of **U.S. Hospital Cost Reports** published by the **Centers for Medicare & Medicaid Services (CMS)**.  
It focuses on understanding the **financial health**, **operational efficiency**, and **geographic disparities** among hospitals.  
The dataset was compiled from **12 yearly reports (2011–2022)** and integrated into a single analytical framework.

The workflow includes:
- Data collection and combination  
- Data cleaning and quality validation  
- Exploratory data analysis (EDA) and KPI derivation  
- Visualization in Tableau for interactive storytelling  

## 🎯 Objectives
- Consolidate 12 CMS annual cost report files into one master dataset.  
- Standardize column formats and ensure cross-year consistency.  
- Analyze hospital performance based on operational and financial indicators.  
- Derive Key Performance Indicators (KPIs) for comparative benchmarking.  
- Develop Tableau dashboards for data-driven decision insights.

## 🧩 Project Structure
```
hospital-provider-cost-analysis/
│
├── data_collection/
│   ├── cms_raw/                     # Raw yearly CSVs (2011–2022)
│   ├── combined/                    # Combined 2011–2022 dataset
│   └── combine_data.ipynb           # Script to merge files
│
├── data_processing/
│   ├── data_cleaning.ipynb          # Missing values, outliers, standardization
│   └── cleaned_hospital_cost_reports.csv
│
├── eda/
│   └── eda.ipynb                    # Exploratory Data Analysis & KPIs
│
├── tableau_exports/
│   ├── tableau_hospital_financials.csv
│   ├── tableau_geo_summary.csv
│   └── tableau_kpi_by_facility.csv
│
├── reports/
│   ├── EDA.html                     # Exported notebook
│   └── Capstone_Report.docx         # Final report
│
├── README.md
├── requirements.txt
└── .gitignore
```

## ⚙️ Workflow Summary
### 1️⃣ Data Collection
- 12 CMS CSV files (2011–2022) were downloaded and verified for consistent column structure.  
- Files were merged using `combine_data.ipynb`, resulting in:  
  **73,974 rows × 118 columns**

### 2️⃣ Data Cleaning
- Removed invalid or duplicate records.  
- Imputed missing values using median and mode.  
- Applied **Winsorization** to treat extreme outliers.  
- Standardized categorical labels and normalized numeric fields.

### 3️⃣ Exploratory Data Analysis (EDA)
- Examined hospital distributions by **size, location, and ownership type**.  
- Derived KPIs for performance benchmarking:  

| KPI | Formula | Interpretation |
|-----|----------|----------------|
| **Expense Ratio** | Total Expenses / Net Patient Revenue | Cost efficiency |
| **Current Ratio** | Current Assets / Current Liabilities | Liquidity strength |
| **Debt-to-Asset Ratio** | Total Liabilities / Total Assets | Financial leverage |
| **Revenue per Bed** | Net Patient Revenue / Beds | Productivity measure |
| **Staff-to-Bed Ratio** | FTE Employees / Beds | Workforce intensity |
| **Occupancy Rate** | Inpatient Days / Available Bed Days | Resource utilization |
| **Profit Margin** | Net Income / Total Income | Profitability indicator |

### 4️⃣ Visualization (Tableau)
Created **three dashboards** for interactive exploration:

**A. Financial Performance Dashboard**  
- Tracks profit margin and expense ratio by facility type and ownership.  
- Highlights top and bottom 10 hospitals by profitability.  

**B. Operational Efficiency Dashboard**  
- Examines occupancy rate, staffing ratios, and revenue per bed.  
- Identifies efficient vs. under-utilized hospitals.  

**C. Geographic & Equity Dashboard**  
- Displays regional profit margin variation (choropleth map).  
- Compares rural vs. urban performance and charity care ratios.  

## 📊 Key Insights
- **Profit margins** vary sharply between ownership types.  
- **Rural hospitals** show lower profitability but higher uncompensated care.  
- **Occupancy rate** and **staff-to-bed ratio** correlate strongly with revenue per bed.  
- **Pandemic years (2020–2021)** show operational strain with reduced utilization.  

## 🧠 Tools and Technologies
| Category | Tools Used |
|-----------|------------|
| **Programming** | Python 3.13 |
| **Libraries** | pandas, numpy, matplotlib, seaborn |
| **Visualization** | Tableau Desktop / Tableau Public |
| **Documentation** | Jupyter Notebooks, Markdown |
| **Version Control** | Git & GitHub |

## 🚀 How to Run
1. **Clone Repository**
   ```bash
   git clone https://github.com/<your-username>/hospital-provider-cost-analysis.git
   cd hospital-provider-cost-analysis
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Notebooks**
   1. `data_collection/combine_data.ipynb`
   2. `data_processing/data_cleaning.ipynb`
   3. `eda/eda.ipynb`

4. **Open Tableau**
   - Import the three CSVs in `tableau_exports/`
   - Recreate dashboards following the steps in your project report

## 📅 Project Milestones
| Phase | Description | Status |
|-------|--------------|--------|
| Data Collection | Combined 12 yearly CMS reports | ✅ Done |
| Data Cleaning | Imputed, normalized, and validated | ✅ Done |
| KPI Derivation & EDA | Statistical and visual exploration | ✅ Done |
| Tableau Dashboards | Financial, Operational, and Geographic | 🔄 In Progress |
| Final Report | Documentation & Presentation | 🔜 Upcoming |

## ✍️ Author
**Manjunath Muthineni**  
📍 Data Analytics for Business 
📧 muthinenimanjunath@gmail.com  
📆 Capstone Project (Winter 2025)

## 📎 References
- [CMS Hospital Cost Report Data](https://www.cms.gov)  
- [Tableau Public](https://public.tableau.com)  
- [HealthData.gov – U.S. Hospital Data](https://healthdata.gov)

## 📜 License
Licensed under the **MIT License**.  
You may reuse this project with proper attribution.
