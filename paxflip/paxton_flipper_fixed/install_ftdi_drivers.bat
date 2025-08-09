@echo off
title Install FTDI Drivers for Paxton USB Reader
echo Installing FTDI Drivers for Paxton USB Reader...
echo.

REM Check for administrator rights
net session >nul 2>&1
if errorlevel 1 (
    echo ERROR: Administrator rights required to install drivers.
    echo Please right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

REM Check if FtdiDrivers folder exists
if not exist "FtdiDrivers" (
    echo ERROR: FtdiDrivers folder not found.
    echo Please extract the complete AccessControl.zip file first.
    echo The FtdiDrivers folder should be in the same directory as this script.
    echo.
    pause
    exit /b 1
)

echo Found FtdiDrivers folder. Installing drivers...
echo.

REM Install FTDI drivers using pnputil
echo Installing FTDI USB Bus driver...
pnputil /add-driver "FtdiDrivers\ftdibus.inf" /install

if errorlevel 1 (
    echo.
    echo WARNING: Driver installation may have failed.
    echo This could be because:
    echo 1. Drivers are already installed
    echo 2. Windows blocked the installation
    echo 3. Incompatible driver version
    echo.
    echo You can also install drivers manually:
    echo 1. Connect your Paxton USB reader
    echo 2. Open Device Manager
    echo 3. Right-click on the unknown device
    echo 4. Select "Update driver"
    echo 5. Browse to the FtdiDrivers folder
    echo.
) else (
    echo.
    echo SUCCESS: FTDI drivers installed successfully!
    echo.
    echo Next steps:
    echo 1. Connect your Paxton USB reader
    echo 2. Wait for Windows to recognize the device
    echo 3. Check Device Manager for "USB Serial Port" under "Ports (COM & LPT)"
    echo 4. Run the enhanced Paxton tool
    echo.
)

pause

