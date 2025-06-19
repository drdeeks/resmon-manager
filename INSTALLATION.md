# Installation Guide - Resource Monitor Scanner

## Prerequisites

### 1. Install Python
1. Download Python from [https://python.org](https://python.org)
2. **IMPORTANT**: During installation, check "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing: `python --version`

### 2. Install Dependencies
Open Command Prompt in the project directory and run:
```bash
pip install -r requirements.txt
```

Required packages:
- `psutil` - For system and process monitoring
- `pywin32` - For Windows API access and service management

## Quick Start

### Option 1: Using the Batch File (Recommended)
Simply double-click `run.bat` or run it from Command Prompt:
```bash
run.bat
```

For command-line mode:
```bash
run.bat --cli
```

### Option 2: Direct Python Execution
```bash
python main.py          # GUI mode
python main.py --cli     # CLI mode
```

## Running as Administrator

For full functionality (especially service management), run as Administrator:

1. Right-click `run.bat` → "Run as administrator"
2. Or open Command Prompt as Administrator and run the commands

## Troubleshooting

### "Python not found" Error
- Ensure Python is installed and added to PATH
- Try `py` instead of `python`
- Reinstall Python with "Add to PATH" option checked

### "Module not found" Error
- Run: `pip install -r requirements.txt`
- Ensure you're in the correct directory

### "Access Denied" Errors
- Run as Administrator
- Some system processes require elevated privileges

### GUI Not Appearing
- Check if tkinter is installed: `python -m tkinter`
- Try CLI mode: `python main.py --cli`

## System Requirements

- Windows 7/8/10/11
- Python 3.7 or higher
- Administrator privileges (recommended)
- At least 100MB free disk space

## Features Overview

### Process Management
- ✅ Detects suspended processes
- ✅ Identifies duplicate instances
- ✅ Finds inactive processes
- ✅ Locates unnecessary applications
- ✅ Identifies resource-heavy processes

### Service Management
- ✅ Lists all Windows services
- ✅ Identifies unnecessary services
- ✅ Start/stop services
- ✅ Protects critical services

### Safety Features
- ✅ Critical process protection
- ✅ Confirmation dialogs
- ✅ Detailed logging
- ✅ Export reports

## Usage Tips

1. **Start with CLI mode** to understand what the tool detects
2. **Always review** before terminating processes
3. **Save your work** before running cleanup
4. **Run as Administrator** for full functionality
5. **Export reports** for record keeping

## Support

If you encounter issues:
1. Check this installation guide
2. Review the main README.md
3. Check the logs tab in the GUI
4. Run in CLI mode for detailed error messages 