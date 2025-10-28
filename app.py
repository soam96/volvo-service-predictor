from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import numpy as np
import pandas as pd
from datetime import datetime
import joblib

# Import utility modules
from utils.data_validator import validate_inputs, validate_number_plate
from utils.inventory_manager import InventoryManager
from utils.service_center import ServiceCenter
from utils.model_predictor import predict_service_time
from utils.helpers import generate_service_id

app = Flask(__name__, static_folder='static', template_folder='templates')

# Enable CORS for all routes
CORS(app)

# Initialize service components
service_center = ServiceCenter(total_workers=8)
inventory_manager = InventoryManager('inventory.json')

# Debug: Print available models
print("=== VOLVO SERVICE PREDICTOR STARTED ===")
print("Available car models in inventory:", inventory_manager.get_available_models())
print("========================================")

@app.route('/')
def index():
    """Main page with input form"""
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/predict', methods=['POST'])
def predict():
    """Predict service time endpoint"""
    try:
        # Get form data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data received'
            }), 400
        
        # Validate inputs
        validation_result = validate_inputs(data)
        if not validation_result['valid']:
            return jsonify({
                'success': False,
                'error': validation_result['error']
            }), 400
        
        # Validate number plate format
        if not validate_number_plate(data['car_number_plate']):
            return jsonify({
                'success': False,
                'error': 'Invalid car number plate format. Use format like MH12AB1234'
            }), 400
        
        # Validate that at least one task is selected
        selected_tasks = data.get('selected_tasks', [])
        if not selected_tasks:
            return jsonify({
                'success': False,
                'error': 'Please select at least one service task'
            }), 400
        
        # Generate service ID
        service_id = generate_service_id()
        
        # Get current queue info
        queue_info = service_center.get_queue_info()
        
        # Prepare features for ML prediction
        selected_tasks = data.get('selected_tasks', [])
        number_of_tasks = len(selected_tasks)
        
        features = {
            'car_model': data['car_model'],
            'manufacture_year': int(data['manufacture_year']),
            'fuel_type': data['fuel_type'],
            'service_type': data['service_type'],
            'last_service_days': int(data['last_service_days']),
            'total_kilometers': int(data['total_kilometers']),
            'km_since_last_service': int(data['km_since_last_service']),
            'number_of_tasks': number_of_tasks,
            'worker_availability': queue_info['worker_availability'],
            'selected_tasks': selected_tasks
        }
        
        # Predict service time
        predicted_time = predict_service_time(features)
        
        # Calculate additional metrics
        workload_percentage = queue_info['workload_percentage']
        queue_position = service_center.add_to_queue(service_id)
        
        # Check parts availability based on selected tasks
        parts_availability = inventory_manager.check_parts_availability_for_tasks(
            data['car_model'], 
            data['service_type'], 
            selected_tasks
        )
        
        # Determine workload level
        if workload_percentage < 40:
            workload_level = "Low"
        elif workload_percentage < 70:
            workload_level = "Medium"
        else:
            workload_level = "High"
        
        # Prepare response
        response = {
            'success': True,
            'service_id': service_id,
            'predicted_service_time': float(predicted_time),
            'workload_percentage': float(workload_percentage),
            'workload_level': workload_level,
            'queue_position': int(queue_position),
            'parts_availability': parts_availability,
            'car_model': data['car_model'],
            'car_number_plate': data['car_number_plate'],
            'last_service_days': int(data['last_service_days']),
            'selected_tasks': selected_tasks,
            'number_of_tasks': number_of_tasks
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/api/inventory')
def get_inventory():
    """Get current inventory status"""
    try:
        inventory = inventory_manager.get_inventory_status()
        return jsonify(inventory)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system/status')
def system_status():
    """Get system status and queue information"""
    try:
        queue_info = service_center.get_queue_info()
        return jsonify(queue_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks')
def get_available_tasks():
    """Get available service tasks"""
    try:
        tasks = {
            'engine_performance': [
                {'value': 'oil_change', 'name': 'Engine Oil Change', 'time': 0.5},
                {'value': 'air_filter', 'name': 'Air Filter Replacement', 'time': 0.3},
                {'value': 'spark_plugs', 'name': 'Spark Plugs Replacement', 'time': 1.0},
                {'value': 'fuel_filter', 'name': 'Fuel Filter Replacement', 'time': 0.4}
            ],
            'brakes_safety': [
                {'value': 'brake_pads', 'name': 'Brake Pads Replacement', 'time': 1.5},
                {'value': 'brake_fluid', 'name': 'Brake Fluid Change', 'time': 0.5},
                {'value': 'brake_discs', 'name': 'Brake Discs Replacement', 'time': 2.0}
            ],
            'wheels_alignment': [
                {'value': 'wheel_alignment', 'name': 'Wheel Alignment', 'time': 1.0},
                {'value': 'tire_rotation', 'name': 'Tire Rotation', 'time': 0.5},
                {'value': 'wheel_balancing', 'name': 'Wheel Balancing', 'time': 0.8},
                {'value': 'tire_replacement', 'name': 'Tire Replacement', 'time': 1.2}
            ],
            'ac_cooling': [
                {'value': 'ac_service', 'name': 'AC Service', 'time': 1.5},
                {'value': 'ac_filter', 'name': 'AC Filter Replacement', 'time': 0.3},
                {'value': 'coolant_flush', 'name': 'Coolant Flush', 'time': 1.0}
            ],
            'electrical_battery': [
                {'value': 'battery_replacement', 'name': 'Battery Replacement', 'time': 0.5},
                {'value': 'bulb_replacement', 'name': 'Bulb Replacement', 'time': 0.4},
                {'value': 'electrical_check', 'name': 'Electrical System Check', 'time': 0.8}
            ],
            'additional_services': [
                {'value': 'car_wash', 'name': 'Car Wash & Cleaning', 'time': 0.5},
                {'value': 'diagnostic_scan', 'name': 'Diagnostic Scan', 'time': 0.6},
                {'value': 'suspension_check', 'name': 'Suspension Check', 'time': 1.2}
            ]
        }
        return jsonify(tasks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test')
def test_route():
    """Test route to check if server is working"""
    return jsonify({
        'message': 'Server is running!',
        'timestamp': datetime.now().isoformat(),
        'status': 'OK',
        'inventory_models': inventory_manager.get_available_models()
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Volvo Service Time Predictor',
        'inventory_models': inventory_manager.get_available_models(),
        'total_workers': service_center.total_workers,
        'current_queue': len(service_center.queue)
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)