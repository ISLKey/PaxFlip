@echo off
cd /d "%~dp0"

echo.
echo ===============================================
echo  PaxFlip Professional Edition - Clean Version
echo  Paxton Token to Flipper Zero Converter
echo.
echo  Intercom Services London
echo  Developed by Jamie Johnson (TriggerHappyMe)
echo ===============================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator - Full functionality available
) else (
    echo WARNING: Not running as administrator.
    echo Service control features may not work.
    echo For full functionality, right-click and "Run as administrator"
)

echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
python -c "import pyperclip" >nul 2>&1
if errorlevel 1 (
    echo Installing pyperclip...
    pip install pyperclip
)

python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo Installing Pillow...
    pip install pillow
)

REM Check if the Python script exists
if not exist "PaxFlip_Clean_ISL.py" (
    echo ERROR: PaxFlip_Clean_ISL.py not found in current directory
    echo Please ensure all files are in the same folder
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

echo.
echo Launching PaxFlip Professional Clean Edition...
echo.

REM Launch the application
python PaxFlip_Clean_ISL.py

if errorlevel 1 (
    echo.
    echo Application exited with an error.
    echo For support, contact: support@intercomserviceslondon.co.uk
    echo GitHub: https://github.com/ISLKey/PaxFlip
    echo.
    pause
)

