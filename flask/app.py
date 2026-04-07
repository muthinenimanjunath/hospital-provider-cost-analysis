"""
Hospital Performance Prediction - Flask v4.0 - Multi-Page Application

Complete multi-page web application with:
- Dashboard with analytics
- Prediction system (10-field simplified form)
- Analytics & Reports
- Admin panel
- Real-time statistics
- Export functionality
- User-friendly navigation

Author: ML Team
Date: 2026
Version: 4.0 - Multi-Page
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os
from pathlib import Path
import logging
from datetime import datetime, timedelta
import json
import time

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'hospital-prediction-v4-2026')
CORS(app)

app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Model configuration
MODEL_DIR = r"C:\Users\manju\Downloads\hospital-provider-cost-analysis-main\hospital-provider-cost-analysis-main\notebooks\models"
PROFIT_MARGIN_MODEL_FILE = 'profit_margin_model.pkl'
CHARITY_CARE_MODEL_FILE = 'charity_care_model.pkl'
METADATA_FILE = 'feature_metadata.pkl'

# Global state
pm_model = None
ccr_model = None
metadata = None
prediction_history = []
app_stats = {
    'start_time': datetime.now().isoformat(),
    'total_requests': 0,
    'successful_predictions': 0,
    'failed_predictions': 0,
    'processing_times': []
}


def load_models():
    """Load trained models and metadata from disk."""
    global pm_model, ccr_model, metadata
    
    try:
        pm_path = os.path.join(MODEL_DIR, PROFIT_MARGIN_MODEL_FILE)
        ccr_path = os.path.join(MODEL_DIR, CHARITY_CARE_MODEL_FILE)
        meta_path = os.path.join(MODEL_DIR, METADATA_FILE)
        
        if not os.path.exists(pm_path):
            raise FileNotFoundError(f'Profit margin model not found at {pm_path}')
        if not os.path.exists(ccr_path):
            raise FileNotFoundError(f'Charity care model not found at {ccr_path}')
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f'Metadata not found at {meta_path}')
        
        logger.info('Loading models...')
        pm_model = joblib.load(pm_path)
        ccr_model = joblib.load(ccr_path)
        metadata = joblib.load(meta_path)
        
        logger.info('✓ Models loaded successfully')
        return True
    
    except Exception as e:
        logger.error(f'✗ Error loading models: {str(e)}')
        return False


def auto_calculate_fields(input_data):
    """Auto-calculate 8 derived fields from 10 user inputs."""
    try:
        beds = float(input_data.get('number_of_beds') or 0)
        discharges = float(input_data.get('total_discharges__v___xviii___xix___unknown_') or 0)
        los = float(input_data.get('avg_length_of_stay') or 0)
        fte = float(input_data.get('fte___employees_on_payroll') or 0)
        
        input_data['total_bed_days_available'] = int(beds * 365) if beds > 0 else 0
        input_data['total_days__v___xviii___xix___unknown_'] = int(discharges * los) if discharges > 0 else 0
        input_data['staff_to_bed_ratio'] = round(fte / beds, 2) if beds > 0 else 0
        input_data['discharges_per_bed'] = round(discharges / beds, 2) if beds > 0 else 0
        
        input_data['rucc_code'] = 3
        input_data['ccn_facility_type'] = 'General Acute Care'
        input_data['provider_type'] = 'Hospital'
        input_data['other_healthcare_occupations_wages'] = 45000
        
        return input_data, True
    except Exception as e:
        logger.error(f'Error in auto-calculation: {str(e)}')
        return input_data, False


def fetch_external_data(input_data):
    """Fetch or provide external demographic and wage data."""
    try:
        external_defaults = {
            'population': 500000,
            'median_age': 42,
            'median_income': 65000,
            'poverty_rate': 12,
            'higher_education_rate': 35,
            'wage_physician': 250000,
            'wage_practitioner': 150000,
            'wage_rn': 85000,
            'wage_support': 35000
        }
        
        for key, default_value in external_defaults.items():
            if key not in input_data or input_data[key] is None or input_data[key] == '':
                input_data[key] = default_value
            else:
                input_data[key] = float(input_data[key])
        
        return input_data, True
    except Exception as e:
        logger.error(f'Error fetching external data: {str(e)}')
        return input_data, False


def validate_input_data(input_dict):
    """Validate all 27 required features."""
    try:
        required_features = metadata['all_features']
        missing_features = [f for f in required_features if f not in input_dict]
        
        if missing_features:
            return False, f'Missing {len(missing_features)} required features'
        return True, 'OK'
    except Exception as e:
        logger.error(f'Validation error: {str(e)}')
        return False, str(e)


def prepare_prediction_data(input_dict):
    """Prepare input data for model prediction."""
    try:
        features = metadata['all_features']
        data_dict = {}
        
        for feature in features:
            value = input_dict.get(feature)
            if feature in metadata['numerical_features']:
                data_dict[feature] = float(value) if value is not None else 0
            else:
                data_dict[feature] = str(value) if value is not None else 'Unknown'
        
        return pd.DataFrame([data_dict]), True
    except Exception as e:
        logger.error(f'Error preparing prediction data: {str(e)}')
        return None, False

# MULTI-PAGE ROUTES

@app.route('/')
def index():
    """Home page - Dashboard."""
    logger.info('Dashboard accessed')
    total_predictions = len(prediction_history)
    avg_pm = np.mean([p['profit_margin'] for p in prediction_history]) if prediction_history else 0
    avg_ccr = np.mean([p['charity_care_ratio'] for p in prediction_history]) if prediction_history else 0
    
    return render_template('index.html', 
                         total_predictions=total_predictions,
                         avg_pm=round(avg_pm, 2),
                         avg_ccr=round(avg_ccr, 2))


@app.route('/predict')
def predict_page():
    """Prediction page - Input form."""
    logger.info('Prediction page accessed')
    return render_template('predict.html')


@app.route('/analytics')
def analytics_page():
    """Analytics page - Reports and charts."""
    logger.info('Analytics page accessed')
    return render_template('analytics.html', predictions_count=len(prediction_history))


@app.route('/history')
def history_page():
    """History page - Previous predictions."""
    logger.info('History page accessed')
    return render_template('history.html')


@app.route('/admin')
def admin_page():
    """Admin page - System management."""
    logger.info('Admin page accessed')
    uptime = (datetime.now() - datetime.fromisoformat(app_stats['start_time'])).total_seconds()
    
    return render_template('admin.html',
                         uptime=uptime,
                         total_requests=app_stats['total_requests'],
                         successful=app_stats['successful_predictions'],
                         failed=app_stats['failed_predictions'])


@app.route('/about')
def about_page():
    """About page - Information."""
    logger.info('About page accessed')
    return render_template('about.html')


# API ROUTES

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make predictions with simplified form data."""
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        logger.info('Prediction request received')
        
        # Auto-calculate and fetch external data
        data, _ = auto_calculate_fields(data)
        data, _ = fetch_external_data(data)
        
        # Validate
        is_valid, error_msg = validate_input_data(data)
        if not is_valid:
            return jsonify({'success': False, 'error': error_msg}), 400
        
        # Prepare and predict
        df_input, prep_success = prepare_prediction_data(data)
        if not prep_success:
            return jsonify({'success': False, 'error': 'Failed to prepare data'}), 400
        
        pm_prediction = float(pm_model.predict(df_input)[0])
        ccr_prediction = float(ccr_model.predict(df_input)[0])
        
        # Store record
        prediction_record = {
            'timestamp': datetime.now().isoformat(),
            'profit_margin': round(pm_prediction, 2),
            'charity_care_ratio': round(ccr_prediction, 2),
            'hospital_info': {
                'beds': int(data.get('number_of_beds', 0)),
                'occupancy': float(data.get('occupancy_rate', 0)),
                'type': str(data.get('type_of_control', 'Unknown')),
                'location': str(data.get('rural_urban', 'Unknown'))
            }
        }
        
        prediction_history.append(prediction_record)
        
        processing_time = time.time() - start_time
        app_stats['total_requests'] += 1
        app_stats['successful_predictions'] += 1
        app_stats['processing_times'].append(processing_time)
        
        logger.info(f'Prediction successful ({processing_time:.3f}s)')
        
        return jsonify({
            'success': True,
            'profit_margin': prediction_record['profit_margin'],
            'charity_care_ratio': prediction_record['charity_care_ratio'],
            'timestamp': prediction_record['timestamp']
        }), 200
    
    except Exception as e:
        app_stats['total_requests'] += 1
        app_stats['failed_predictions'] += 1
        logger.error(f'Prediction error: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/dashboard')
def dashboard_data():
    """Get dashboard statistics."""
    try:
        total = len(prediction_history)
        avg_pm = np.mean([p['profit_margin'] for p in prediction_history]) if prediction_history else 0
        avg_ccr = np.mean([p['charity_care_ratio'] for p in prediction_history]) if prediction_history else 0
        
        return jsonify({
            'success': True,
            'total_predictions': total,
            'average_profit_margin': round(avg_pm, 2),
            'average_charity_care': round(avg_ccr, 2),
            'last_updated': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/history')
def get_history():
    """Get prediction history."""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = prediction_history[-limit:] if prediction_history else []
        
        return jsonify({
            'success': True,
            'count': len(history),
            'predictions': history
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/export')
def export_data():
    """Export prediction history."""
    try:
        if not prediction_history:
            return jsonify({'success': False, 'error': 'No data to export'}), 400
        
        return jsonify({
            'success': True,
            'count': len(prediction_history),
            'exported_at': datetime.now().isoformat(),
            'predictions': prediction_history
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    try:
        models_loaded = pm_model is not None and ccr_model is not None and metadata is not None
        
        return jsonify({
            'status': 'healthy' if models_loaded else 'unhealthy',
            'models_loaded': models_loaded,
            'timestamp': datetime.now().isoformat(),
            'version': '4.0'
        }), 200 if models_loaded else 503
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500


@app.route('/api/analytics')
def analytics_data():
    """Get analytics data for charts."""
    try:
        if not prediction_history:
            return jsonify({'success': True, 'data': []}), 200
        
        # Group by day
        daily_data = {}
        for pred in prediction_history:
            date = pred['timestamp'][:10]
            if date not in daily_data:
                daily_data[date] = {'count': 0, 'avg_pm': 0, 'avg_ccr': 0, 'values_pm': [], 'values_ccr': []}
            
            daily_data[date]['count'] += 1
            daily_data[date]['values_pm'].append(pred['profit_margin'])
            daily_data[date]['values_ccr'].append(pred['charity_care_ratio'])
        
        # Calculate averages
        for date in daily_data:
            daily_data[date]['avg_pm'] = round(np.mean(daily_data[date]['values_pm']), 2)
            daily_data[date]['avg_ccr'] = round(np.mean(daily_data[date]['values_ccr']), 2)
            del daily_data[date]['values_pm']
            del daily_data[date]['values_ccr']
        
        return jsonify({
            'success': True,
            'data': daily_data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear prediction history (admin)."""
    try:
        prediction_history.clear()
        logger.info('History cleared')
        return jsonify({'success': True, 'message': 'History cleared'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Internal error: {str(error)}')
    return render_template('500.html'), 500


if __name__ == '__main__':
    try:
        logger.info('=' * 70)
        logger.info('Hospital Performance Prediction System v4.0')
        logger.info('Multi-Page Web Application')
        logger.info('=' * 70)
        
        if load_models():
            logger.info('✓ Application ready')
            app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
        else:
            logger.error('✗ Failed to load models')
    
    except Exception as e:
        logger.error(f'✗ Fatal error: {str(e)}')
