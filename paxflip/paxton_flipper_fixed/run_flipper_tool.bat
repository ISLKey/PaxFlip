@echo off
title Enhanced Paxton Token Converter with Flipper Export
echo Starting Enhanced Paxton Token to Flipper Zero Converter...
echo Now with Flipper Zero .rfid file export support!
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import pyperclip, serial" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements_enhanced.txt
    if errorlevel 1 (
        echo ERROR: Failed to install required packages.
        echo Please run 'pip install pyperclip pyserial' manually.
        echo.
        pause
        exit /b 1
    )
)

REM Check for administrator rights (needed for service control)
net session >nul 2>&1
if errorlevel 1 (
    echo.
    echo WARNING: Not running as administrator.
    echo Service control features may not work.
    echo For full functionality, right-click and "Run as administrator"
    echo.
    timeout /t 3 >nul
)

REM Run the enhanced application with Flipper export
echo Launching Enhanced Paxton Token Converter with Flipper Export...
python paxton_tool_with_flipper_export.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
)

