#!/usr/bin/env python3
"""
Enhanced Paxton Token to Flipper Zero Converter
Supports manual input, direct FTDI-based USB reader communication, and Flipper Zero file export
Based on analysis of Paxton AccessControl drivers
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyperclip
import serial
import serial.tools.list_ports
import threading
import time
import re
import subprocess
import os
from datetime import datetime

class PaxtonConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Paxton Token to Flipper Zero Converter")
        self.root.geometry("750x850")
        self.root.resizable(True, True)
        
        # FTDI/Serial reader variables
        self.serial_connection = None
        self.reader_thread = None
        self.reading_active = False
        self.available_ports = []
        self.ftdi_ports = []
        
        # Current token data
        self.current_token_decimal = ""
        self.current_token_hex = ""
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        self.refresh_ports()
        self.check_net2_service()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Enhanced Paxton Token to Flipper Zero Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                                text="Convert Paxton tokens using manual input or direct USB reader.\n"
                                     "Now supports FTDI-based communication and Flipper Zero file export.\n"
                                     "Converts to 8-digit hex format and saves as .rfid files.",
                                font=("Arial", 10),
                                justify=tk.CENTER)
        instructions.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Net2 Service Status
        service_frame = ttk.LabelFrame(main_frame, text="Net2 Service Status", padding="10")
        service_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.service_status_label = ttk.Label(service_frame, text="Checking Net2ClientSvc status...")
        self.service_status_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        service_btn_frame = ttk.Frame(service_frame)
        service_btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.stop_net2_btn = ttk.Button(service_btn_frame, text="Stop Net2 Service", 
                                       command=self.stop_net2_service)
        self.stop_net2_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.start_net2_btn = ttk.Button(service_btn_frame, text="Start Net2 Service", 
                                        command=self.start_net2_service)
        self.start_net2_btn.grid(row=0, column=1)
        
        # FTDI USB Reader section
        usb_frame = ttk.LabelFrame(main_frame, text="FTDI USB Reader (Direct Communication)", padding="10")
        usb_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Port selection
        port_frame = ttk.Frame(usb_frame)
        port_frame.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(port_frame, text="FTDI Port:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.port_var, width=20, state="readonly")
        self.port_combo.grid(row=0, column=1, padx=(0, 10))
        
        refresh_btn = ttk.Button(port_frame, text="Refresh", command=self.refresh_ports)
        refresh_btn.grid(row=0, column=2, padx=(0, 10))
        
        self.connect_btn = ttk.Button(port_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=3)
        
        # Reader status and settings
        self.status_label = ttk.Label(usb_frame, text="Status: Disconnected", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
        # Baud rate selection
        baud_frame = ttk.Frame(usb_frame)
        baud_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(baud_frame, text="Baud Rate:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        self.baud_var = tk.StringVar(value="9600")
        baud_combo = ttk.Combobox(baud_frame, textvariable=self.baud_var, width=10, 
                                 values=["9600", "19200", "38400", "57600", "115200"], state="readonly")
        baud_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Test communication button
        test_btn = ttk.Button(baud_frame, text="Test Communication", command=self.test_communication)
        test_btn.grid(row=0, column=2)
        
        # Manual Input section
        input_frame = ttk.LabelFrame(main_frame, text="Manual Input", padding="10")
        input_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(input_frame, text="Paxton Token Number (Decimal):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.token_entry = ttk.Entry(input_frame, font=("Courier", 12), width=25)
        self.token_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.token_entry.bind('<Return>', lambda e: self.convert_token())
        
        convert_btn = ttk.Button(input_frame, text="Convert to Hex", command=self.convert_token)
        convert_btn.grid(row=2, column=0, pady=(0, 5))
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Output", padding="10")
        output_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(output_frame, text="Flipper Zero Hex Code (8 digits):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.hex_output = ttk.Entry(output_frame, font=("Courier", 14, "bold"), width=25, state="readonly")
        self.hex_output.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        button_frame = ttk.Frame(output_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        copy_btn = ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.grid(row=0, column=0, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_fields)
        clear_btn.grid(row=0, column=1)
        
        # Flipper Zero Export section
        flipper_frame = ttk.LabelFrame(main_frame, text="Flipper Zero Export", padding="10")
        flipper_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Token name input
        ttk.Label(flipper_frame, text="Token Name (for Flipper file):").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.token_name_entry = ttk.Entry(flipper_frame, font=("Arial", 10), width=30)
        self.token_name_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.token_name_entry.insert(0, "Paxton_Token")
        
        # Export buttons
        export_btn_frame = ttk.Frame(flipper_frame)
        export_btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        save_flipper_btn = ttk.Button(export_btn_frame, text="Save as Flipper .rfid File", 
                                     command=self.save_flipper_file)
        save_flipper_btn.grid(row=0, column=0, padx=(0, 10))
        
        preview_btn = ttk.Button(export_btn_frame, text="Preview File Content", 
                                command=self.preview_flipper_file)
        preview_btn.grid(row=0, column=1)
        
        # Example section
        example_frame = ttk.LabelFrame(main_frame, text="Example & Info", padding="10")
        example_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        example_text = ttk.Label(example_frame, 
                                text="Example: 12345678 (decimal) → 00BC614E (hex) → Paxton_Token.rfid\n"
                                     "FTDI-based communication bypasses Net2 service requirements.\n"
                                     "Generated .rfid files can be imported directly to Flipper Zero.",
                                font=("Courier", 9),
                                foreground="blue",
                                justify=tk.CENTER)
        example_text.grid(row=0, column=0, sticky=tk.W)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        service_frame.columnconfigure(0, weight=1)
        service_btn_frame.columnconfigure(0, weight=1)
        usb_frame.columnconfigure(0, weight=1)
        port_frame.columnconfigure(1, weight=1)
        baud_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(0, weight=1)
        output_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(0, weight=1)
        flipper_frame.columnconfigure(0, weight=1)
        export_btn_frame.columnconfigure(0, weight=1)
    
    def check_net2_service(self):
        """Check the status of Net2ClientSvc"""
        try:
            result = subprocess.run(['sc', 'query', 'Net2ClientSvc'], 
                                  capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                if "RUNNING" in result.stdout:
                    self.service_status_label.config(text="Net2ClientSvc: RUNNING (may conflict with direct USB)", 
                                                   foreground="orange")
                    self.stop_net2_btn.config(state="normal")
                    self.start_net2_btn.config(state="disabled")
                elif "STOPPED" in result.stdout:
                    self.service_status_label.config(text="Net2ClientSvc: STOPPED (good for direct USB)", 
                                                   foreground="green")
                    self.stop_net2_btn.config(state="disabled")
                    self.start_net2_btn.config(state="normal")
                else:
                    self.service_status_label.config(text="Net2ClientSvc: Unknown state", foreground="gray")
            else:
                self.service_status_label.config(text="Net2ClientSvc: Not found or access denied", 
                                               foreground="gray")
                self.stop_net2_btn.config(state="disabled")
                self.start_net2_btn.config(state="disabled")
                
        except Exception as e:
            self.service_status_label.config(text=f"Error checking service: {str(e)}", foreground="red")
    
    def stop_net2_service(self):
        """Stop the Net2ClientSvc service"""
        try:
            result = subprocess.run(['sc', 'stop', 'Net2ClientSvc'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", "Net2ClientSvc stopped successfully.\nYou can now use direct USB communication.")
            else:
                messagebox.showerror("Error", f"Failed to stop Net2ClientSvc.\nYou may need to run as administrator.")
            self.check_net2_service()
        except Exception as e:
            messagebox.showerror("Error", f"Error stopping service: {str(e)}")
    
    def start_net2_service(self):
        """Start the Net2ClientSvc service"""
        try:
            result = subprocess.run(['sc', 'start', 'Net2ClientSvc'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", "Net2ClientSvc started successfully.")
            else:
                messagebox.showerror("Error", f"Failed to start Net2ClientSvc.\nYou may need to run as administrator.")
            self.check_net2_service()
        except Exception as e:
            messagebox.showerror("Error", f"Error starting service: {str(e)}")
    
    def refresh_ports(self):
        """Refresh the list of available COM ports, highlighting FTDI devices"""
        self.available_ports = []
        self.ftdi_ports = []
        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            port_info = f"{port.device}"
            if port.description:
                port_info += f" - {port.description}"
            
            self.available_ports.append(port_info)
            
            # Check if this is an FTDI device
            if any(keyword in port.description.upper() for keyword in ['FTDI', 'FT232', 'FT245']):
                self.ftdi_ports.append(port_info)
                port_info += " [FTDI]"
                self.available_ports[-1] = port_info
        
        self.port_combo['values'] = self.available_ports
        
        # Prefer FTDI ports
        if self.ftdi_ports:
            self.port_combo.set(self.ftdi_ports[0] + " [FTDI]")
        elif self.available_ports:
            self.port_combo.set(self.available_ports[0])
        else:
            self.port_combo.set("")
    
    def toggle_connection(self):
        """Connect or disconnect from the USB reader"""
        if self.serial_connection is None:
            self.connect_reader()
        else:
            self.disconnect_reader()
    
    def connect_reader(self):
        """Connect to the selected USB reader"""
        selected_port_info = self.port_var.get()
        if not selected_port_info:
            messagebox.showwarning("No Port Selected", "Please select a COM port first.")
            return
        
        # Extract just the port name (e.g., "COM3" from "COM3 - USB Serial Port [FTDI]")
        port_name = selected_port_info.split(' ')[0]
        baud_rate = int(self.baud_var.get())
        
        try:
            self.serial_connection = serial.Serial(
                port=port_name,
                baudrate=baud_rate,
                timeout=1,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            
            if self.serial_connection.is_open:
                self.reading_active = True
                self.reader_thread = threading.Thread(target=self.read_from_device, daemon=True)
                self.reader_thread.start()
                
                self.status_label.config(text=f"Status: Connected to {port_name} at {baud_rate} baud", 
                                       foreground="green")
                self.connect_btn.config(text="Disconnect")
                messagebox.showinfo("Connected", f"Successfully connected to {port_name}")
            else:
                raise serial.SerialException("Could not open port")
                
        except serial.SerialException as e:
            messagebox.showerror("Connection Error", f"Failed to connect to {port_name}:\n{str(e)}")
            self.serial_connection = None
    
    def test_communication(self):
        """Test communication with the connected reader"""
        if not self.serial_connection or not self.serial_connection.is_open:
            messagebox.showwarning("Not Connected", "Please connect to a reader first.")
            return
        
        try:
            # Send a test command (this would need to be determined from protocol analysis)
            # For now, just check if we can write to the port
            self.serial_connection.write(b'\x00')  # Null byte test
            messagebox.showinfo("Test Result", "Communication test sent. Check reader response.")
        except Exception as e:
            messagebox.showerror("Test Failed", f"Communication test failed: {str(e)}")
    
    def disconnect_reader(self):
        """Disconnect from the USB reader"""
        self.reading_active = False
        
        if self.serial_connection:
            self.serial_connection.close()
            self.serial_connection = None
        
        if self.reader_thread:
            self.reader_thread.join(timeout=2)
        
        self.status_label.config(text="Status: Disconnected", foreground="red")
        self.connect_btn.config(text="Connect")
    
    def read_from_device(self):
        """Read data from the USB reader in a separate thread"""
        buffer = ""
        
        while self.reading_active and self.serial_connection and self.serial_connection.is_open:
            try:
                if self.serial_connection.in_waiting > 0:
                    data = self.serial_connection.read(self.serial_connection.in_waiting).decode('utf-8', errors='ignore')
                    buffer += data
                    
                    # Look for complete lines or token patterns
                    lines = buffer.split('\n')
                    buffer = lines[-1]  # Keep incomplete line in buffer
                    
                    for line in lines[:-1]:
                        line = line.strip()
                        if line:
                            # Try to extract decimal number from the line
                            token_match = re.search(r'\b(\d{6,10})\b', line)
                            if token_match:
                                token_decimal = token_match.group(1)
                                # Update UI in main thread
                                self.root.after(0, self.process_scanned_token, token_decimal)
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except (serial.SerialException, UnicodeDecodeError) as e:
                self.root.after(0, self.handle_reader_error, str(e))
                break
    
    def process_scanned_token(self, token_decimal):
        """Process a token scanned from the USB reader"""
        try:
            # Update the input field
            self.token_entry.delete(0, tk.END)
            self.token_entry.insert(0, token_decimal)
            
            # Automatically convert
            self.convert_token()
            
            # Auto-generate token name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.token_name_entry.delete(0, tk.END)
            self.token_name_entry.insert(0, f"Paxton_Token_{timestamp}")
            
            # Show notification
            messagebox.showinfo("Token Scanned", f"Token {token_decimal} scanned and converted!\nReady to save as Flipper file.")
            
        except Exception as e:
            messagebox.showerror("Processing Error", f"Error processing scanned token: {str(e)}")
    
    def handle_reader_error(self, error_msg):
        """Handle errors from the USB reader"""
        messagebox.showerror("Reader Error", f"USB reader error: {error_msg}")
        self.disconnect_reader()
    
    def convert_token(self):
        """Convert decimal token number to 8-digit hex format"""
        try:
            # Get input value
            token_str = self.token_entry.get().strip()
            
            if not token_str:
                messagebox.showwarning("Input Error", "Please enter a token number.")
                return
            
            # Convert to integer
            token_decimal = int(token_str)
            
            if token_decimal < 0:
                messagebox.showerror("Input Error", "Token number must be positive.")
                return
            
            if token_decimal > 0xFFFFFFFF:  # 32-bit limit
                messagebox.showerror("Input Error", "Token number is too large (exceeds 32-bit limit).")
                return
            
            # Convert to hex and format to 8 digits with leading zeros
            hex_value = format(token_decimal, '08X')
            
            # Store current values
            self.current_token_decimal = token_str
            self.current_token_hex = hex_value
            
            # Update output field
            self.hex_output.config(state="normal")
            self.hex_output.delete(0, tk.END)
            self.hex_output.insert(0, hex_value)
            self.hex_output.config(state="readonly")
            
            # Show success message
            messagebox.showinfo("Success", f"Converted {token_decimal} to {hex_value}\nReady to use with Flipper Zero!")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid decimal number.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy hex output to clipboard"""
        hex_value = self.hex_output.get()
        if hex_value:
            try:
                pyperclip.copy(hex_value)
                messagebox.showinfo("Copied", f"Hex code '{hex_value}' copied to clipboard!")
            except:
                # Fallback if pyperclip fails
                self.root.clipboard_clear()
                self.root.clipboard_append(hex_value)
                messagebox.showinfo("Copied", f"Hex code '{hex_value}' copied to clipboard!")
        else:
            messagebox.showwarning("Nothing to Copy", "No hex code to copy. Please convert a token first.")
    
    def clear_fields(self):
        """Clear all input and output fields"""
        self.token_entry.delete(0, tk.END)
        self.hex_output.config(state="normal")
        self.hex_output.delete(0, tk.END)
        self.hex_output.config(state="readonly")
        self.token_name_entry.delete(0, tk.END)
        self.token_name_entry.insert(0, "Paxton_Token")
        self.current_token_decimal = ""
        self.current_token_hex = ""
        self.token_entry.focus()
    
    def format_hex_for_flipper(self, hex_string):
        """Format hex string for Flipper Zero RFID file (space-separated bytes)"""
        # Remove any existing spaces and ensure uppercase
        hex_clean = hex_string.replace(" ", "").upper()
        
        # Pad to 8 characters if needed
        hex_clean = hex_clean.zfill(8)
        
        # Convert to space-separated bytes (2 hex digits each)
        formatted = " ".join([hex_clean[i:i+2] for i in range(0, len(hex_clean), 2)])
        
        return formatted
    
    def generate_flipper_content(self, token_name, hex_data):
        """Generate Flipper Zero RFID file content"""
        formatted_hex = self.format_hex_for_flipper(hex_data)
        
        content = f"""Filetype: Flipper RFID key
Version: 1
Key type: EM4100
Data: {formatted_hex}
"""
        return content
    
    def preview_flipper_file(self):
        """Preview the Flipper Zero file content"""
        if not self.current_token_hex:
            messagebox.showwarning("No Data", "Please convert a token first.")
            return
        
        token_name = self.token_name_entry.get().strip()
        if not token_name:
            token_name = "Paxton_Token"
        
        content = self.generate_flipper_content(token_name, self.current_token_hex)
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Flipper Zero File Preview")
        preview_window.geometry("400x300")
        preview_window.resizable(False, False)
        
        # Preview text
        preview_frame = ttk.Frame(preview_window, padding="20")
        preview_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(preview_frame, text="Flipper Zero .rfid File Content:", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        text_widget = tk.Text(preview_frame, width=50, height=10, font=("Courier", 10))
        text_widget.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_widget.insert(tk.END, content)
        text_widget.config(state="disabled")
        
        # Info labels
        info_frame = ttk.Frame(preview_frame)
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(info_frame, text=f"Token Decimal: {self.current_token_decimal}", 
                 font=("Arial", 9)).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=f"Token Hex: {self.current_token_hex}", 
                 font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(info_frame, text=f"Formatted for Flipper: {self.format_hex_for_flipper(self.current_token_hex)}", 
                 font=("Arial", 9)).grid(row=2, column=0, sticky=tk.W)
        
        # Close button
        close_btn = ttk.Button(preview_frame, text="Close", command=preview_window.destroy)
        close_btn.grid(row=3, column=0, pady=(10, 0))
        
        preview_window.columnconfigure(0, weight=1)
        preview_window.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)
    
    def save_flipper_file(self):
        """Save token as Flipper Zero .rfid file"""
        if not self.current_token_hex:
            messagebox.showwarning("No Data", "Please convert a token first.")
            return
        
        token_name = self.token_name_entry.get().strip()
        if not token_name:
            token_name = "Paxton_Token"
        
        # Remove invalid filename characters
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', token_name)
        
        # Ask user where to save
        filename = filedialog.asksaveasfilename(
            title="Save Flipper Zero RFID File",
            defaultextension=".rfid",
            filetypes=[("Flipper RFID files", "*.rfid"), ("All files", "*.*")],
            initialvalue=f"{safe_name}.rfid"
        )
        
        if filename:
            try:
                content = self.generate_flipper_content(token_name, self.current_token_hex)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                messagebox.showinfo("Success", 
                                  f"Flipper Zero file saved successfully!\n\n"
                                  f"File: {os.path.basename(filename)}\n"
                                  f"Token: {self.current_token_decimal} → {self.current_token_hex}\n\n"
                                  f"You can now import this file to your Flipper Zero.")
                
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file:\n{str(e)}")
    
    def on_closing(self):
        """Handle application closing"""
        self.disconnect_reader()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = PaxtonConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()

