
# PaxFlip Professional - Clean Edition

**Paxton Token to Flipper Zero Converter**

---

## 🏢 Company Information

**Intercom Services London**  
Developed by Jamie Johnson (TriggerHappyMe)

**Contact Details:**
- **Address:** 3rd Floor 86-90 Paul Street, London EC2A 4NE
- **Phone:** 0207 856 0515
- **Email:** support@intercomserviceslondon.co.uk
- **Website:** www.intercomserviceslondon.co.uk
- **GitHub:** https://github.com/ISLKey/PaxFlip

---

## 📋 Overview

PaxFlip Professional Clean Edition is a streamlined version of the Paxton token converter, designed for professional security testing. This clean version focuses on the essential functionality:

- **Manual token input** and conversion
- **Net2 service control** (requires administrator privileges)
- **Flipper Zero file export** (.rfid format)
- **Professional ISL branding** throughout

---

## ✨ Features

### 🎯 Core Functionality
- **Decimal to Hex Conversion** - Convert Paxton token numbers to 8-digit hex format
- **Flipper Zero Export** - Save tokens as .rfid files for direct import
- **Net2 Service Control** - Stop/start Net2ClientSvc service
- **Professional Interface** - Clean, modern UI with ISL branding

### 🔧 Technical Features
- **EM4100 Format** - Compatible with Flipper Zero RFID emulation
- **File Preview** - Preview .rfid file content before saving
- **Clipboard Integration** - Copy hex codes directly to clipboard
- **Error Handling** - Comprehensive input validation and error messages

---

## 🚀 Quick Start

### Prerequisites
- **Windows 10/11**
- **Python 3.7 or higher**
- **Administrator privileges** (for Net2 service control)

### Installation
1. **Extract** all files to a folder on your Windows machine
2. **Right-click** `PaxFlip_Clean_ISL.bat` → **"Run as administrator"**
3. The batch file will automatically install required Python packages
4. **PaxFlip Professional** will launch automatically

### Usage
1. **Enter** a Paxton token number (decimal format)
2. **Click** "Convert to Hex" to generate the 8-digit hex code
3. **Enter** a name for your token
4. **Click** "Save as Flipper .rfid File" to export
5. **Import** the .rfid file to your Flipper Zero

---

## 📁 Package Contents

- **PaxFlip_Clean_ISL.py** - Main application (clean version)
- **PaxFlip_Clean_ISL.bat** - One-click launcher with dependency checking
- **requirements_clean.txt** - Python package requirements
- **README_Clean_ISL.md** - This documentation file
- **isl_logo.jpg** - Intercom Services London logo

---

## 🎯 Key Differences from Full Version

This **Clean Edition** removes:
- ❌ FTDI USB reader functionality
- ❌ Status & information sections
- ❌ Complex USB communication code

This **Clean Edition** includes:
- ✅ Manual token input and conversion
- ✅ Net2 service control with administrator note
- ✅ Flipper Zero file export
- ✅ Professional ISL branding
- ✅ Streamlined, focused interface

---

## 🔧 Technical Details

### Supported Token Format
- **Input:** Decimal numbers (e.g., 12345678)
- **Output:** 8-digit hex (e.g., 00BC614E)
- **Flipper Format:** Space-separated bytes (e.g., 00 BC 61 4E)

### File Format
```
Filetype: Flipper RFID key
Version: 1
Key type: EM4100
Data: 00 BC 61 4E
```

### Net2 Service Control
- **Service Name:** Net2ClientSvc
- **Purpose:** Prevents conflicts with Paxton software
- **Requirement:** Administrator privileges needed

---

## 🆘 Support

### Common Issues
1. **"Not running as administrator"** - Right-click batch file → "Run as administrator"
2. **"Python not found"** - Install Python from https://python.org
3. **Service control fails** - Ensure running as administrator

### Contact Support
- **Email:** support@intercomserviceslondon.co.uk
- **Phone:** 0207 856 0515
- **GitHub Issues:** https://github.com/ISLKey/PaxFlip/issues

---

## 📄 License & Legal

**Professional Security Testing Tool**

This software is designed for authorized security testing and research purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations.

**© 2024 Intercom Services London**  
**Developed by Jamie Johnson (TriggerHappyMe)**

---

## 🔄 Version History

- **v1.0** - Initial clean edition release
- **Features:** Manual input, Net2 service control, Flipper export
- **UI:** Professional ISL branding, streamlined interface
- **Requirements:** Administrator privileges note added

---

*For the latest updates and full documentation, visit our GitHub repository: https://github.com/ISLKey/PaxFlip*


