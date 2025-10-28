# utils/__init__.py
"""
Volvo Service Prediction System - Utilities Package
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from .inventory_manager import InventoryManager
from .service_center import EnhancedServiceCenter
from .model_predictor import VolvoServicePredictor
from .data_validator import DataValidator
from .helpers import (
    format_car_number, 
    validate_indian_number_plate,
    format_service_time,
    get_workload_color,
    get_availability_color,
    generate_service_id
)

__all__ = [
    'InventoryManager',
    'EnhancedServiceCenter', 
    'VolvoServicePredictor',
    'DataValidator',
    'format_car_number',
    'validate_indian_number_plate',
    'format_service_time',
    'get_workload_color',
    'get_availability_color',
    'generate_service_id'
]

__version__ = '1.0.0'