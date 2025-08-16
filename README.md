# PaxFlip V3 Professional

**Paxton Token to Flipper Zero Converter - Version 3**

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

PaxFlip V3 Professional is the latest version of our professional Paxton token converter, designed for authorized security testing and penetration testing scenarios. This streamlined version focuses on essential functionality with enhanced user experience.

**Version 3 Improvements:**
- **Enhanced Window Sizing** - Properly displays all GUI elements (1100x850)
- **Streamlined Interface** - Removed unnecessary sections for cleaner experience
- **Professional Branding** - Complete ISL branding throughout
- **Administrator Notifications** - Clear privilege requirements displayed

---

## ✨ Features

### 🎯 Core Functionality
- **Decimal to Hex Conversion** - Convert Paxton token numbers to 8-digit hex format
- **Flipper Zero Export** - Save tokens as .rfid files for direct import
- **Net2 Service Control** - Stop/start Net2ClientSvc service (requires admin)
- **Professional Interface** - Modern, card-based UI with ISL branding

### 🔧 Technical Features
- **EM4100 Format** - Compatible with Flipper Zero RFID emulation
- **File Preview** - Preview .rfid file content before saving
- **Clipboard Integration** - Copy hex codes directly to clipboard
- **Error Handling** - Comprehensive input validation and error messages
- **Responsive Design** - Properly sized window that displays all elements

### 🆕 Version 3 Enhancements
- **Optimized Window Size** - 1100x850 pixels for complete visibility
- **Clean Interface** - Removed FTDI USB reader and status sections
- **Administrator Alerts** - Clear notifications for privilege requirements
- **V3 Branding** - Updated titles, class names, and documentation

---

## 🚀 Quick Start

### Prerequisites
- **Windows 10/11**
- **Python 3.7 or higher**
- **Administrator privileges** (for Net2 service control)

### Installation
1. **Extract** all files to a folder on your Windows machine
2. **Right-click** `PaxFlip_V3.bat` → **"Run as administrator"**
3. The batch file will automatically install required Python packages
4. **PaxFlip V3 Professional** will launch automatically

### Usage
1. **Enter** a Paxton token number (decimal format)
2. **Click** "Convert to Hex" to generate the 8-digit hex code
3. **Enter** a name for your token
4. **Click** "Save as Flipper .rfid File" to export
5. **Import** the .rfid file to your Flipper Zero

---

## 📁 Package Contents

- **PaxFlip_V3.py** - Main application (Version 3)
- **PaxFlip_V3.bat** - One-click launcher with dependency checking
- **requirements_V3.txt** - Python package requirements
- **README_PaxFlip_V3.md** - This documentation file
- **isl_logo.jpg** - Intercom Services London logo

---

## 🎯 Version 3 Changes

### ✅ **What's New:**
- **Enhanced Window Size** - Increased from 900x650 to 1100x850
- **V3 Branding** - Updated titles, class names, and version references
- **Administrator Notifications** - Clear privilege requirement warnings
- **Streamlined Interface** - Removed unnecessary sections for focus

### ❌ **What's Removed:**
- FTDI USB reader functionality (streamlined for manual input)
- Status & information sections (cleaner interface)
- Complex USB communication code (simplified codebase)

### 🔧 **What's Improved:**
- Better window sizing for complete element visibility
- Enhanced error handling and user feedback
- Professional ISL branding throughout
- Cleaner, more focused user experience

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
- **Visual Indicator:** Warning displayed in interface

### Window Specifications
- **Size:** 1100x850 pixels
- **Resizable:** Yes
- **Centered:** Automatically centers on screen
- **Compatibility:** Works on 1920x1080 and higher resolutions

---

## 🆘 Support

### Common Issues
1. **"Not running as administrator"** - Right-click batch file → "Run as administrator"
2. **"Python not found"** - Install Python from https://python.org
3. **Service control fails** - Ensure running as administrator
4. **GUI elements cut off** - V3 fixes this with larger window size

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

### **Version 3.0** (Current)
- **Enhanced window sizing** - 1100x850 for complete visibility
- **Streamlined interface** - Removed unnecessary sections
- **V3 branding** - Updated throughout application
- **Administrator notifications** - Clear privilege requirements
- **Professional polish** - Enhanced user experience

### **Previous Versions**
- **v2.x** - Added FTDI USB reader support
- **v1.x** - Initial release with basic functionality

---

## 🎯 Use Cases

### **Professional Security Testing**
- Authorized penetration testing engagements
- Security assessments of access control systems
- Red team exercises with proper authorization
- Security research and development

### **Compatible Hardware**
- Flipper Zero RFID emulation
- EM4100 compatible readers
- Paxton access control systems
- Security testing equipment

---

*For the latest updates and full documentation, visit our GitHub repository: https://github.com/ISLKey/PaxFlip*

**PaxFlip V3 Professional - The definitive tool for professional Paxton token conversion and Flipper Zero integration.**

