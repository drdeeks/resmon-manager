# Resource Monitor Scanner - PowerShell Launcher
# Launches the application independently from the PowerShell window

param(
    [switch]$CLI,
    [switch]$Admin,
    [switch]$Help
)

if ($Help) {
    Write-Host "Resource Monitor Scanner - PowerShell Launcher" -ForegroundColor Green
    Write-Host "=================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  .\launch.ps1           # Launch GUI independently"
    Write-Host "  .\launch.ps1 -CLI      # Launch CLI mode"
    Write-Host "  .\launch.ps1 -Admin    # Launch with admin privileges"
    Write-Host "  .\launch.ps1 -Help     # Show this help"
    Write-Host ""
    Write-Host "The GUI mode will launch independently, allowing you to close"
    Write-Host "this PowerShell window without affecting the application."
    exit 0
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Host "Resource Monitor Scanner - PowerShell Launcher" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

if ($Admin) {
    Write-Host "Requesting administrator privileges..." -ForegroundColor Yellow
    
    if ($CLI) {
        Start-Process PowerShell -ArgumentList "-File `"$($MyInvocation.MyCommand.Path)`" -CLI" -Verb RunAs
    } else {
        Start-Process PowerShell -ArgumentList "-File `"$($MyInvocation.MyCommand.Path)`"" -Verb RunAs
    }
    exit 0
}

# Find Python executable
$pythonExe = $null
$pythonCommands = @("py", "python", "python3")

foreach ($cmd in $pythonCommands) {
    try {
        & $cmd --version 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $pythonExe = $cmd
            Write-Host "Found Python: $cmd" -ForegroundColor Green
            break
        }
    } catch {
        continue
    }
}

if (-not $pythonExe) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    if ($CLI) {
        Write-Host "Launching CLI mode..." -ForegroundColor Cyan
        & $pythonExe "detached_launcher.py" --cli
    } else {
        Write-Host "Launching GUI independently..." -ForegroundColor Cyan
        
        # Try pythonw first (no console window)
        $pythonwExe = $pythonExe -replace "python", "pythonw"
        try {
            Start-Process $pythonwExe -ArgumentList "main.py" -WindowStyle Hidden | Out-Null
            Write-Host "Application launched successfully!" -ForegroundColor Green
            Write-Host "You can now close this PowerShell window." -ForegroundColor Green
        } catch {
            # Fall back to detached launcher
            Write-Host "Falling back to detached launcher..." -ForegroundColor Yellow
            & $pythonExe "detached_launcher.py"
        }
    }
} catch {
    Write-Host "ERROR: Failed to launch application" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not $CLI) {
    Start-Sleep -Seconds 2
    Write-Host "PowerShell launcher completed." -ForegroundColor Green
} 