import random
from datetime import datetime

class ServiceCenter:
    def __init__(self, total_workers=8):
        self.total_workers = total_workers
        self.queue = []
        self.current_workload = random.randint(2, 6)  # Simulate current active services
    
    def add_to_queue(self, service_id):
        """Add service to queue and return position"""
        self.queue.append({
            'service_id': service_id,
            'timestamp': datetime.now(),
            'status': 'waiting'
        })
        return len(self.queue)
    
    def get_queue_info(self):
        """Get current queue information and worker availability"""
        queue_length = len(self.queue)
        
        # Calculate worker availability based on queue and current workload
        available_workers = max(0, self.total_workers - self.current_workload)
        
        # Adjust based on queue length (more queue = less availability)
        if queue_length > 5:
            available_workers = max(0, available_workers - 2)
        elif queue_length > 10:
            available_workers = max(0, available_workers - 4)
        
        # Calculate workload percentage
        workload_percentage = min(100, (self.current_workload / self.total_workers) * 100 + (queue_length * 5))
        
        return {
            'total_workers': self.total_workers,
            'current_workload': self.current_workload,
            'queue_length': queue_length,
            'worker_availability': available_workers,
            'workload_percentage': round(workload_percentage, 1)
        }
    
    def complete_service(self, service_id):
        """Remove service from queue when completed"""
        self.queue = [job for job in self.queue if job['service_id'] != service_id]