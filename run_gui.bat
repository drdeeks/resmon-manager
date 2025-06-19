@echo off
cd /d "%~dp0"
echo Resource Monitor Scanner - GUI Mode
echo ====================================
echo Starting GUI application...

REM Try different Python commands with pythonw (no console window)
if exist "%LocalAppData%\Programs\Python\*\pythonw.exe" (
    for /d %%i in ("%LocalAppData%\Programs\Python\*") do (
        if exist "%%i\pythonw.exe" (
            echo Launching with %%i\pythonw.exe
            start "" "%%i\pythonw.exe" main.py
            echo Application launched! You can close this window.
            timeout /t 3 >nul
            exit /b 0
        )
    )
)

REM Try pyw launcher (GUI mode)
pyw main.py
if %ERRORLEVEL% EQU 0 (
    echo Application launched! You can close this window.
    timeout /t 3 >nul
    exit /b 0
)

REM Try py launcher with -w flag (no console)
py -w main.py
if %ERRORLEVEL% EQU 0 (
    echo Application launched! You can close this window.
    timeout /t 3 >nul
    exit /b 0
)

REM Try system pythonw
pythonw main.py
if %ERRORLEVEL% EQU 0 (
    echo Application launched! You can close this window.
    timeout /t 3 >nul
    exit /b 0
)

REM Fall back to detached launcher
echo Trying detached launcher...
py detached_launcher.py
if %ERRORLEVEL% EQU 0 goto :end

python detached_launcher.py
if %ERRORLEVEL% EQU 0 goto :end

echo.
echo ERROR: Could not launch GUI application!
echo Please ensure Python is installed with tkinter support.
echo.
echo You can try:
echo 1. py main.py         (normal mode)
echo 2. pythonw main.py    (no console)
echo 3. pyw main.py        (GUI mode)
echo.
pause

:end 