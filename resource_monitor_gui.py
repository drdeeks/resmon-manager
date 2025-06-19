import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import logging
from datetime import datetime
import json
import sys
import os

try:
    from process_scanner import ProcessScanner
    from service_manager import ServiceManager
except ImportError:
    print("Could not import scanner modules. Running in demo mode.")
    ProcessScanner = None
    ServiceManager = None

class ResourceMonitorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Resource Monitor Scanner")
        self.root.geometry("900x700")
        
        # Initialize components
        if ProcessScanner and ServiceManager:
            self.process_scanner = ProcessScanner()
            self.service_manager = ServiceManager()
        else:
            self.process_scanner = None
            self.service_manager = None
            
        self.setup_logging()
        
        # Data storage
        self.scan_results = {}
        
        # Create GUI
        self.create_widgets()
        
        # Initial scan if modules available
        if self.process_scanner:
            self.perform_scan()
    
    def setup_logging(self):
        """Setup logging for the GUI"""
        logging.basicConfig(level=logging.INFO)
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Process tab
        self.process_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.process_frame, text='Processes')
        self.create_process_tab()
        
        # Service tab
        self.service_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.service_frame, text='Services')
        self.create_service_tab()
        
        # Log tab
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text='Logs')
        self.create_log_tab()
        
        # Control buttons
        self.create_control_buttons()
    
    def create_process_tab(self):
        """Create the process monitoring tab"""
        # Process type selection
        type_frame = ttk.LabelFrame(self.process_frame, text="Process Types")
        type_frame.pack(fill='x', padx=5, pady=5)
        
        self.process_vars = {}
        process_types = ['suspended', 'duplicates', 'inactive', 'unnecessary', 'resource_heavy']
        
        for i, ptype in enumerate(process_types):
            var = tk.BooleanVar(value=True)
            self.process_vars[ptype] = var
            cb = ttk.Checkbutton(type_frame, text=ptype.replace('_', ' ').title(), variable=var)
            cb.grid(row=0, column=i, padx=5, pady=5, sticky='w')
        
        # Process list
        list_frame = ttk.LabelFrame(self.process_frame, text="Detected Processes")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Treeview for processes
        columns = ('Type', 'PID', 'Name', 'Memory (MB)', 'CPU %', 'Status', 'User')
        self.process_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(list_frame, orient='vertical', command=self.process_tree.yview)
        self.process_tree.configure(yscrollcommand=v_scroll.set)
        
        self.process_tree.pack(side='left', fill='both', expand=True)
        v_scroll.pack(side='right', fill='y')
        
        # Process action buttons
        action_frame = ttk.Frame(self.process_frame)
        action_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(action_frame, text="Terminate Selected", 
                  command=self.terminate_selected_processes).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Force Kill Selected", 
                  command=lambda: self.terminate_selected_processes(force=True)).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Refresh", 
                  command=self.perform_scan).pack(side='left', padx=5)
    
    def create_service_tab(self):
        """Create the service monitoring tab"""
        # Service list
        list_frame = ttk.LabelFrame(self.service_frame, text="Windows Services")
        list_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Treeview for services
        columns = ('Name', 'Display Name', 'Status', 'Start Type', 'Category')
        self.service_tree = ttk.Treeview(list_frame, columns=columns, show='tree headings')
        
        for col in columns:
            self.service_tree.heading(col, text=col)
            self.service_tree.column(col, width=150)
        
        # Scrollbars
        v_scroll2 = ttk.Scrollbar(list_frame, orient='vertical', command=self.service_tree.yview)
        self.service_tree.configure(yscrollcommand=v_scroll2.set)
        
        self.service_tree.pack(side='left', fill='both', expand=True)
        v_scroll2.pack(side='right', fill='y')
        
        # Service action buttons
        action_frame = ttk.Frame(self.service_frame)
        action_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(action_frame, text="Stop Selected", 
                  command=self.stop_selected_services).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Start Selected", 
                  command=self.start_selected_services).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Refresh Services", 
                  command=self.refresh_services).pack(side='left', padx=5)
    
    def create_log_tab(self):
        """Create the logging tab"""
        self.log_text = scrolledtext.ScrolledText(self.log_frame, wrap=tk.WORD, height=20)
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Clear log button
        ttk.Button(self.log_frame, text="Clear Log", 
                  command=lambda: self.log_text.delete(1.0, tk.END)).pack(pady=5)
    
    def create_control_buttons(self):
        """Create main control buttons"""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(control_frame, text="Scan All", 
                  command=self.perform_scan).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Auto Clean", 
                  command=self.auto_clean).pack(side='left', padx=5)
        ttk.Button(control_frame, text="Export Report", 
                  command=self.export_report).pack(side='left', padx=5)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready")
        self.status_label.pack(side='right', padx=5)
    
    def perform_scan(self):
        """Perform a comprehensive scan"""
        if not self.process_scanner:
            self.log_message("Scanner not available - dependencies not installed")
            return
            
        def scan_thread():
            try:
                self.update_status("Scanning processes...")
                self.scan_results = self.process_scanner.scan_all()
                self.root.after(0, self.update_process_display)
                self.root.after(0, lambda: self.update_status("Scan completed"))
                self.log_message("Process scan completed successfully")
            except Exception as e:
                self.log_message(f"Error during scan: {e}")
                self.root.after(0, lambda: self.update_status("Scan failed"))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def update_process_display(self):
        """Update the process tree view with scan results"""
        # Clear existing items
        for item in self.process_tree.get_children():
            self.process_tree.delete(item)
        
        if not self.scan_results:
            return
            
        # Add processes by type
        for process_type, processes in self.scan_results.items():
            if not self.process_vars.get(process_type, tk.BooleanVar(value=True)).get():
                continue
            
            # Create parent node for process type
            type_node = self.process_tree.insert('', 'end', text=f"{process_type.title()} ({len(processes)})")
            
            for proc in processes:
                if self.process_scanner:
                    details = self.process_scanner.get_process_details(proc)
                    if details:
                        values = (
                            process_type,
                            details['pid'],
                            details['name'],
                            details['memory_mb'],
                            details['cpu_percent'],
                            details['status'],
                            details['username']
                        )
                        self.process_tree.insert(type_node, 'end', values=values, tags=(process_type,))
    
    def refresh_services(self):
        """Refresh the service list"""
        if not self.service_manager:
            self.log_message("Service manager not available - dependencies not installed")
            return
            
        def refresh_thread():
            try:
                self.update_status("Refreshing services...")
                services = self.service_manager.get_all_services()
                self.root.after(0, lambda: self.update_service_display(services))
                self.root.after(0, lambda: self.update_status("Services refreshed"))
                self.log_message("Services refreshed successfully")
            except Exception as e:
                self.log_message(f"Error refreshing services: {e}")
                self.root.after(0, lambda: self.update_status("Refresh failed"))
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def update_service_display(self, services):
        """Update the service tree view"""
        # Clear existing items
        for item in self.service_tree.get_children():
            self.service_tree.delete(item)
        
        # Group services by category
        categories = {'Critical': [], 'Unnecessary': [], 'Normal': []}
        
        for service in services:
            if service.get('is_critical'):
                categories['Critical'].append(service)
            elif service.get('is_unnecessary'):
                categories['Unnecessary'].append(service)
            else:
                categories['Normal'].append(service)
        
        # Add services by category
        for category, service_list in categories.items():
            if not service_list:
                continue
            
            category_node = self.service_tree.insert('', 'end', text=f"{category} ({len(service_list)})")
            
            for service in service_list:
                values = (
                    service['name'],
                    service['display_name'],
                    service['status'],
                    service['start_type'],
                    category
                )
                self.service_tree.insert(category_node, 'end', values=values, tags=(category.lower(),))
    
    def terminate_selected_processes(self, force=False):
        """Terminate selected processes"""
        selected_items = self.process_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No processes selected")
            return
        
        if not self.process_scanner:
            messagebox.showerror("Error", "Process scanner not available")
            return
        
        if not messagebox.askyesno("Confirm", f"Are you sure you want to {'force kill' if force else 'terminate'} selected processes?"):
            return
        
        def terminate_thread():
            terminated_count = 0
            for item in selected_items:
                values = self.process_tree.item(item, 'values')
                if values and len(values) > 1:  # Skip category headers
                    try:
                        pid = int(values[1])
                        import psutil
                        proc = psutil.Process(pid)
                        if self.process_scanner.terminate_process(proc, force):
                            terminated_count += 1
                            self.log_message(f"Terminated process: {values[2]} (PID: {pid})")
                    except Exception as e:
                        self.log_message(f"Failed to terminate PID {values[1]}: {e}")
            
            self.log_message(f"Terminated {terminated_count} processes")
            self.root.after(1000, self.perform_scan)  # Refresh after 1 second
        
        threading.Thread(target=terminate_thread, daemon=True).start()
    
    def stop_selected_services(self):
        """Stop selected services"""
        selected_items = self.service_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No services selected")
            return
        
        if not self.service_manager:
            messagebox.showerror("Error", "Service manager not available")
            return
        
        if not messagebox.askyesno("Confirm", "Are you sure you want to stop selected services?"):
            return
        
        def stop_thread():
            stopped_count = 0
            for item in selected_items:
                values = self.service_tree.item(item, 'values')
                if values and len(values) > 0:  # Skip category headers
                    service_name = values[0]
                    if self.service_manager.stop_service(service_name):
                        stopped_count += 1
                        self.log_message(f"Stopped service: {service_name}")
            
            self.log_message(f"Stopped {stopped_count} services")
            self.root.after(1000, self.refresh_services)
        
        threading.Thread(target=stop_thread, daemon=True).start()
    
    def start_selected_services(self):
        """Start selected services"""
        selected_items = self.service_tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "No services selected")
            return
        
        if not self.service_manager:
            messagebox.showerror("Error", "Service manager not available")
            return
        
        def start_thread():
            started_count = 0
            for item in selected_items:
                values = self.service_tree.item(item, 'values')
                if values and len(values) > 0:
                    service_name = values[0]
                    if self.service_manager.start_service(service_name):
                        started_count += 1
                        self.log_message(f"Started service: {service_name}")
            
            self.log_message(f"Started {started_count} services")
            self.root.after(1000, self.refresh_services)
        
        threading.Thread(target=start_thread, daemon=True).start()
    
    def auto_clean(self):
        """Perform automatic cleanup"""
        if not self.process_scanner or not self.service_manager:
            messagebox.showerror("Error", "Scanner components not available")
            return
            
        if not messagebox.askyesno("Confirm", "This will automatically terminate unnecessary processes and stop unnecessary services. Continue?"):
            return
        
        def clean_thread():
            cleaned_processes = 0
            cleaned_services = 0
            
            # Clean processes
            if hasattr(self, 'scan_results') and self.scan_results:
                for process_type in ['unnecessary', 'inactive']:
                    if process_type in self.scan_results:
                        for proc in self.scan_results[process_type]:
                            if self.process_scanner.terminate_process(proc):
                                cleaned_processes += 1
            
            # Clean services
            unnecessary_services = self.service_manager.find_unnecessary_services()
            for service in unnecessary_services:
                if self.service_manager.stop_service(service['name']):
                    cleaned_services += 1
            
            self.log_message(f"Auto-clean completed: {cleaned_processes} processes, {cleaned_services} services")
            self.root.after(1000, self.perform_scan)
            self.root.after(1000, self.refresh_services)
        
        threading.Thread(target=clean_thread, daemon=True).start()
    
    def export_report(self):
        """Export scan results to a file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resource_monitor_report_{timestamp}.json"
            
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'scan_results': {},
                'services': []
            }
            
            # Convert process objects to serializable data
            if hasattr(self, 'scan_results') and self.scan_results:
                for process_type, processes in self.scan_results.items():
                    report_data['scan_results'][process_type] = []
                    for proc in processes:
                        if self.process_scanner:
                            details = self.process_scanner.get_process_details(proc)
                            if details:
                                report_data['scan_results'][process_type].append(details)
            
            # Add services if available
            if self.service_manager:
                report_data['services'] = self.service_manager.get_all_services()
            
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            messagebox.showinfo("Export", f"Report exported to {filename}")
            self.log_message(f"Report exported to {filename}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")
    
    def log_message(self, message):
        """Add a message to the log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        def update_log():
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
        
        self.root.after(0, update_log)
    
    def update_status(self, status):
        """Update the status label"""
        self.status_label.config(text=status)
    
    def run(self):
        """Start the GUI application"""
        # Show initial message
        if not self.process_scanner or not self.service_manager:
            self.log_message("Some dependencies are missing. Install requirements.txt for full functionality.")
        else:
            self.log_message("Resource Monitor Scanner started successfully")
            # Load initial data
            self.refresh_services()
        
        # Start the main loop
        self.root.mainloop()

if __name__ == "__main__":
    app = ResourceMonitorGUI()
    app.run() 