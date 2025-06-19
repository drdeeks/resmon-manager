#!/usr/bin/env python3
"""
Resource Monitor Scanner
A comprehensive Windows system resource monitoring and cleanup tool.

Features:
- Scans for suspended, duplicate, inactive, and unnecessary processes
- Manages Windows services
- Provides GUI interface for user interaction
- Exports detailed reports
- Automatic cleanup functionality
"""

import sys
import os
import logging
import argparse
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_logging(log_level='INFO', log_file=None):
    """Setup logging configuration"""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

def run_cli_scan():
    """Run a command-line scan without GUI"""
    print("Resource Monitor Scanner - CLI Mode")
    print("=" * 50)
    
    try:
        from process_scanner import ProcessScanner
        from service_manager import ServiceManager
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        return
    
    # Initialize scanner
    scanner = ProcessScanner()
    service_manager = ServiceManager()
    
    print("Scanning processes...")
    results = scanner.scan_all()
    
    print("\nScan Results:")
    print("-" * 30)
    
    total_issues = 0
    for process_type, processes in results.items():
        count = len(processes)
        total_issues += count
        print(f"{process_type.title().replace('_', ' ')}: {count} processes")
        
        if count > 0 and count <= 10:  # Show details for small lists
            for proc in processes:
                details = scanner.get_process_details(proc)
                if details:
                    print(f"  - {details['name']} (PID: {details['pid']}, Memory: {details['memory_mb']}MB)")
    
    print(f"\nTotal issues found: {total_issues}")
    
    print("\nScanning services...")
    unnecessary_services = service_manager.find_unnecessary_services()
    print(f"Unnecessary running services: {len(unnecessary_services)}")
    
    for service in unnecessary_services[:10]:  # Show first 10
        print(f"  - {service['name']} ({service['display_name']})")
    
    print("\nScan completed. Use GUI mode for interactive management.")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Resource Monitor Scanner - Windows System Cleanup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Launch GUI interface
  python main.py --cli              # Run CLI scan only
  python main.py --log-file scan.log # Log to file
        """
    )
    
    parser.add_argument(
        '--cli', 
        action='store_true',
        help='Run in command-line mode (no GUI)'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Set logging level'
    )
    
    parser.add_argument(
        '--log-file',
        help='Log to file (default: console only)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Resource Monitor Scanner 1.0.1'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Resource Monitor Scanner")
    
    try:
        if args.cli:
            # Run CLI mode
            run_cli_scan()
        else:
            # Check if we're on Windows
            if os.name != 'nt':
                print("Warning: This tool is designed for Windows systems.")
                print("Some features may not work correctly on other platforms.")
            
            # Launch GUI
            print("Launching Resource Monitor Scanner GUI...")
            try:
                from resource_monitor_gui import ResourceMonitorGUI
                app = ResourceMonitorGUI()
                app.run()
            except ImportError as e:
                print(f"Error importing GUI: {e}")
                print("Falling back to CLI mode...")
                run_cli_scan()
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\nApplication stopped by user.")
    except ImportError as e:
        logger.error(f"Missing required dependency: {e}")
        print(f"Error: Missing required dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 