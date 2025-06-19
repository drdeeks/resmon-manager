#!/usr/bin/env python3
"""
Detached launcher for Resource Monitor Scanner
Allows the GUI application to run independently of the console window
"""

import sys
import os
import subprocess
import platform

def launch_detached_gui():
    """Launch the GUI application detached from the console"""
    
    # Get the path to main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, 'main.py')
    
    # Find Python executable
    python_exe = sys.executable
    if not python_exe:
        # Try common Python locations
        possible_pythons = ['python', 'py', 'python3']
        for py_cmd in possible_pythons:
            try:
                subprocess.run([py_cmd, '--version'], 
                             capture_output=True, text=True, timeout=5, check=True)
                python_exe = py_cmd
                break
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        if not python_exe:
            print("Error: Could not find Python executable")
            return False
    
    try:
        if platform.system() == 'Windows':
            # On Windows, use CREATE_NEW_PROCESS_GROUP and DETACHED_PROCESS
            # to completely detach from the parent console
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            DETACHED_PROCESS = 0x00000008
            
            subprocess.Popen(
                [python_exe, main_script],
                creationflags=CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS,
                close_fds=True,
                cwd=script_dir
            )
        else:
            # On Unix-like systems, use nohup equivalent
            subprocess.Popen(
                [python_exe, main_script],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                preexec_fn=os.setpgrp if hasattr(os, 'setpgrp') else None,
                cwd=script_dir
            )
        
        print("Resource Monitor Scanner launched successfully!")
        print("The application is now running independently.")
        print("You can safely close this command window.")
        return True
        
    except Exception as e:
        print(f"Error launching application: {e}")
        return False

def launch_detached_cli():
    """Launch the CLI application detached from the console"""
    
    # Get the path to main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, 'main.py')
    
    # Find Python executable
    python_exe = sys.executable
    if not python_exe:
        python_exe = 'python'
    
    try:
        if platform.system() == 'Windows':
            # For CLI, we still want to see output, so just detach the process
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            
            # Wait for the process to complete
            subprocess.run(
                [python_exe, main_script, '--cli'],
                creationflags=CREATE_NEW_PROCESS_GROUP,
                cwd=script_dir
            )
        else:
            # On Unix-like systems
            subprocess.run([python_exe, main_script, '--cli'], cwd=script_dir)
        
        return True
        
    except Exception as e:
        print(f"Error launching CLI application: {e}")
        return False

def main():
    """Main entry point for detached launcher"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Detached launcher for Resource Monitor Scanner"
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Launch in CLI mode'
    )
    
    args = parser.parse_args()
    
    if args.cli:
        success = launch_detached_cli()
    else:
        success = launch_detached_gui()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main() 