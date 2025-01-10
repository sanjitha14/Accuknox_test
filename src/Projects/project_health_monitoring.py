#monitoring health of CPU
import psutil
import logging
from datetime import datetime

# Configuration for logging
logging.basicConfig(
    filename='system_health.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Thresholds for alerts
CPU_THRESHOLD = 80.0  # in percentage
MEMORY_THRESHOLD = 80.0  # in percentage
DISK_THRESHOLD = 80.0  # in percentage
PROCESS_THRESHOLD = 300  # max running processes

def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        logging.warning(f"High CPU usage detected: {cpu_usage}%")
    else:
        logging.info(f"CPU usage is normal: {cpu_usage}%")

def check_memory_usage():
    memory = psutil.virtual_memory()
    if memory.percent > MEMORY_THRESHOLD:
        logging.warning(f"High Memory usage detected: {memory.percent}%")
    else:
        logging.info(f"Memory usage is normal: {memory.percent}%")

def check_disk_space():
    disk_usage = psutil.disk_usage('/')
    if disk_usage.percent > DISK_THRESHOLD:
        logging.warning(f"Low Disk space available: {disk_usage.percent}% used")
    else:
        logging.info(f"Disk space usage is normal: {disk_usage.percent}% used")

def check_running_processes():
    process_count = len(psutil.pids())
    if process_count > PROCESS_THRESHOLD:
        logging.warning(f"High number of running processes: {process_count}")
    else:
        logging.info(f"Number of running processes is normal: {process_count}")

def main():
    logging.info("System Health Check Started")
    check_cpu_usage()
    check_memory_usage()
    check_disk_space()
    check_running_processes()
    logging.info("System Health Check Completed")

if __name__ == "__main__":
    main()
