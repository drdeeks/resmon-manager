import psutil
import time
import logging
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from typing import List, Dict, Set, Tuple
import win32api
import win32con
import win32process

from config import (
    CRITICAL_PROCESSES, PROTECTED_PROCESSES, COMMON_UNNECESSARY_PROCESSES, MEMORY_THRESHOLD_MB,
    CPU_THRESHOLD_PERCENT, INACTIVE_TIME_THRESHOLD, MAX_DUPLICATE_INSTANCES
)

class ProcessScanner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cpu_history = defaultdict(list)
        self.last_scan_time = time.time()
        
    def get_all_processes(self) -> List[psutil.Process]:
        """Get all running processes with error handling"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'create_time', 'status']):
            try:
                processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return processes
    
    def find_suspended_processes(self) -> List[psutil.Process]:
        """Find processes that are suspended or stopped"""
        suspended = []
        for proc in self.get_all_processes():
            try:
                # Check for stopped, zombie, or dead processes
                status = proc.info['status']
                if status in [psutil.STATUS_STOPPED, psutil.STATUS_ZOMBIE, psutil.STATUS_DEAD]:
                    name = proc.info['name'].lower().strip()
                    if name and name not in CRITICAL_PROCESSES and name not in PROTECTED_PROCESSES:
                        suspended.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return suspended
    
    def find_duplicate_processes(self) -> Dict[str, List[psutil.Process]]:
        """Find processes with multiple instances running"""
        process_counts = defaultdict(list)
        
        for proc in self.get_all_processes():
            try:
                name = proc.info['name'].lower().strip()
                if name and name not in CRITICAL_PROCESSES and name not in PROTECTED_PROCESSES:
                    process_counts[name].append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Return only processes with more than the allowed number of instances
        duplicates = {}
        for name, procs in process_counts.items():
            if len(procs) > MAX_DUPLICATE_INSTANCES:
                duplicates[name] = procs[MAX_DUPLICATE_INSTANCES:]  # Keep only excess instances
        
        return duplicates
    
    def find_inactive_processes(self) -> List[psutil.Process]:
        """Find processes that have been inactive for a long time"""
        inactive = []
        current_time = time.time()
        
        for proc in self.get_all_processes():
            try:
                # Check if process has been created long ago and has low CPU usage
                create_time = proc.info['create_time']
                age = current_time - create_time
                
                if age > INACTIVE_TIME_THRESHOLD:
                    cpu_percent = proc.info['cpu_percent']
                    if cpu_percent < 1.0:  # Very low CPU usage
                        name = proc.info['name'].lower().strip()
                        if name and name not in CRITICAL_PROCESSES and name not in PROTECTED_PROCESSES:
                            inactive.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return inactive
    
    def find_unnecessary_processes(self) -> List[psutil.Process]:
        """Find processes that are commonly unnecessary"""
        unnecessary = []
        
        for proc in self.get_all_processes():
            try:
                name = proc.info['name'].lower().strip()
                if name and name in COMMON_UNNECESSARY_PROCESSES:
                    unnecessary.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return unnecessary
    
    def find_resource_heavy_processes(self) -> List[psutil.Process]:
        """Find processes consuming excessive resources"""
        resource_heavy = []
        
        for proc in self.get_all_processes():
            try:
                name = proc.info['name'].lower().strip()
                if name and name not in CRITICAL_PROCESSES and name not in PROTECTED_PROCESSES:
                    # Check memory usage
                    memory_mb = proc.info['memory_info'].rss / 1024 / 1024
                    
                    # Check CPU usage (average over time)
                    cpu_percent = proc.info['cpu_percent']
                    self.cpu_history[proc.pid].append(cpu_percent)
                    
                    # Keep only recent CPU measurements
                    if len(self.cpu_history[proc.pid]) > 10:
                        self.cpu_history[proc.pid] = self.cpu_history[proc.pid][-10:]
                    
                    avg_cpu = sum(self.cpu_history[proc.pid]) / len(self.cpu_history[proc.pid])
                    
                    if memory_mb > MEMORY_THRESHOLD_MB or avg_cpu > CPU_THRESHOLD_PERCENT:
                        resource_heavy.append(proc)
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return resource_heavy
    
    def get_process_details(self, proc: psutil.Process) -> Dict:
        """Get detailed information about a process"""
        try:
            with proc.oneshot():
                memory_mb = proc.memory_info().rss / 1024 / 1024
                cpu_percent = proc.cpu_percent()
                create_time = datetime.fromtimestamp(proc.create_time())
                
                details = {
                    'pid': proc.pid,
                    'name': proc.name(),
                    'memory_mb': round(memory_mb, 2),
                    'cpu_percent': round(cpu_percent, 2),
                    'status': proc.status(),
                    'create_time': create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'cmdline': ' '.join(proc.cmdline()[:3]) if proc.cmdline() else 'N/A'  # First 3 args only
                }
                
                try:
                    details['username'] = proc.username()
                except (psutil.AccessDenied, OSError):
                    details['username'] = 'N/A'
                
                return details
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None
    
    def terminate_process(self, proc: psutil.Process, force: bool = False) -> bool:
        """Safely terminate a process"""
        try:
            name = proc.name().lower().strip()
            
            # Skip processes with empty or invalid names
            if not name or len(name) == 0:
                self.logger.info(f"Skipping process with empty name (PID: {proc.pid})")
                return False
            
            if name in CRITICAL_PROCESSES:
                self.logger.warning(f"Attempted to terminate critical process: {name}")
                return False
            
            if name in PROTECTED_PROCESSES:
                self.logger.info(f"Skipping protected process: {name} (requires elevated privileges)")
                return False
            
            self.logger.info(f"Terminating process: {proc.name()} (PID: {proc.pid})")
            
            if force:
                proc.kill()
            else:
                proc.terminate()
                
            # Wait for process to terminate
            try:
                proc.wait(timeout=5)
                return True
            except psutil.TimeoutExpired:
                # Force kill if graceful termination failed
                proc.kill()
                proc.wait(timeout=3)
                return True
                
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
            self.logger.error(f"Failed to terminate process {proc.pid}: {e}")
            return False
    
    def scan_all(self) -> Dict[str, List]:
        """Perform a comprehensive scan of all process types"""
        self.logger.info("Starting comprehensive process scan...")
        
        results = {
            'suspended': self.find_suspended_processes(),
            'duplicates': self.find_duplicate_processes(),
            'inactive': self.find_inactive_processes(),
            'unnecessary': self.find_unnecessary_processes(),
            'resource_heavy': self.find_resource_heavy_processes()
        }
        
        # Convert duplicate dict to list for consistency
        duplicate_list = []
        for name, procs in results['duplicates'].items():
            duplicate_list.extend(procs)
        results['duplicates'] = duplicate_list
        
        total_issues = sum(len(procs) for procs in results.values())
        self.logger.info(f"Scan completed. Found {total_issues} potential issues.")
        
        return results 