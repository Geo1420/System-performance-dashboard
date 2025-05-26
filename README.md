# 🖥️ System Performance Dashboard

A real-time system monitoring dashboard that displays CPU, RAM, Disk, and GPU performance metrics with a modern dark-themed interface.

## ✨ Features

- 📊 Real-time CPU usage monitoring (overall and per-core)
- 💾 RAM usage tracking
- 💿 Disk usage statistics
- 🎮 GPU performance monitoring (if available)
- 🎨 Modern dark-themed UI with interactive graphs
- 🔍 Per-core CPU usage visualization
- ℹ️ System information display

## 📋 Requirements

- 🐍 Python 3.6 or higher
- 🪟 Windows operating system (for GPU monitoring)

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/System-performance-dashboard.git
cd System-performance-dashboard
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
```

3. Activate the virtual environment:

- Windows:

```bash
venv\Scripts\activate
```

- Linux/Mac:

```bash
source venv/bin/activate
```

4. Install required packages:

```bash
pip install -r requirements.txt
```

## 📦 Required Packages

The following packages are required to run the application:

- 📈 psutil
- 🖼️ tkinter (usually comes with Python)
- 📊 matplotlib
- 🔢 numpy

You can install them manually using:

```bash
pip install psutil matplotlib numpy
```

## 💻 Usage

1. Run the main dashboard:

```bash
python main_dashboard.py
```

2. To run individual components:

- CPU Dashboard: `python cpu_dashboard.py`
- RAM Dashboard: `python ram_dashboard.py`
- Disk Dashboard: `python disk_dashboard.py`
- GPU Dashboard: `python gpu_dashboard.py`

## 🔍 Features in Detail

### 🖥️ CPU Dashboard

- 📊 Displays overall CPU usage
- 🔢 Shows per-core usage statistics
- ⚡ Real-time CPU frequency monitoring
- ℹ️ CPU information display (model, cores, etc.)

### 💾 RAM Dashboard

- 📈 Real-time memory usage monitoring
- 💽 Available and used memory display
- 📊 Memory usage trends

### 💿 Disk Dashboard

- 📊 Disk space usage monitoring
- ⚡ Read/Write speeds
- 🔍 Disk health information

### 🎮 GPU Dashboard

- 📊 GPU usage monitoring (if available)
- 💽 Memory usage
- 🌡️ Temperature monitoring
- 📈 Performance metrics

## 🔧 Troubleshooting

1. If you get a "No module named X" error:

   - ✅ Make sure you have activated the virtual environment
   - ✅ Verify that all required packages are installed
   - ✅ Try running `pip install -r requirements.txt` again

2. If the GPU dashboard doesn't work:
   - ✅ Verify that you have a compatible GPU
   - ✅ Check if you have the latest GPU drivers installed
   - ℹ️ The GPU monitoring feature is currently optimized for Windows systems

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
