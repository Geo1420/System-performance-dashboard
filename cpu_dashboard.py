import psutil
import time
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import platform

class CpuDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Performance Dashboard")
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
        
        # Create CPU info frame
        self.info_frame = ttk.LabelFrame(self.main_frame, text="CPU Information")
        self.info_frame.pack(fill=tk.X, pady=10)
        
        # CPU Information labels
        self.cpu_name_label = ttk.Label(self.info_frame, text="CPU: Loading...")
        self.cpu_name_label.pack(pady=2)
        
        self.cpu_cores_label = ttk.Label(self.info_frame, text="Cores: Loading...")
        self.cpu_cores_label.pack(pady=2)
        
        self.cpu_freq_label = ttk.Label(self.info_frame, text="Frequency: Loading...")
        self.cpu_freq_label.pack(pady=2)
        
        # Create usage frame
        self.usage_frame = ttk.LabelFrame(self.main_frame, text="Current Usage")
        self.usage_frame.pack(fill=tk.X, pady=10)
        
        # CPU Usage labels
        self.cpu_usage_label = ttk.Label(self.usage_frame, text="CPU Usage: 0%")
        self.cpu_usage_label.pack(pady=2)
        
        self.cpu_per_core_frame = ttk.LabelFrame(self.usage_frame, text="Per Core Usage")
        self.cpu_per_core_frame.pack(fill=tk.X, pady=5)
        
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
        self.core_labels = []
        self.update_cpu_info()
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
    
    def update_cpu_info(self):
        # Get CPU information
        cpu_info = platform.processor()
        cpu_count = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        
        # Update labels
        self.cpu_name_label.config(text=f"CPU: {cpu_info}")
        self.cpu_cores_label.config(text=f"Cores: {cpu_count} Physical, {psutil.cpu_count()} Logical")
        self.cpu_freq_label.config(text=f"Frequency: {cpu_freq.current:.1f} MHz")
        
        # Create per-core usage labels
        for i in range(psutil.cpu_count()):
            label = ttk.Label(self.cpu_per_core_frame, text=f"Core {i}: 0%")
            label.pack(pady=1)
            self.core_labels.append(label)
    
    def update_metrics(self):
        while True:
            # Get CPU usage
            self.usage = psutil.cpu_percent()
            self.cpu_usage_label.config(text=f"CPU Usage: {self.usage}%")
            
            # Get per-core usage
            per_core = psutil.cpu_percent(percpu=True)
            for i, usage in enumerate(per_core):
                self.core_labels[i].config(text=f"Core {i}: {usage}%")
            
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
        self.ax.text(0, 0, f'{self.usage}%', 
                    ha='center', 
                    va='center', 
                    fontsize=20,
                    color=self.fg_color)
        
        # Set aspect ratio to be equal
        self.ax.axis('equal')
        
        # Remove labels
        self.ax.set_title('CPU Usage', color=self.accent_color)
        
        # Update canvas
        self.canvas.draw()