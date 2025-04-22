import psutil
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class CpuDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Usage Dashboard")
        self.root.geometry("400x400")
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create usage frame
        self.usage_frame = ttk.LabelFrame(self.main_frame, text="Current Usage")
        self.usage_frame.pack(fill=tk.X, pady=10)
        
        # Create usage label
        self.usage_label = ttk.Label(self.usage_frame, text="CPU Usage: 0%")
        self.usage_label.pack(pady=5)
        
        # Create graph frame
        self.graph_frame = ttk.LabelFrame(self.main_frame, text="Usage Gauge")
        self.graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(4, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initialize and update gauge
        self.update_gauge()
    
    def get_color(self, usage):
        if usage < 60:
            return 'green'
        elif usage < 80:
            return 'yellow'
        else:
            return 'red'
    
    def update_gauge(self):
        # Get current CPU usage
        usage = psutil.cpu_percent()
        
        # Update usage label
        self.usage_label.config(text=f"CPU Usage: {usage}%")
        
        # Clear previous plot
        self.ax.clear()
        
        # Create pie chart
        sizes = [usage, 100 - usage]
        colors = [self.get_color(usage), 'lightgray']
        
        # Draw the pie chart
        wedges, texts = self.ax.pie(sizes, 
                                   colors=colors,
                                   startangle=90,
                                   counterclock=False,
                                   wedgeprops=dict(width=0.3))
        
        # Add percentage text in the center
        self.ax.text(0, 0, f'{usage}%', 
                    ha='center', 
                    va='center', 
                    fontsize=20)
        
        # Set aspect ratio to be equal
        self.ax.axis('equal')
        
        # Remove labels
        self.ax.set_title('CPU Usage')
        
        # Update canvas
        self.canvas.draw() 