import psutil
import time
from resource_dashboard import ResourceDashboard

class CpuDashboard(ResourceDashboard):
    def __init__(self, root):
        super().__init__(root, "CPU Load Dashboard")
    
    def update_metrics(self):
        while True:
            usage = psutil.cpu_percent()
            self.usage_label.config(text=f"CPU Usage: {usage}%")
            self.update_graph(usage)
            time.sleep(1) 