# Resource Monitor Scanner

A comprehensive Windows system resource monitoring and cleanup tool that helps identify and manage unnecessary processes and services to optimize system performance.

![Version](https://img.shields.io/badge/version-1.0.1-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

### 🔍 Process Management
- **Suspended Processes**: Detects processes that are suspended, stopped, or zombie
- **Duplicate Processes**: Identifies multiple instances of the same application (>3 instances)
- **Inactive Processes**: Finds long-running processes with minimal activity (>1 hour, low CPU)
- **Unnecessary Processes**: Locates commonly unnecessary applications (browsers, notepad, etc.)
- **Resource-Heavy Processes**: Identifies processes consuming excessive CPU (>80%) or memory (>500MB)

### ⚙️ Service Management
- **Service Scanning**: Lists all Windows services with detailed information
- **Unnecessary Services**: Identifies services that can be safely stopped
- **Service Control**: Start, stop, or disable services through the GUI
- **Critical Service Protection**: Prevents accidental modification of essential services

### 🖥️ User Interface
- **Tabbed Interface**: Separate tabs for processes, services, and logs
- **Real-time Monitoring**: Live updates of system status with threaded scanning
- **Interactive Controls**: Easy selection and management of processes/services
- **Detailed Logging**: Comprehensive activity logs with timestamps
- **Export Reports**: Generate JSON reports with scan results

### 🛡️ Safety Features
- **Whitelist Protection**: Critical system processes and services are protected
- **Confirmation Dialogs**: User confirmation required for all destructive actions
- **Graceful Termination**: Processes are terminated gracefully before force-killing
- **Error Handling**: Robust error handling with detailed logging and fallback modes

## 📋 Installation

### Prerequisites
- **Operating System**: Windows 10/11 (Windows 7/8 may work but are not officially supported)
- **Python**: 3.7 or higher (3.13+ recommended)
- **Privileges**: Administrator privileges (recommended for full functionality)

### Quick Start

**Option 1: Using the Batch File (Recommended)**
1. Download or clone this repository
2. Double-click `run.bat` - it will automatically detect Python and install dependencies
3. The GUI will launch automatically

**Option 2: Manual Installation**
1. Clone or download this repository:
   ```bash
   git clone https://github.com/drdeeks/resmon-manager.git
   cd resmon-manager
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

### Dependencies

The project uses the following Python packages (managed via `requirements.txt`):

```
psutil==5.9.8      # System and process monitoring
pywin32>=307       # Windows API access for service management
```

**Note**: `tkinter` is used for the GUI but is typically included with Python installations.

## 🚀 Usage

### Important Notes About Process Termination

**Expected Behavior**: Some processes may fail to terminate, and this is normal. The application includes:

- **Critical Process Protection**: System-essential processes are never terminated
- **Protected Process Recognition**: HP services, Windows authentication, and other protected processes are automatically skipped
- **Privilege Requirements**: Some processes require administrator privileges to terminate

**Termination Failures Are Normal For**:
- HP diagnostic services (DiagsCap.exe, SysInfoCap.exe, NetworkCap.exe, etc.)
- Windows authentication services (NgcIso.exe)
- Security and antivirus software (Windows Defender, Malwarebytes, etc.)
- System memory management (MemCompression)
- System services with dependencies
- Processes running with higher privileges

**These Are Now Automatically Skipped** to reduce error messages and focus on processes that can actually be managed.

### Running with Administrator Privileges

For better process termination success, use the admin launcher:

```bash
# Run with administrator privileges (recommended)
.\run_admin.bat

# Or standard mode
.\run.bat
```

### Independent vs Attached Launch Modes

**🔓 Independent Mode** (Recommended):
- Application runs independently of the command window
- You can close the command prompt after launch
- Uses `.\run_gui.bat` or `python detached_launcher.py`

**🔗 Attached Mode**:
- Application is tied to the command window
- Closing the command prompt will close the application
- Uses `.\run.bat` or `python main.py`

### GUI Mode (Recommended)

**Option 1: Detached GUI (Recommended - runs independently)**
```bash
# GUI that runs independently of the command window
.\run_gui.bat

# PowerShell launcher (alternative)
.\launch.ps1

# Or using the detached launcher directly
python detached_launcher.py
```

**Option 2: Standard GUI (tied to command window)**
```bash
# Using batch file (auto-detects Python)
.\run.bat

# Or directly with Python
python main.py
```

### Command Line Mode
```bash
# Quick CLI scan
.\run.bat --cli

# Or directly
python main.py --cli
```

### Launch Options Summary

| Launcher | Independent | Admin Support | Description |
|----------|-------------|---------------|-------------|
| `.\run_gui.bat` | ✅ Yes | ❌ No | **Recommended** - GUI runs independently |
| `.\launch.ps1` | ✅ Yes | ✅ Yes | PowerShell launcher with admin support |
| `.\run_admin.bat` | ❌ No | ✅ Yes | GUI with administrator privileges |
| `.\run_detached.bat` | ✅ Yes | ❌ No | Detached launcher for GUI/CLI |
| `.\run.bat` | ❌ No | ❌ No | Standard launcher (tied to console) |

### Command Line Options
```bash
python main.py [options]

Options:
  -h, --help            Show help message and exit
  --cli                 Run in command-line mode (no GUI)
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Set logging level (default: INFO)
  --log-file LOG_FILE   Log to specified file (default: console only)
  --version             Show version information

Examples:
  python main.py                    # Launch GUI interface
  python main.py --cli              # Run CLI scan only
  python main.py --log-file scan.log # Log to file
```

### PowerShell Launcher Options
```powershell
.\launch.ps1           # Launch GUI independently
.\launch.ps1 -CLI      # Launch CLI mode  
.\launch.ps1 -Admin    # Launch with admin privileges
.\launch.ps1 -Help     # Show help
```

## 🖥️ GUI Interface

### Process Tab
- **Process Types**: Toggle different categories of problematic processes
- **Process List**: Hierarchical view showing process details (PID, Memory, CPU, Status)
- **Actions**: Terminate selected processes, force kill, or refresh process list
- **Information**: Detailed process information including user, command line, and creation time

### Service Tab
- **Service Categories**: Groups services by Critical, Unnecessary, and Normal
- **Service List**: Detailed service information including status, start type, and PID
- **Actions**: Start, stop, disable, or refresh services
- **Safety**: Critical services are clearly marked and protected from modification

### Log Tab
- **Activity Log**: Real-time logging of all actions and events
- **Timestamps**: Detailed timestamps for all entries
- **Export**: Save logs to file for troubleshooting
- **Clear Function**: Option to clear log for readability

### Control Panel
- **Scan All**: Perform comprehensive system scan
- **Auto Clean**: Automatically clean unnecessary processes (with confirmation)
- **Export Report**: Generate detailed JSON report of findings
- **Status**: Current operation status display with progress indication

## ⚙️ Configuration

The `config.py` file contains customizable settings:

### Process Thresholds
```python
MEMORY_THRESHOLD_MB = 500          # Memory usage threshold (MB)
CPU_THRESHOLD_PERCENT = 80         # CPU usage threshold (%)
INACTIVE_TIME_THRESHOLD = 3600     # Inactivity threshold (seconds = 1 hour)
MAX_DUPLICATE_INSTANCES = 3        # Maximum allowed duplicate processes
```

### Safety Lists
- **CRITICAL_PROCESSES**: System processes that should never be terminated
- **CRITICAL_SERVICES**: Essential Windows services
- **COMMON_UNNECESSARY_PROCESSES**: Applications commonly safe to terminate
- **UNNECESSARY_SERVICES**: Services that can usually be stopped safely

## 🛡️ Safety Considerations

### What's Protected
- **Critical System Processes**: Core Windows processes (system, csrss.exe, winlogon.exe, etc.)
- **Security Software**: Windows Defender, Malwarebytes, and other antivirus/security processes
- **Protected Processes**: HP services, Windows authentication services, and other system-protected processes
- **Essential Services**: Windows services required for basic functionality (eventlog, rpcss, cryptsvc, etc.)
- **Current Application**: The scanner won't terminate itself

### What Gets Flagged
- **Multiple Browser Instances**: Chrome, Firefox, Edge with many tabs
- **Redundant Applications**: Multiple instances of the same program
- **Background Applications**: Applications running without user interaction
- **Resource Hogs**: Applications using >500MB RAM or >80% CPU
- **Inactive Processes**: Long-running processes with minimal recent activity

### Recommendations
1. **Review Before Action**: Always review the list before terminating processes
2. **Start Conservative**: Begin with "Unnecessary" processes only
3. **Save Work**: Ensure all important work is saved before cleanup
4. **Test Environment**: Try the tool in a test environment first
5. **Administrator Rights**: Run as administrator for full functionality

## 🔧 Troubleshooting

### Recent Fixes (v1.0.1)
- ✅ Fixed `STATUS_SUSPENDED` compatibility issue with newer psutil versions
- ✅ Fixed service enumeration "tuple index out of range" error
- ✅ Improved batch file Python detection and error handling
- ✅ Added proper error handling for service PID extraction

### Common Issues

**"Python not found" Error**
- Ensure Python is installed from [python.org](https://python.org)
- Use the `py` launcher: `py main.py` instead of `python main.py`
- The batch file should auto-detect most Python installations

**"Access Denied" Errors**
- Run the application as Administrator (right-click → "Run as administrator")
- Some system processes require elevated privileges

**"Module Not Found" Errors**
- Install dependencies: `pip install -r requirements.txt`
- Ensure you're using Python 3.7+
- Try: `py -m pip install -r requirements.txt`

**GUI Not Appearing**
- Check if tkinter is installed: `python -m tkinter`
- Try CLI mode: `python main.py --cli`
- Ensure you're not running in a headless environment

**Services Not Visible**
- Run as Administrator
- Check Windows service permissions
- Some services may be hidden or restricted

### Debug Logging
Enable detailed logging for troubleshooting:
```bash
python main.py --log-level DEBUG --log-file debug.log
```

## 📊 Export Reports

The tool can generate detailed JSON reports containing:
- Process scan results with full details (PID, memory, CPU, status)
- Service status and configuration
- Timestamp and system information
- Recommended actions and safety warnings
- Scan statistics and performance metrics

Reports are saved as `resource_monitor_report_YYYYMMDD_HHMMSS.json`

## 📁 Project Structure

```
ResourceMonitorManager/
├── main.py                    # Main application entry point
├── config.py                  # Configuration and safety lists
├── process_scanner.py         # Process scanning and management
├── service_manager.py         # Windows service management
├── resource_monitor_gui.py    # GUI interface implementation
├── detached_launcher.py       # Independent application launcher
├── requirements.txt           # Python dependencies
├── run.bat                    # Standard Windows batch launcher
├── run_gui.bat                # Independent GUI launcher (recommended)
├── run_admin.bat              # Administrator privilege launcher
├── run_detached.bat           # Detached process launcher
├── launch.ps1                 # PowerShell launcher script
├── .gitignore                 # Git ignore patterns
├── package-lock.json          # Package lockfile for consistency
├── README.md                  # This documentation
└── INSTALLATION.md            # Detailed installation guide
```

## 🔄 Package Management

This project uses standard Python package management:

- **requirements.txt**: Defines Python dependencies with version constraints
- **package-lock.json**: Ensures consistent dependency versions across environments
- **.gitignore**: Excludes temporary files, virtual environments, and build artifacts

To ensure consistent environments:
```bash
# Install exact versions
pip install -r requirements.txt

# Update dependencies (be careful)
pip install --upgrade -r requirements.txt
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please ensure any changes:
- Maintain the safety-first approach
- Include appropriate error handling
- Add tests for new functionality
- Update documentation as needed

### Development Setup
```bash
git clone [<repository-url](https://github.com/drdeeks/resmon-manager.git)
cd resmon-manager
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## ⚠️ Disclaimer

This tool modifies running processes and services on your system. While extensive safety measures are in place, the authors are not responsible for any system issues that may arise from its use. Always:
- Test in a non-production environment first
- Ensure you have system backups
- Review actions before executing them
- Run with appropriate privileges

## 📈 Version History

- **1.0.1** (2025-06-18):
  - Fixed psutil compatibility issues
  - Improved service enumeration reliability
  - Enhanced batch file Python detection
  - Added proper error handling and logging
  - Updated documentation and troubleshooting

- **1.0.0**: Initial release with full GUI and CLI support 
