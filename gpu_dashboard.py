import time
from resource_dashboard import ResourceDashboard
from monitor import get_gpu_usage

class GpuDashboard(ResourceDashboard):
    def __init__(self, root):
        super().__init__(root, "GPU Load Dashboard")
    
    def update_metrics(self):
        while True:
            usage = get_gpu_usage()
            self.usage_label.config(text=f"GPU Usage: {usage}")
            self.update_graph(float(usage.replace('%', '')) if usage != "N/A" else 0)
            time.sleep(1) 