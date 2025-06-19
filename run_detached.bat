@echo off
cd /d "%~dp0"
echo Resource Monitor Scanner - Detached Launch
echo ===========================================
echo Launching application independently...
echo.

REM Try different Python commands
if exist "%LocalAppData%\Programs\Python\*\python.exe" (
    for /d %%i in ("%LocalAppData%\Programs\Python\*") do (
        if exist "%%i\python.exe" (
            echo Found Python at %%i\python.exe
            "%%i\python.exe" detached_launcher.py %*
            goto :end
        )
    )
)

REM Try py launcher first (most reliable on Windows)
py detached_launcher.py %*
if %ERRORLEVEL% EQU 0 goto :end

REM Try system Python
python detached_launcher.py %*
if %ERRORLEVEL% EQU 0 goto :end

REM Try python3
python3 detached_launcher.py %*
if %ERRORLEVEL% EQU 0 goto :end

echo.
echo ERROR: Python not found or not working!
echo Please install Python from https://python.org
echo Make sure to add Python to PATH during installation.
echo.
echo Alternatively, try running directly:
echo py detached_launcher.py
echo or
echo python detached_launcher.py
echo.
pause

:end
echo.
echo Press any key to close this launcher window...
timeout /t 3 >nul
echo You can now close this window safely. 