# Financial and Operational Analysis of U.S. Hospitals  
### CMS Hospital Provider Cost Reports (2011–2022)

## Project Overview
This capstone project analyzes a decade of U.S. Hospital Provider Cost Reports published by the Centers for Medicare & Medicaid Services (CMS).  
The aim is to evaluate hospital financial performance, operational efficiency, and geographic variations from 2011 to 2022.

This project is **currently in progress** as part of the Data Analytics for Business program.  
The preliminary dashboard has been developed, and further refinement, KPI validation, and deep-dive analysis will continue.

The project currently includes:
- Collection and consolidation of yearly CMS cost datasets  
- Initial and secondary data cleaning  
- Exploratory Data Analysis (EDA) and required column selection  
- Creation of a KPI-ready dataset  
- Development of a preliminary Power BI dashboard containing three integrated views  
Additional phases will enhance data validation, dashboard refinement, and insight development.

---

## Objectives
- Combine twelve annual CMS hospital cost report files into a unified dataset  
- Standardize variable names and resolve structural differences across years  
- Perform thorough cleaning, validation, and preprocessing  
- Select key variables for KPI creation  
- Develop financial, operational, and geographic KPIs  
- Build an interactive Power BI dashboard to visualize trends  
- Continue refinement and enhancement as analysis progresses  

---

## Repository Structure

```
hospital-provider-cost-analysis/
│
├── data_collection/
│   ├── cms_raw/                    
│   ├── combined/
│   └── data_collection.ipynb
│
├── data_processing/
│   ├── cleaned/
│   └── data_cleaning.ipynb
│
├── eda/
│   ├── kpi_ready/
│   └── eda.ipynb
│
├── powerbi/
│   └── Preliminary_Dashboard_Group_8.pbix
│
├── README.md
└── requirements.txt
```

---

## Workflow Summary

### 1. Data Collection  
Notebook: `data_collection/data_collection.ipynb`

Tasks performed:
- Imported yearly CMS CostReport CSV files  
- Standardized column names  
- Merged all datasets into one master file  
- Saved combined file to `data_collection/combined/`  

---

### 2. Initial Data Cleaning  
Notebook: `data_processing/data_cleaning.ipynb`

Performed:
- Missing value handling  
- Duplicate removal  
- Data type corrections  
- Standardization of categorical fields  
- Structural validation  

Output:  
`data_processing/cleaned/cms_hospital_costs_2011_2022_cleaned.csv`

---

### 3. Exploratory Data Analysis (EDA)  
Notebook: `eda/eda.ipynb`

Performed:
- Required column selection  
- Second-stage cleaning  
- Handling KPI-specific missing values  
- Validation of financial and operational metrics  
- Exploratory analysis by ownership, facility type, and region  

Output:  
`eda/kpi_ready/hospital_kpi_ready.csv`

---

## Key Performance Indicators (KPIs)

### Financial KPIs
- Profit Margin  
- Expense Ratio  
- Current Ratio  
- Debt-to-Asset Ratio  

### Operational KPIs
- Occupancy Rate  
- Revenue per Bed  
- Staff-to-Bed Ratio  
- Discharges per Bed  
- Average Length of Stay  

---

## Power BI Dashboard  
A preliminary dashboard containing three sections is included:

Location:  
`powerbi/Preliminary_Dashboard_Group_8.pbix`

### Financial Dashboard
- Profit margin, expense ratio, current ratio, debt-to-asset ratio  
- Profit vs expense trend  
- Profit by facility type  
- Revenue by provider type  

### Operational Dashboard
- Occupancy rate  
- Staff-to-bed ratio  
- Discharges per bed  
- Length of stay  
- Revenue per bed  
- Hospital drill-down  

### Geographical Dashboard
- Profit margin by state  
- Revenue centers (city-level)  
- Occupancy by state  
- Profit trends by state and year  

A final refined dashboard will be added as:  
`powerbi/Final_Dashboard_Group_8.pbix`

---

## Tools and Technologies
- Python 3.13  
- pandas, numpy, matplotlib, seaborn  
- Jupyter Notebook  
- Power BI Desktop  
- Git & GitHub  

---

## How to Run the Project

### Step 1 — Clone repository
```
git clone https://github.com/muthinenimanjunath/hospital-provider-cost-analysis.git
cd hospital-provider-cost-analysis
```

### Step 2 — Install dependencies
```
pip install -r requirements.txt
```

### Step 3 — Execute notebooks
1. data_collection.ipynb  
2. data_cleaning.ipynb  
3. eda.ipynb  

### Step 4 — Open Dashboard  
Open:
```
powerbi/Preliminary_Dashboard_Group_8.pbix
```

---

## Project Status
This project is **in progress**.  
Final EDA, KPI enhancements, and dashboard refinement will be completed in upcoming phases.

---

## Team Members (Group 8)
- Manjunath Muthineni – Team Lead & Data Integration  
- Abhishekh Choudhary – Data Cleaning Lead  
- Krishna Chaitanya Venuturumilli – Visualization Lead  
- Neha Oberoi – Finance SME  
- Rajesh Thota – Documentation Lead  

---

## References
- CMS Hospital Provider Cost Report Data  
  https://data.cms.gov/provider-compliance/cost-report/hospital-provider-cost-report  

- Hospital Provider Cost Report Dataset (Data.gov)  
  https://catalog.data.gov/dataset/hospital-provider-cost-report-7c92c  

- Microsoft Power BI Documentation  
  https://learn.microsoft.com/en-us/power-bi/