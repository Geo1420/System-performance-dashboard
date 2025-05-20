import psutil
import time
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import platform

class DiskDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Performance Dashboard")
        self.root.geometry("400x600")
        
        # Configure dark theme colors
        self.bg_color = "#1E1E1E"  # Dark background
        self.fg_color = "#FFFFFF"  # White text
        self.accent_color = "#00FF9D"  # Neon green accent
        self.frame_bg = "#2D2D2D"  # Slightly lighter background for frames
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabelframe", background=self.frame_bg, foreground=self.fg_color)
        self.style.configure("TLabelframe.Label", background=self.frame_bg, foreground=self.accent_color)
        self.style.configure("TLabel", background=self.frame_bg, foreground=self.fg_color)
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create disk info frame
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Disk Information")
        self.info_frame.pack(fill=tk.X, pady=10)
        
        # Disk Information labels
        self.disk_name_label = ttk.Label(self.info_frame, text="Disk: Loading...")
        self.disk_name_label.pack(pady=2)
        
        self.disk_type_label = ttk.Label(self.info_frame, text="Type: Loading...")
        self.disk_type_label.pack(pady=2)
        
        self.disk_fs_label = ttk.Label(self.info_frame, text="File System: Loading...")
        self.disk_fs_label.pack(pady=2)
        
        # Create usage frame
        self.usage_frame = ttk.LabelFrame(self.main_frame, text="Current Usage")
        self.usage_frame.pack(fill=tk.X, pady=10)
        
        # Disk Usage labels
        self.disk_usage_label = ttk.Label(self.usage_frame, text="Disk Usage: 0.00%")
        self.disk_usage_label.pack(pady=2)
        
        self.total_space_label = ttk.Label(self.usage_frame, text="Total Space: 0 GB")
        self.total_space_label.pack(pady=2)
        
        self.used_space_label = ttk.Label(self.usage_frame, text="Used Space: 0 GB")
        self.used_space_label.pack(pady=2)
        
        self.free_space_label = ttk.Label(self.usage_frame, text="Free Space: 0 GB")
        self.free_space_label.pack(pady=2)
        
        # Create IO frame
        self.io_frame = ttk.LabelFrame(self.main_frame, text="Disk I/O")
        self.io_frame.pack(fill=tk.X, pady=10)
        
        self.read_speed_label = ttk.Label(self.io_frame, text="Read Speed: 0 MB/s")
        self.read_speed_label.pack(pady=2)
        
        self.write_speed_label = ttk.Label(self.io_frame, text="Write Speed: 0 MB/s")
        self.write_speed_label.pack(pady=2)
        
        # Create graph frame
        self.graph_frame = ttk.LabelFrame(self.main_frame, text="Usage Gauge")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create matplotlib figure with dark theme
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(4, 4), facecolor=self.frame_bg)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize data
        self.usage = 0
        self.last_read_bytes = 0
        self.last_write_bytes = 0
        self.last_time = time.time()
        self.update_disk_info()
        self.update_gauge()
        
        # Start update thread
        self.update_thread = threading.Thread(target=self.update_metrics, daemon=True)
        self.update_thread.start()
    
    def get_color(self, usage):
        if usage < 60:
            return '#00FF9D'  # Neon green
        elif usage < 80:
            return '#FFD700'  # Gold
        else:
            return '#FF4444'  # Bright red
    
    def format_bytes(self, bytes_value):
        gb = bytes_value / (1024**3)
        return f"{gb:.2f} GB"
    
    def format_speed(self, bytes_value):
        mb = bytes_value / (1024**2)
        return f"{mb:.2f} MB/s"
    
    def update_disk_info(self):
        # Get disk information for the main drive
        partitions = psutil.disk_partitions()
        main_partition = partitions[0]  # Usually the main drive
        
        # Update labels
        self.disk_name_label.config(text=f"Disk: {main_partition.device}")
        self.disk_type_label.config(text=f"Type: {main_partition.fstype}")
        self.disk_fs_label.config(text=f"File System: {main_partition.fstype}")
    
    def update_metrics(self):
        while True:
            # Get disk usage
            disk_usage = psutil.disk_usage('/')
            self.usage = disk_usage.percent
            
            # Update usage labels
            self.disk_usage_label.config(text=f"Disk Usage: {self.usage:.2f}%")
            self.total_space_label.config(text=f"Total Space: {self.format_bytes(disk_usage.total)}")
            self.used_space_label.config(text=f"Used Space: {self.format_bytes(disk_usage.used)}")
            self.free_space_label.config(text=f"Free Space: {self.format_bytes(disk_usage.free)}")
            
            # Get disk I/O
            current_time = time.time()
            time_diff = current_time - self.last_time
            
            disk_io = psutil.disk_io_counters()
            read_speed = (disk_io.read_bytes - self.last_read_bytes) / time_diff
            write_speed = (disk_io.write_bytes - self.last_write_bytes) / time_diff
            
            self.read_speed_label.config(text=f"Read Speed: {self.format_speed(read_speed)}")
            self.write_speed_label.config(text=f"Write Speed: {self.format_speed(write_speed)}")
            
            # Update last values
            self.last_read_bytes = disk_io.read_bytes
            self.last_write_bytes = disk_io.write_bytes
            self.last_time = current_time
            
            self.update_gauge()
            time.sleep(1)
    
    def update_gauge(self):
        # Clear previous plot
        self.ax.clear()
        
        # Create pie chart
        sizes = [self.usage, 100 - self.usage]
        colors = [self.get_color(self.usage), '#3D3D3D']  # Dark gray for unused portion
        
        # Draw the pie chart
        wedges, texts = self.ax.pie(sizes, 
                                   colors=colors,
                                   startangle=90,
                                   counterclock=False,
                                   wedgeprops=dict(width=0.3))
        
        # Add percentage text in the center
        self.ax.text(0, 0, f'{self.usage:.2f}%', 
                    ha='center', 
                    va='center', 
                    fontsize=20,
                    color=self.fg_color)
        
        # Set aspect ratio to be equal
        self.ax.axis('equal')
        
        # Remove labels
        self.ax.set_title('Disk Usage', color=self.accent_color)
        
        # Update canvas
        self.canvas.draw()