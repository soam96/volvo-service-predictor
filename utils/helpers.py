import random
import string
from datetime import datetime

def generate_service_id():
    """Generate unique service ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"VOL{timestamp}{random_str}"

def format_time(hours):
    """Format time in hours to readable format"""
    if hours < 1:
        minutes = int(hours * 60)
        return f"{minutes} minutes"
    elif hours == 1:
        return "1 hour"
    else:
        return f"{hours:.1f} hours"