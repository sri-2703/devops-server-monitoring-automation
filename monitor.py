import platform
import socket
import time
import psutil
import subprocess

def collect_system_metrics():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "hostname": socket.gethostname(),
        "os": platform.platform(),
        "cpu_percent": round(psutil.cpu_percent(interval=0.5), 2),
        "memory_percent": round(memory.percent, 2),
        "disk_percent": round(disk.percent, 2),
        "memory_used_mb": round(memory.used / 1024 / 1024, 2),
        "memory_total_mb": round(memory.total / 1024 / 1024, 2),
        "disk_free_gb": round(disk.free / 1024 / 1024 / 1024, 2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

def check_network(host="8.8.8.8"):
    command = ["ping", "-c", "1", "-W", "2", host]
    if platform.system().lower() == "windows":
        command = ["ping", "-n", "1", "-w", "2000", host]

    start = time.perf_counter()
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=4
        )
        latency = round((time.perf_counter() - start) * 1000, 2)
        return {"reachable": result.returncode == 0, "latency_ms": latency, "host": host}
    except (subprocess.TimeoutExpired, OSError):
        return {"reachable": False, "latency_ms": None, "host": host}
