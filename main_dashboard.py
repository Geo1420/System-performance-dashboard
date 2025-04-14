import tkinter as tk
from tkinter import ttk
import psutil
import platform
import socket
import os
from ram_dashboard import RamDashboard
from cpu_dashboard import CpuDashboard
from disk_dashboard import DiskDashboard
from gpu_dashboard import GpuDashboard

class SystemInfoDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("System Information Dashboard")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create system info frame
        self.system_frame = ttk.LabelFrame(self.main_frame, text="System Information")
        self.system_frame.pack(fill=tk.X, pady=10)
        
        # Create hardware info frame
        self.hardware_frame = ttk.LabelFrame(self.main_frame, text="Hardware Information")
        self.hardware_frame.pack(fill=tk.X, pady=10)
        
        # Create memory and storage info frame
        self.storage_frame = ttk.LabelFrame(self.main_frame, text="Memory and Storage Information")
        self.storage_frame.pack(fill=tk.X, pady=10)
        
        # Create monitoring buttons frame
        self.buttons_frame = ttk.LabelFrame(self.main_frame, text="Resource Monitoring")
        self.buttons_frame.pack(fill=tk.X, pady=10)
        
        # Create monitoring buttons
        self.create_monitoring_buttons()
        
        # Initialize labels
        self.create_system_labels()
        self.create_hardware_labels()
        self.create_storage_labels()
    
    def create_monitoring_buttons(self):
        # Create buttons for each resource
        resources = [
            ("RAM Consumption", self.open_ram_dashboard),
            ("CPU Load", self.open_cpu_dashboard),
            ("Disk Load", self.open_disk_dashboard),
            ("GPU Load", self.open_gpu_dashboard)
        ]
        
        for text, command in resources:
            button = ttk.Button(self.buttons_frame, text=text, command=command)
            button.pack(side=tk.LEFT, padx=10, pady=5)
    
    def open_ram_dashboard(self):
        window = tk.Toplevel(self.root)
        RamDashboard(window)
    
    def open_cpu_dashboard(self):
        window = tk.Toplevel(self.root)
        CpuDashboard(window)
    
    def open_disk_dashboard(self):
        window = tk.Toplevel(self.root)
        DiskDashboard(window)
    
    def open_gpu_dashboard(self):
        window = tk.Toplevel(self.root)
        GpuDashboard(window)
    
    def format_bytes(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"
    
    def create_system_labels(self):
        # System information
        system_info = {
            "Computer Name": socket.gethostname(),
            "Operating System": f"{platform.system()} {platform.release()}",
            "OS Version": platform.version(),
            "Architecture": platform.machine(),
            "Python Version": platform.python_version()
        }
        
        for key, value in system_info.items():
            label = ttk.Label(self.system_frame, text=f"{key}: {value}")
            label.pack(anchor="w", padx=10, pady=2)
    
    def create_hardware_labels(self):
        # CPU information
        cpu_info = {
            "Processor": platform.processor(),
            "Physical Cores": str(psutil.cpu_count(logical=False)),
            "Logical Cores": str(psutil.cpu_count(logical=True)),
            "CPU Frequency": f"{psutil.cpu_freq().current:.2f} MHz"
        }
        
        for key, value in cpu_info.items():
            label = ttk.Label(self.hardware_frame, text=f"{key}: {value}")
            label.pack(anchor="w", padx=10, pady=2)
    
    def create_storage_labels(self):
        # Memory and storage information
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        storage_info = {
            "Total RAM": self.format_bytes(ram.total),
            "Total Storage": self.format_bytes(disk.total)
        }
        
        for key, value in storage_info.items():
            label = ttk.Label(self.storage_frame, text=f"{key}: {value}")
            label.pack(anchor="w", padx=10, pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemInfoDashboard(root)
    root.mainloop() 