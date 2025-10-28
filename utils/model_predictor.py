import numpy as np
import joblib
import os
import random

class ServiceTimePredictor:
    def __init__(self):
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the prediction model"""
        pass
    
    def predict(self, features):
        """Predict service time based on features with task-based adjustments"""
        # Base time for different service types
        service_type_times = {
            'general': 2.5,
            'basic': 1.8,
            'standard': 3.2,
            'premium': 4.8,
            'major': 6.5
        }
        
        base_time = service_type_times.get(features['service_type'], 3.0)
        
        # Task-based time adjustments
        task_times = {
            'oil_change': 0.5,
            'air_filter': 0.3,
            'spark_plugs': 1.0,
            'fuel_filter': 0.4,
            'brake_pads': 1.5,
            'brake_fluid': 0.5,
            'brake_discs': 2.0,
            'wheel_alignment': 1.0,
            'tire_rotation': 0.5,
            'wheel_balancing': 0.8,
            'tire_replacement': 1.2,
            'ac_service': 1.5,
            'ac_filter': 0.3,
            'coolant_flush': 1.0,
            'battery_replacement': 0.5,
            'bulb_replacement': 0.4,
            'electrical_check': 0.8,
            'car_wash': 0.5,
            'diagnostic_scan': 0.6,
            'suspension_check': 1.2
        }
        
        # Calculate task-based time
        selected_tasks = features.get('selected_tasks', [])
        task_based_time = sum(task_times.get(task, 0) for task in selected_tasks)
        
        # Use the maximum of base time and task-based time
        if task_based_time > base_time:
            base_time = task_based_time
        
        # Adjust based on car age (older cars take longer)
        current_year = 2024
        car_age = current_year - features['manufacture_year']
        year_factor = 1 + (car_age * 0.08)  # 8% increase per year
        base_time *= min(year_factor, 2.0)  # Max 2x for very old cars
        
        # Adjust based on kilometers
        km_factor = 1 + (features['total_kilometers'] / 100000) * 0.3
        base_time *= min(km_factor, 1.8)
        
        # Adjust based on days since last service
        if features['last_service_days'] > 365:
            maintenance_factor = 1.4
        elif features['last_service_days'] > 180:
            maintenance_factor = 1.2
        else:
            maintenance_factor = 1.0
        base_time *= maintenance_factor
        
        # Adjust based on number of tasks
        task_factor = 1 + (features['number_of_tasks'] * 0.15)
        base_time *= task_factor
        
        # Adjust based on worker availability
        if features['worker_availability'] <= 1:
            worker_factor = 1.4  # Very high workload
        elif features['worker_availability'] <= 3:
            worker_factor = 1.2  # High workload
        elif features['worker_availability'] <= 5:
            worker_factor = 1.0  # Normal workload
        else:
            worker_factor = 0.9  # Low workload
        
        base_time *= worker_factor
        
        # Add some realistic random variation
        variation = np.random.normal(0, 0.15)
        predicted_time = max(1.0, base_time + variation)
        
        return round(predicted_time, 1)

# Global predictor instance
_predictor = ServiceTimePredictor()

def predict_service_time(features):
    """Public function to predict service time"""
    return _predictor.predict(features)