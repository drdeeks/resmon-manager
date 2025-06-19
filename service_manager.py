import win32service
import win32serviceutil
import win32api
import logging
from typing import List, Dict, Tuple
import time

from config import CRITICAL_SERVICES, UNNECESSARY_SERVICES

class ServiceManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def get_all_services(self) -> List[Dict]:
        """Get all Windows services with their status"""
        services = []
        try:
            # Connect to Service Control Manager
            scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ENUMERATE_SERVICE)
            
            # Enumerate all services
            service_list = win32service.EnumServicesStatus(scm)
            
            for service in service_list:
                try:
                    service_name = service[0]
                    display_name = service[1]
                    status = service[2]
                    
                    # Safely get PID if available
                    pid = None
                    if len(status) > 7 and status[7] != 0:
                        pid = status[7]
                    
                    service_info = {
                        'name': service_name,
                        'display_name': display_name,
                        'status': self._get_service_status_text(status[1]),
                        'start_type': self._get_start_type(service_name),
                        'pid': pid,
                        'is_critical': service_name.lower() in CRITICAL_SERVICES,
                        'is_unnecessary': service_name.lower() in UNNECESSARY_SERVICES
                    }
                    services.append(service_info)
                except (IndexError, TypeError) as e:
                    self.logger.warning(f"Failed to process service {service}: {e}")
                    continue
            
            win32service.CloseServiceHandle(scm)
            
        except Exception as e:
            self.logger.error(f"Failed to enumerate services: {e}")
            
        return services
    
    def _get_service_status_text(self, status_code: int) -> str:
        """Convert service status code to readable text"""
        status_map = {
            win32service.SERVICE_STOPPED: "Stopped",
            win32service.SERVICE_START_PENDING: "Start Pending",
            win32service.SERVICE_STOP_PENDING: "Stop Pending",
            win32service.SERVICE_RUNNING: "Running",
            win32service.SERVICE_CONTINUE_PENDING: "Continue Pending",
            win32service.SERVICE_PAUSE_PENDING: "Pause Pending",
            win32service.SERVICE_PAUSED: "Paused"
        }
        return status_map.get(status_code, "Unknown")
    
    def _get_start_type(self, service_name: str) -> str:
        """Get service start type"""
        try:
            scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)
            service_handle = win32service.OpenService(scm, service_name, win32service.SERVICE_QUERY_CONFIG)
            
            config = win32service.QueryServiceConfig(service_handle)
            start_type = config[1]
            
            start_type_map = {
                win32service.SERVICE_AUTO_START: "Automatic",
                win32service.SERVICE_BOOT_START: "Boot",
                win32service.SERVICE_DEMAND_START: "Manual",
                win32service.SERVICE_DISABLED: "Disabled",
                win32service.SERVICE_SYSTEM_START: "System"
            }
            
            win32service.CloseServiceHandle(service_handle)
            win32service.CloseServiceHandle(scm)
            
            return start_type_map.get(start_type, "Unknown")
            
        except Exception:
            return "Unknown"
    
    def find_unnecessary_services(self) -> List[Dict]:
        """Find services that are unnecessary and running"""
        unnecessary = []
        all_services = self.get_all_services()
        
        for service in all_services:
            if (service['is_unnecessary'] and 
                service['status'] == "Running" and 
                not service['is_critical']):
                unnecessary.append(service)
        
        return unnecessary
    
    def find_stopped_auto_services(self) -> List[Dict]:
        """Find automatic services that are stopped (might indicate issues)"""
        stopped_auto = []
        all_services = self.get_all_services()
        
        for service in all_services:
            if (service['start_type'] == "Automatic" and 
                service['status'] == "Stopped" and 
                not service['is_unnecessary']):
                stopped_auto.append(service)
        
        return stopped_auto
    
    def stop_service(self, service_name: str) -> bool:
        """Stop a Windows service"""
        try:
            if service_name.lower() in CRITICAL_SERVICES:
                self.logger.warning(f"Attempted to stop critical service: {service_name}")
                return False
            
            self.logger.info(f"Stopping service: {service_name}")
            
            # Open service control manager
            scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)
            
            # Open the service
            service_handle = win32service.OpenService(
                scm, service_name, 
                win32service.SERVICE_STOP | win32service.SERVICE_QUERY_STATUS
            )
            
            # Stop the service
            win32service.ControlService(service_handle, win32service.SERVICE_CONTROL_STOP)
            
            # Wait for service to stop
            timeout = 30  # seconds
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                status = win32service.QueryServiceStatus(service_handle)
                if status[1] == win32service.SERVICE_STOPPED:
                    break
                time.sleep(1)
            
            win32service.CloseServiceHandle(service_handle)
            win32service.CloseServiceHandle(scm)
            
            self.logger.info(f"Successfully stopped service: {service_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to stop service {service_name}: {e}")
            return False
    
    def start_service(self, service_name: str) -> bool:
        """Start a Windows service"""
        try:
            self.logger.info(f"Starting service: {service_name}")
            
            scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)
            service_handle = win32service.OpenService(
                scm, service_name,
                win32service.SERVICE_START | win32service.SERVICE_QUERY_STATUS
            )
            
            win32service.StartService(service_handle, None)
            
            # Wait for service to start
            timeout = 30
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                status = win32service.QueryServiceStatus(service_handle)
                if status[1] == win32service.SERVICE_RUNNING:
                    break
                time.sleep(1)
            
            win32service.CloseServiceHandle(service_handle)
            win32service.CloseServiceHandle(scm)
            
            self.logger.info(f"Successfully started service: {service_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start service {service_name}: {e}")
            return False
    
    def disable_service(self, service_name: str) -> bool:
        """Disable a Windows service"""
        try:
            if service_name.lower() in CRITICAL_SERVICES:
                self.logger.warning(f"Attempted to disable critical service: {service_name}")
                return False
            
            self.logger.info(f"Disabling service: {service_name}")
            
            scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)
            service_handle = win32service.OpenService(
                scm, service_name, win32service.SERVICE_CHANGE_CONFIG
            )
            
            # Change service to disabled
            win32service.ChangeServiceConfig(
                service_handle,
                win32service.SERVICE_NO_CHANGE,  # dwServiceType
                win32service.SERVICE_DISABLED,   # dwStartType
                win32service.SERVICE_NO_CHANGE,  # dwErrorControl
                None, None, 0, None, None, None, None
            )
            
            win32service.CloseServiceHandle(service_handle)
            win32service.CloseServiceHandle(scm)
            
            self.logger.info(f"Successfully disabled service: {service_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to disable service {service_name}: {e}")
            return False
    
    def get_service_details(self, service_name: str) -> Dict:
        """Get detailed information about a specific service"""
        try:
            scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_CONNECT)
            service_handle = win32service.OpenService(
                scm, service_name,
                win32service.SERVICE_QUERY_CONFIG | win32service.SERVICE_QUERY_STATUS
            )
            
            # Get service configuration
            config = win32service.QueryServiceConfig(service_handle)
            status = win32service.QueryServiceStatus(service_handle)
            
            details = {
                'name': service_name,
                'display_name': config[2],
                'binary_path': config[3],
                'start_type': self._get_start_type(service_name),
                'status': self._get_service_status_text(status[1]),
                'pid': status[7] if status[7] != 0 else None,
                'is_critical': service_name.lower() in CRITICAL_SERVICES,
                'is_unnecessary': service_name.lower() in UNNECESSARY_SERVICES
            }
            
            win32service.CloseServiceHandle(service_handle)
            win32service.CloseServiceHandle(scm)
            
            return details
            
        except Exception as e:
            self.logger.error(f"Failed to get service details for {service_name}: {e}")
            return {} 