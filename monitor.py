import psutil
import time
import os
import subprocess

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_gpu_usage():
    try:
        output = subprocess.check_output("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits", shell=True)
        return output.decode().strip() + "%"
    except Exception:
        return "N/A"

def monitor_system():
    try:
        while True:
            clear_console()
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            gpu_usage = get_gpu_usage()
            
            print(f"CPU Usage: {cpu_usage}%")
            print(f"RAM Usage: {ram_usage}%")
            print(f"Disk Usage: {disk_usage}%")
            print(f"GPU Usage: {gpu_usage}")
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_system()
