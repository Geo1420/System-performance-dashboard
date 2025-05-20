import psutil
import time
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading

class RamDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("RAM Consumption Dashboard")
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
        
        # Create usage frame
        self.usage_frame = ttk.LabelFrame(self.main_frame, text="Current Usage")
        self.usage_frame.pack(fill=tk.X, pady=10)
        
        # Create detailed RAM information labels
        self.usage_label = ttk.Label(self.usage_frame, text="RAM Usage: 0%")
        self.usage_label.pack(pady=5)
        
        self.total_ram_label = ttk.Label(self.usage_frame, text="Total RAM: 0 GB")
        self.total_ram_label.pack(pady=2)
        
        self.used_ram_label = ttk.Label(self.usage_frame, text="Used RAM: 0 GB")
        self.used_ram_label.pack(pady=2)
        
        self.available_ram_label = ttk.Label(self.usage_frame, text="Available RAM: 0 GB")
        self.available_ram_label.pack(pady=2)
        
        # Create swap memory frame
        self.swap_frame = ttk.LabelFrame(self.main_frame, text="Swap Memory")
        self.swap_frame.pack(fill=tk.X, pady=10)
        
        self.swap_total_label = ttk.Label(self.swap_frame, text="Total Swap: 0 GB")
        self.swap_total_label.pack(pady=2)
        
        self.swap_used_label = ttk.Label(self.swap_frame, text="Used Swap: 0 GB")
        self.swap_used_label.pack(pady=2)
        
        self.swap_free_label = ttk.Label(self.swap_frame, text="Free Swap: 0 GB")
        self.swap_free_label.pack(pady=2)
        
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
    
    def update_metrics(self):
        while True:
            # Get RAM information
            ram = psutil.virtual_memory()
            self.usage = ram.percent
            
            # Update RAM labels
            self.usage_label.config(text=f"RAM Usage: {self.usage}%")
            self.total_ram_label.config(text=f"Total RAM: {self.format_bytes(ram.total)}")
            self.used_ram_label.config(text=f"Used RAM: {self.format_bytes(ram.used)}")
            self.available_ram_label.config(text=f"Available RAM: {self.format_bytes(ram.available)}")
            
            # Get swap information
            swap = psutil.swap_memory()
            self.swap_total_label.config(text=f"Total Swap: {self.format_bytes(swap.total)}")
            self.swap_used_label.config(text=f"Used Swap: {self.format_bytes(swap.used)}")
            self.swap_free_label.config(text=f"Free Swap: {self.format_bytes(swap.free)}")
            
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
        self.ax.set_title('RAM Usage', color=self.accent_color)
        
        # Update canvas
        self.canvas.draw()