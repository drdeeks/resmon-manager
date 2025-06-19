@echo off
REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
    cd /d "%~dp0"
    goto :run_app
) else (
    echo Requesting administrator privileges...
    echo This will help terminate more processes successfully.
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~dpnx0\"' -Verb runAs"
    exit /b
)

:run_app
echo Resource Monitor Scanner (Administrator Mode)
echo ============================================
echo Current directory: %CD%

REM Try different Python commands
if exist "%LocalAppData%\Programs\Python\*\python.exe" (
    for /d %%i in ("%LocalAppData%\Programs\Python\*") do (
        if exist "%%i\python.exe" (
            echo Found Python at %%i\python.exe
            "%%i\python.exe" main.py %*
            goto :end
        )
    )
)

REM Try py launcher first (most reliable on Windows)
py main.py %*
if %ERRORLEVEL% EQU 0 goto :end

REM Try system Python
python main.py %*
if %ERRORLEVEL% EQU 0 goto :end

REM Try python3
python3 main.py %*
if %ERRORLEVEL% EQU 0 goto :end

echo.
echo ERROR: Python not found or not working!
echo Please install Python from https://python.org
echo Make sure to add Python to PATH during installation.
echo.
pause

:end
echo.
echo Application finished. Press any key to exit...
pause 