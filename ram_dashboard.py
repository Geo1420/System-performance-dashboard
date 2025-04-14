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
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create usage frame
        self.usage_frame = ttk.LabelFrame(self.main_frame, text="Current Usage")
        self.usage_frame.pack(fill=tk.X, pady=10)
        
        # Create usage label
        self.usage_label = ttk.Label(self.usage_frame, text="RAM Usage: 0%")
        self.usage_label.pack(pady=5)
        
        # Create graph frame
        self.graph_frame = ttk.LabelFrame(self.main_frame, text="Usage Gauge")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(4, 4))
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
            return 'green'
        elif usage < 80:
            return 'yellow'
        else:
            return 'red'
    
    def update_gauge(self):
        self.ax.clear()
        
        # Create pie chart
        sizes = [self.usage, 100 - self.usage]
        colors = [self.get_color(self.usage), 'lightgray']
        
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
                    fontsize=20)
        
        # Set aspect ratio to be equal
        self.ax.axis('equal')
        
        # Remove labels
        self.ax.set_title('RAM Usage')
        
        # Update canvas
        self.canvas.draw()
    
    def update_metrics(self):
        while True:
            self.usage = psutil.virtual_memory().percent
            self.usage_label.config(text=f"RAM Usage: {self.usage}%")
            self.update_gauge()
            time.sleep(1) 