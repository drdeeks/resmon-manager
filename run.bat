@echo off
cd /d "%~dp0"
echo Resource Monitor Scanner
echo ========================
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
echo Alternatively, try running directly:
echo py main.py
echo or
echo python main.py
echo.
pause

:end 