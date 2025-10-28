import re

def validate_number_plate(number_plate):
    """Validate Indian car number plate format (MH12AB1234)"""
    if not number_plate:
        return False
    pattern = r'^[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{1,4}$'
    return bool(re.match(pattern, number_plate.upper()))

def validate_inputs(data):
    """Validate all input fields"""
    required_fields = [
        'car_number_plate', 'car_model', 'manufacture_year', 
        'fuel_type', 'service_type', 'last_service_days',
        'total_kilometers', 'km_since_last_service', 'number_of_tasks'
    ]
    
    # Check for missing fields
    for field in required_fields:
        if field not in data or data[field] is None:
            return {'valid': False, 'error': f'Missing required field: {field}'}
    
    # Validate numeric fields
    try:
        year = int(data['manufacture_year'])
        if year < 2000 or year > 2024:
            return {'valid': False, 'error': 'Manufacture year must be between 2000 and 2024'}
        
        last_service_days = int(data['last_service_days'])
        if last_service_days < 0:
            return {'valid': False, 'error': 'Last service days cannot be negative'}
        if last_service_days > 3650:  # 10 years max
            return {'valid': False, 'error': 'Last service date seems too far in the past'}
        
        total_kms = int(data['total_kilometers'])
        if total_kms < 0:
            return {'valid': False, 'error': 'Total kilometers cannot be negative'}
        
        km_since_service = int(data['km_since_last_service'])
        if km_since_service < 0:
            return {'valid': False, 'error': 'KM since last service cannot be negative'}
        
        num_tasks = int(data['number_of_tasks'])
        if num_tasks <= 0:
            return {'valid': False, 'error': 'Number of tasks must be greater than 0'}
        if num_tasks > 20:
            return {'valid': False, 'error': 'Number of tasks cannot exceed 20'}
            
    except (ValueError, TypeError):
        return {'valid': False, 'error': 'Invalid numeric value in input fields'}
    
    return {'valid': True}