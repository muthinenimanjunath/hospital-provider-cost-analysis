from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
import traceback

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_pkl(name):
    path = os.path.join(BASE_DIR, "models", name)
    if os.path.exists(path):
        print(f"Loaded: {name}")
        return joblib.load(path)
    print(f"Missing: {name}")
    return None

# Load models
pm_model = load_pkl("profit_margin_model.pkl")
ccr_model = load_pkl("charity_care_model.pkl")
kmeans = load_pkl("kmeans_model.pkl")
cluster_scaler = load_pkl("scaler.pkl")

# Supervised features
ALL_FEATURES = [
    'year','number_of_beds','total_bed_days_available','occupancy_rate',
    'total_discharges__v___xviii___xix___unknown_',
    'total_days__v___xviii___xix___unknown_',
    'fte___employees_on_payroll','staff_to_bed_ratio',
    'revenue_per_bed','discharges_per_bed','avg_length_of_stay',
    'total_other_expenses','rucc_code',
    'wage_physician','wage_practitioner','wage_rn','wage_support',
    'other_healthcare_occupations_wages',
    'population','median_age','median_income','poverty_rate',
    'higher_education_rate',
    'provider_type','ccn_facility_type','type_of_control','rural_urban'
]

# Clustering features 
CLUSTER_FEATURES = [
    'number_of_beds',
    'occupancy_rate',
    'revenue_per_bed',
    'discharges_per_bed',
    'staff_to_bed_ratio',
    'avg_length_of_stay',
    'profit_margin_calc',
    'cost_to_charge_ratio',
    'charity_care_ratio',
    'wage_rn',
    'median_income',
    'poverty_rate',
    'population'
]

CLUSTER_NAMES = {
    0: "High Performing Hospitals",
    1: "High Utilization Hospitals",
    2: "Cost Inefficient Hospitals",
    3: "Underperforming Hospitals",
    4: "Charity Focused Hospitals",
    5: "Staff Heavy Hospitals"
}

def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0

# ------------------ SUPERVISED INPUT ------------------
def build_supervised_input(user_input):
    beds = user_input['beds']
    revenue = user_input['revenue']
    costs = user_input['costs']
    discharges = user_input['discharges']
    staff = user_input['staff']

    row = {col: 0 for col in ALL_FEATURES}

    row['number_of_beds'] = beds
    row['total_bed_days_available'] = beds * 365
    row['fte___employees_on_payroll'] = staff
    row['total_discharges__v___xviii___xix___unknown_'] = discharges
    row['total_days__v___xviii___xix___unknown_'] = discharges * 5
    row['occupancy_rate'] = discharges / (beds * 365) if beds else 0
    row['revenue_per_bed'] = revenue / beds if beds else 0
    row['staff_to_bed_ratio'] = staff / beds if beds else 0
    row['discharges_per_bed'] = discharges / beds if beds else 0
    row['avg_length_of_stay'] = 5
    row['total_other_expenses'] = costs * 0.1
    row['year'] = 2022

    row['provider_type'] = 'General Short-Term (includes CAH)'
    row['ccn_facility_type'] = 'Short-Term Hospital'
    row['type_of_control'] = str(user_input.get('type_of_control', 'Voluntary Nonprofit - Church'))
    row['rural_urban'] = str(user_input.get('rural_urban', 'Urban'))

    df = pd.DataFrame([row])
    return df[ALL_FEATURES]

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict-form")
def predict_form():
    return render_template("predict.html")

@app.route("/segment-form")
def segment_form():
    return render_template("segment.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/supervised", methods=["POST"])
def supervised():
    try:
        user_input = {
            'beds': safe_float(request.form.get('beds')),
            'revenue': safe_float(request.form.get('revenue')),
            'costs': safe_float(request.form.get('costs')),
            'discharges': safe_float(request.form.get('discharges')),
            'staff': safe_float(request.form.get('staff')),
            'rural_urban': request.form.get('rural_urban'),
            'type_of_control': request.form.get('type_of_control')
        }

        sup_input = build_supervised_input(user_input)
        pm_pred = float(pm_model.predict(sup_input).item())
        ccr_pred = float(ccr_model.predict(sup_input).item())

        return render_template("supervised_result.html", r={
            'profit_margin_pct': round(pm_pred * 100, 2),
            'charity_care_pct': round(ccr_pred * 100, 2)
        })

    except Exception as e:
        traceback.print_exc()
        return render_template("predict.html", error=str(e))

@app.route("/unsupervised", methods=["POST"])
def unsupervised():
    try:
        user_input = {
            'beds': safe_float(request.form.get('beds')),
            'revenue': safe_float(request.form.get('revenue')),
            'costs': safe_float(request.form.get('costs')),
            'discharges': safe_float(request.form.get('discharges')),
            'staff': safe_float(request.form.get('staff')),
            'rural_urban': request.form.get('rural_urban', 'Urban'),
            'type_of_control': request.form.get('type_of_control', 'Voluntary Nonprofit - Church')
        }

        # Predict targets needed for clustering
        sup_input = build_supervised_input(user_input)
        pm_pred = float(pm_model.predict(sup_input).item())
        ccr_pred = float(ccr_model.predict(sup_input).item())

        clust_input = pd.DataFrame([{
            'number_of_beds': user_input['beds'],
            'occupancy_rate': user_input['discharges'] / (user_input['beds'] * 365) if user_input['beds'] else 0,
            'revenue_per_bed': user_input['revenue'] / user_input['beds'] if user_input['beds'] else 0,
            'discharges_per_bed': user_input['discharges'] / user_input['beds'] if user_input['beds'] else 0,
            'staff_to_bed_ratio': user_input['staff'] / user_input['beds'] if user_input['beds'] else 0,
            'avg_length_of_stay': 5,
            'profit_margin_calc': pm_pred,
            'cost_to_charge_ratio': user_input['costs'] / user_input['revenue'] if user_input['revenue'] else 1,
            'charity_care_ratio': ccr_pred,
            'wage_rn': 35,
            'median_income': 55000,
            'poverty_rate': 0.13,
            'population': 100000
        }])

        clust_input = clust_input[CLUSTER_FEATURES]
        clust_scaled = cluster_scaler.transform(clust_input)
        cluster_id = int(kmeans.predict(clust_scaled).item())

        return render_template("unsupervised_result.html", r={
            'cluster_name': CLUSTER_NAMES.get(cluster_id, "Unknown Cluster"),
            'pm_pred': round(pm_pred * 100, 2),
            'ccr_pred': round(ccr_pred * 100, 2)
        })

    except Exception as e:
        traceback.print_exc()
        return render_template("segment.html", error=f"Clustering Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)