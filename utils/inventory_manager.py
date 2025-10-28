import json
import os
import random

class InventoryManager:
    def __init__(self, inventory_file='inventory.json'):
        self.inventory_file = inventory_file
        self.inventory = self._load_inventory()
    
    def _load_inventory(self):
        """Load inventory data from JSON file"""
        try:
            if os.path.exists(self.inventory_file):
                with open(self.inventory_file, 'r') as f:
                    return json.load(f)
            else:
                # Return default inventory if file doesn't exist
                return self._create_default_inventory()
        except Exception as e:
            print(f"Error loading inventory: {e}")
            return self._create_default_inventory()
    
    def _create_default_inventory(self):
        """Create default inventory data"""
        default_inventory = {
            "XC90": {
                "oil_filter": {"quantity": 15, "min_threshold": 5},
                "air_filter": {"quantity": 12, "min_threshold": 4},
                "fuel_filter": {"quantity": 8, "min_threshold": 3},
                "brake_pads": {"quantity": 20, "min_threshold": 6},
                "spark_plugs": {"quantity": 25, "min_threshold": 8},
                "battery": {"quantity": 10, "min_threshold": 3},
                "engine_oil": {"quantity": 30, "min_threshold": 10},
                "brake_fluid": {"quantity": 18, "min_threshold": 6},
                "brake_discs": {"quantity": 12, "min_threshold": 4},
                "ac_gas": {"quantity": 25, "min_threshold": 8},
                "ac_filter": {"quantity": 15, "min_threshold": 5},
                "coolant": {"quantity": 22, "min_threshold": 7},
                "tires": {"quantity": 8, "min_threshold": 3}
            },
            "XC60": {
                "oil_filter": {"quantity": 18, "min_threshold": 6},
                "air_filter": {"quantity": 15, "min_threshold": 5},
                "fuel_filter": {"quantity": 10, "min_threshold": 4},
                "brake_pads": {"quantity": 22, "min_threshold": 7},
                "spark_plugs": {"quantity": 28, "min_threshold": 9},
                "battery": {"quantity": 12, "min_threshold": 4},
                "engine_oil": {"quantity": 35, "min_threshold": 12},
                "brake_fluid": {"quantity": 20, "min_threshold": 7},
                "brake_discs": {"quantity": 15, "min_threshold": 5},
                "ac_gas": {"quantity": 28, "min_threshold": 9},
                "ac_filter": {"quantity": 18, "min_threshold": 6},
                "coolant": {"quantity": 25, "min_threshold": 8},
                "tires": {"quantity": 10, "min_threshold": 4}
            },
            "XC40": {
                "oil_filter": {"quantity": 20, "min_threshold": 7},
                "air_filter": {"quantity": 18, "min_threshold": 6},
                "fuel_filter": {"quantity": 12, "min_threshold": 4},
                "brake_pads": {"quantity": 25, "min_threshold": 8},
                "spark_plugs": {"quantity": 30, "min_threshold": 10},
                "battery": {"quantity": 15, "min_threshold": 5},
                "engine_oil": {"quantity": 40, "min_threshold": 15},
                "brake_fluid": {"quantity": 22, "min_threshold": 8},
                "brake_discs": {"quantity": 18, "min_threshold": 6},
                "ac_gas": {"quantity": 30, "min_threshold": 10},
                "ac_filter": {"quantity": 20, "min_threshold": 7},
                "coolant": {"quantity": 28, "min_threshold": 9},
                "tires": {"quantity": 12, "min_threshold": 5}
            },
            "S90": {
                "oil_filter": {"quantity": 12, "min_threshold": 4},
                "air_filter": {"quantity": 10, "min_threshold": 3},
                "fuel_filter": {"quantity": 6, "min_threshold": 2},
                "brake_pads": {"quantity": 18, "min_threshold": 6},
                "spark_plugs": {"quantity": 22, "min_threshold": 7},
                "battery": {"quantity": 8, "min_threshold": 3},
                "engine_oil": {"quantity": 25, "min_threshold": 8},
                "brake_fluid": {"quantity": 15, "min_threshold": 5},
                "brake_discs": {"quantity": 10, "min_threshold": 3},
                "ac_gas": {"quantity": 20, "min_threshold": 7},
                "ac_filter": {"quantity": 12, "min_threshold": 4},
                "coolant": {"quantity": 18, "min_threshold": 6},
                "tires": {"quantity": 6, "min_threshold": 2}
            }
        }
        
        # Save default inventory
        try:
            with open(self.inventory_file, 'w') as f:
                json.dump(default_inventory, f, indent=2)
            print("Default inventory created successfully")
        except Exception as e:
            print(f"Error saving default inventory: {e}")
        
        return default_inventory
    
    def check_parts_availability(self, car_model, service_type):
        """Check parts availability for specific car model and service type"""
        print(f"Checking parts for model: {car_model}, service: {service_type}")
        
        # Normalize car model name (handle case variations)
        car_model = car_model.upper()
        available_models = [model.upper() for model in self.inventory.keys()]
        
        if car_model not in available_models:
            # Try to find matching model
            for model in self.inventory.keys():
                if car_model in model.upper() or model.upper() in car_model:
                    car_model = model
                    break
            else:
                print(f"Model {car_model} not found in inventory. Available models: {list(self.inventory.keys())}")
                return "Model not found"
        
        # Get the correct case model name
        actual_model = None
        for model in self.inventory.keys():
            if model.upper() == car_model:
                actual_model = model
                break
        
        if not actual_model:
            print(f"Could not find actual model for: {car_model}")
            return "Model not found"
        
        model_inventory = self.inventory[actual_model]
        print(f"Found inventory for model: {actual_model}")
        
        # Define required parts for different service types with quantities
        service_requirements = {
            "general": {
                "oil_filter": 1,
                "air_filter": 1,
                "engine_oil": 1
            },
            "basic": {
                "oil_filter": 1,
                "air_filter": 1,
                "engine_oil": 1
            },
            "standard": {
                "oil_filter": 1,
                "air_filter": 1,
                "fuel_filter": 1,
                "engine_oil": 1
            },
            "premium": {
                "oil_filter": 1,
                "air_filter": 1,
                "fuel_filter": 1,
                "spark_plugs": 4,
                "engine_oil": 1
            },
            "major": {
                "oil_filter": 1,
                "air_filter": 1,
                "fuel_filter": 1,
                "spark_plugs": 4,
                "brake_pads": 1,
                "engine_oil": 1
            }
        }
        
        required_parts = service_requirements.get(service_type, {})
        print(f"Required parts for {service_type}: {required_parts}")
        
        # Check if all required parts are available
        missing_parts = []
        low_stock_parts = []
        available_parts = []
        
        for part, required_qty in required_parts.items():
            if part not in model_inventory:
                missing_parts.append(part)
                print(f"Part {part} not found in inventory for model {actual_model}")
                continue
                
            current_qty = model_inventory[part]["quantity"]
            min_threshold = model_inventory[part]["min_threshold"]
            
            print(f"Part {part}: current={current_qty}, required={required_qty}, min_threshold={min_threshold}")
            
            if current_qty < required_qty:
                missing_parts.append(part)
                print(f"Part {part} out of stock (current: {current_qty}, required: {required_qty})")
            elif current_qty <= min_threshold:
                low_stock_parts.append(part)
                print(f"Part {part} low stock (current: {current_qty}, threshold: {min_threshold})")
            else:
                available_parts.append(part)
                print(f"Part {part} available (current: {current_qty})")
        
        print(f"Missing parts: {missing_parts}")
        print(f"Low stock parts: {low_stock_parts}")
        print(f"Available parts: {available_parts}")
        
        if missing_parts:
            if len(missing_parts) == len(required_parts):
                return "All parts out of stock"
            else:
                return f"Some parts out of stock ({', '.join(missing_parts)})"
        elif low_stock_parts:
            return f"All parts available (low stock: {', '.join(low_stock_parts)})"
        else:
            return "All parts available"
    
    def check_parts_availability_for_tasks(self, car_model, service_type, selected_tasks):
        """Check parts availability based on selected tasks"""
        print(f"Checking parts for tasks: {selected_tasks}")
        
        # Normalize car model name
        car_model = car_model.upper()
        available_models = [model.upper() for model in self.inventory.keys()]
        
        if car_model not in available_models:
            for model in self.inventory.keys():
                if car_model in model.upper() or model.upper() in car_model:
                    car_model = model
                    break
            else:
                return "Model not found"
        
        # Get the correct case model name
        actual_model = None
        for model in self.inventory.keys():
            if model.upper() == car_model:
                actual_model = model
                break
        
        if not actual_model:
            return "Model not found"
        
        model_inventory = self.inventory[actual_model]
        
        # Map tasks to required parts
        task_requirements = {
            'oil_change': {'oil_filter': 1, 'engine_oil': 1},
            'air_filter': {'air_filter': 1},
            'spark_plugs': {'spark_plugs': 4},
            'fuel_filter': {'fuel_filter': 1},
            'brake_pads': {'brake_pads': 1},
            'brake_fluid': {'brake_fluid': 1},
            'brake_discs': {'brake_discs': 1},
            'wheel_alignment': {},  # No parts required
            'tire_rotation': {},    # No parts required
            'wheel_balancing': {},  # No parts required
            'tire_replacement': {'tires': 1},
            'ac_service': {'ac_gas': 1},
            'ac_filter': {'ac_filter': 1},
            'coolant_flush': {'coolant': 1},
            'battery_replacement': {'battery': 1},
            'bulb_replacement': {},  # Bulbs are typically in stock
            'electrical_check': {},  # No parts required
            'car_wash': {},         # No parts required
            'diagnostic_scan': {},  # No parts required
            'suspension_check': {}  # No parts required
        }
        
        # Collect all required parts from selected tasks
        required_parts = {}
        for task in selected_tasks:
            if task in task_requirements:
                for part, quantity in task_requirements[task].items():
                    required_parts[part] = required_parts.get(part, 0) + quantity
        
        print(f"Required parts for tasks: {required_parts}")
        
        # Check parts availability
        missing_parts = []
        low_stock_parts = []
        
        for part, required_qty in required_parts.items():
            if part not in model_inventory:
                missing_parts.append(part)
                continue
                
            current_qty = model_inventory[part]["quantity"]
            min_threshold = model_inventory[part]["min_threshold"]
            
            if current_qty < required_qty:
                missing_parts.append(part)
            elif current_qty <= min_threshold:
                low_stock_parts.append(part)
        
        if missing_parts:
            return f"Parts out of stock: {', '.join(missing_parts)}"
        elif low_stock_parts:
            return f"All parts available (low stock: {', '.join(low_stock_parts)})"
        else:
            return "All parts available"
    
    def get_inventory_status(self):
        """Get complete inventory status"""
        return self.inventory
    
    def get_available_models(self):
        """Get list of available car models"""
        return list(self.inventory.keys())
    
    def update_inventory(self, car_model, parts_used):
        """Update inventory after service"""
        if car_model not in self.inventory:
            return False
        
        try:
            for part, quantity in parts_used.items():
                if part in self.inventory[car_model]:
                    self.inventory[car_model][part]["quantity"] = max(
                        0, self.inventory[car_model][part]["quantity"] - quantity
                    )
            
            # Save updated inventory
            with open(self.inventory_file, 'w') as f:
                json.dump(self.inventory, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error updating inventory: {e}")
            return False
    
    def add_new_model(self, model_name, parts_config):
        """Add a new car model to inventory"""
        try:
            self.inventory[model_name] = parts_config
            with open(self.inventory_file, 'w') as f:
                json.dump(self.inventory, f, indent=2)
            return True
        except Exception as e:
            print(f"Error adding new model: {e}")
            return False