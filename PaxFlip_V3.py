#!/usr/bin/env python3
"""
PaxFlip - Paxton Token to Flipper Zero Converter
Professional Edition

Intercom Services London
Developed by Jamie Johnson (TriggerHappyMe)

Contact:
3rd Floor 86-90 Paul Street
London EC2A 4NE
www.intercomserviceslondon.co.uk
support@intercomserviceslondon.co.uk
0207 856 0515

GitHub: https://github.com/ISLKey/PaxFlip
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyperclip
import subprocess
import os
import webbrowser
import re
from datetime import datetime

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class PaxFlipClean:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_colors()
        self.setup_variables()
        self.setup_ui()
        self.check_net2_service()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("PaxFlip Professional - Paxton Token to Flipper Zero Converter | Intercom Services London")
        self.root.geometry("1100x850")
        self.root.configure(bg='white')
        self.root.resizable(True, True)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1100 // 2)
        y = (self.root.winfo_screenheight() // 2) - (850 // 2)
        self.root.geometry(f"1100x850+{x}+{y}")
        
    def setup_colors(self):
        """Define the ISL color scheme"""
        self.colors = {
            'primary': '#FF6600',      # ISL Orange
            'primary_dark': '#E55A00',  # Darker orange for hover
            'secondary': '#F0F0F0',     # Light gray
            'text_primary': '#333333',  # Dark gray
            'text_secondary': '#666666', # Medium gray
            'success': '#28A745',       # Green
            'warning': '#FFC107',       # Yellow
            'danger': '#DC3545',        # Red
            'white': '#FFFFFF',
            'light_gray': '#F8F9FA'
        }
        
    def setup_variables(self):
        """Initialize variables"""
        # Current token data
        self.current_token_decimal = ""
        self.current_token_hex = ""
        
        # UI variables
        self.token_var = tk.StringVar()
        self.hex_var = tk.StringVar()
        self.flipper_name_var = tk.StringVar(value="Paxton_Token")
        self.service_status_var = tk.StringVar(value="Checking...")
        
    def setup_ui(self):
        """Create the user interface"""
        # Create main container with scrollbar
        main_container = tk.Frame(self.root, bg='white')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Content area with cards
        self.create_content_area(main_container)
        
    def create_header(self, parent):
        """Create the header section with company branding"""
        header_frame = tk.Frame(parent, bg='white')
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Logo and title section
        title_frame = tk.Frame(header_frame, bg='white')
        title_frame.pack(fill='x')
        
        # Load and display logo if available
        if PIL_AVAILABLE and os.path.exists('isl_logo.jpg'):
            try:
                logo_img = Image.open('isl_logo.jpg')
                logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(title_frame, image=self.logo_photo, bg='white')
                logo_label.pack(side='left', padx=(0, 20))
            except Exception:
                pass
        
        # Title and subtitle
        title_text_frame = tk.Frame(title_frame, bg='white')
        title_text_frame.pack(side='left', fill='x', expand=True)
        
        title_label = tk.Label(title_text_frame, text="PaxFlip Professional", 
                              font=('Arial', 28, 'bold'), 
                              fg=self.colors['primary'], bg='white')
        title_label.pack(anchor='w')
        
        subtitle_label = tk.Label(title_text_frame, 
                                 text="Paxton Token to Flipper Zero Converter",
                                 font=('Arial', 14), 
                                 fg=self.colors['text_secondary'], bg='white')
        subtitle_label.pack(anchor='w')
        
        # Company info
        company_frame = tk.Frame(header_frame, bg='white')
        company_frame.pack(fill='x', pady=(15, 0))
        
        company_label = tk.Label(company_frame, text="Intercom Services London",
                                font=('Arial', 16, 'bold'), 
                                fg=self.colors['primary'], bg='white')
        company_label.pack(anchor='w')
        
        dev_label = tk.Label(company_frame, text="Developed by Jamie Johnson (TriggerHappyMe)",
                            font=('Arial', 11), 
                            fg=self.colors['text_secondary'], bg='white')
        dev_label.pack(anchor='w')
        
        contact_label = tk.Label(company_frame, 
                                text="3rd Floor 86-90 Paul Street, London EC2A 4NE | Tel: 0207 856 0515 | Email: support@intercomserviceslondon.co.uk",
                                font=('Arial', 10), 
                                fg=self.colors['text_secondary'], bg='white')
        contact_label.pack(anchor='w')
        
        # Action buttons
        button_frame = tk.Frame(company_frame, bg='white')
        button_frame.pack(anchor='w', pady=(8, 0))
        
        website_btn = tk.Button(button_frame, text="🌐 Website", 
                               command=self.open_website,
                               bg=self.colors['primary'], fg='white',
                               font=('Arial', 10, 'bold'), relief='flat',
                               padx=12, pady=6)
        website_btn.pack(side='left', padx=(0, 10))
        
        github_btn = tk.Button(button_frame, text="📁 GitHub", 
                              command=self.open_github,
                              bg=self.colors['primary'], fg='white',
                              font=('Arial', 10, 'bold'), relief='flat',
                              padx=12, pady=6)
        github_btn.pack(side='left', padx=(0, 10))
        
        about_btn = tk.Button(button_frame, text="ℹ️ About", 
                             command=self.show_about,
                             bg=self.colors['primary'], fg='white',
                             font=('Arial', 10, 'bold'), relief='flat',
                             padx=12, pady=6)
        about_btn.pack(side='left')
        
        # Separator
        separator = tk.Frame(header_frame, height=2, bg=self.colors['secondary'])
        separator.pack(fill='x', pady=(20, 0))
        
    def create_content_area(self, parent):
        """Create the main content area"""
        # Description
        desc_label = tk.Label(parent, 
                             text="Convert Paxton tokens using manual input and export to Flipper Zero format.\\nConverts to 8-digit hex format and saves as .rfid files.",
                             font=('Arial', 12), fg=self.colors['text_secondary'], 
                             bg='white', justify='left')
        desc_label.pack(anchor='w', pady=(0, 25))
        
        # Two-column layout
        columns_frame = tk.Frame(parent, bg='white')
        columns_frame.pack(fill='both', expand=True)
        
        # Left column
        left_column = tk.Frame(columns_frame, bg='white')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Right column  
        right_column = tk.Frame(columns_frame, bg='white')
        right_column.pack(side='right', fill='both', expand=True, padx=(15, 0))
        
        # Create sections
        self.create_service_status_section(left_column)
        self.create_manual_input_section(left_column)
        
        self.create_output_section(right_column)
        self.create_flipper_export_section(right_column)
        
    def create_card_frame(self, parent, title):
        """Create a card-style frame"""
        card = tk.Frame(parent, bg='white', relief='solid', bd=1)
        card.pack(fill='x', pady=(0, 20))
        
        # Card header
        header = tk.Frame(card, bg=self.colors['light_gray'])
        header.pack(fill='x')
        
        title_label = tk.Label(header, text=title, font=('Arial', 13, 'bold'),
                              fg=self.colors['text_primary'], bg=self.colors['light_gray'])
        title_label.pack(anchor='w', padx=20, pady=12)
        
        # Card content
        content = tk.Frame(card, bg='white')
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        return content
        
    def create_service_status_section(self, parent):
        """Create Net2 service status section"""
        content = self.create_card_frame(parent, "Net2 Service Status")
        
        # Administrator requirement note
        admin_note = tk.Label(content, 
                             text="⚠️ Administrator privileges required for service control",
                             font=('Arial', 10, 'bold'), fg=self.colors['warning'],
                             bg='white')
        admin_note.pack(anchor='w', pady=(0, 10))
        
        # Service status display
        self.service_label = tk.Label(content, textvariable=self.service_status_var,
                                     font=('Arial', 11), fg=self.colors['warning'],
                                     bg='white', relief='solid', bd=1, padx=10, pady=8)
        self.service_label.pack(fill='x', pady=(0, 15))
        
        # Service control buttons
        service_buttons = tk.Frame(content, bg='white')
        service_buttons.pack(fill='x')
        
        self.stop_service_btn = tk.Button(service_buttons, text="Stop Net2 Service",
                                         command=self.stop_net2_service,
                                         bg=self.colors['danger'], fg='white',
                                         font=('Arial', 11, 'bold'), relief='flat',
                                         padx=15, pady=8)
        self.stop_service_btn.pack(side='left', padx=(0, 10))
        
        self.start_service_btn = tk.Button(service_buttons, text="Start Net2 Service",
                                          command=self.start_net2_service,
                                          bg=self.colors['success'], fg='white',
                                          font=('Arial', 11, 'bold'), relief='flat',
                                          padx=15, pady=8)
        self.start_service_btn.pack(side='left')
        
    def create_manual_input_section(self, parent):
        """Create manual input section"""
        content = self.create_card_frame(parent, "Manual Input")
        
        tk.Label(content, text="Paxton Token Number (Decimal):", 
                font=('Arial', 12, 'bold'), fg=self.colors['text_primary'], 
                bg='white').pack(anchor='w', pady=(0, 8))
        
        self.token_entry = tk.Entry(content, textvariable=self.token_var, 
                                   font=('Arial', 16), bg='white', 
                                   fg=self.colors['text_primary'],
                                   relief='solid', bd=1)
        self.token_entry.pack(fill='x', pady=(0, 20), ipady=10)
        
        convert_btn = tk.Button(content, text="Convert to Hex",
                               command=self.convert_token,
                               bg=self.colors['primary'], fg='white',
                               font=('Arial', 13, 'bold'), relief='flat',
                               padx=25, pady=12)
        convert_btn.pack(anchor='w')
        
    def create_output_section(self, parent):
        """Create output section"""
        content = self.create_card_frame(parent, "Output")
        
        tk.Label(content, text="Flipper Zero Hex Code (8 digits):", 
                font=('Arial', 12, 'bold'), fg=self.colors['text_primary'], 
                bg='white').pack(anchor='w', pady=(0, 8))
        
        self.hex_output = tk.Entry(content, textvariable=self.hex_var, 
                                  font=('Courier', 18, 'bold'), bg='white',
                                  fg=self.colors['primary'], relief='solid', bd=1,
                                  state='readonly')
        self.hex_output.pack(fill='x', pady=(0, 20), ipady=10)
        
        # Action buttons
        button_frame = tk.Frame(content, bg='white')
        button_frame.pack(fill='x')
        
        copy_btn = tk.Button(button_frame, text="Copy to Clipboard",
                            command=self.copy_to_clipboard,
                            bg=self.colors['success'], fg='white',
                            font=('Arial', 11, 'bold'), relief='flat',
                            padx=18, pady=10)
        copy_btn.pack(side='left')
        
        clear_btn = tk.Button(button_frame, text="Clear All",
                             command=self.clear_fields,
                             bg=self.colors['secondary'], fg=self.colors['text_primary'],
                             font=('Arial', 11), relief='flat',
                             padx=18, pady=10)
        clear_btn.pack(side='right')
        
    def create_flipper_export_section(self, parent):
        """Create Flipper Zero export section"""
        content = self.create_card_frame(parent, "Flipper Zero Export")
        
        tk.Label(content, text="Token Name (for .rfid file):", 
                font=('Arial', 12, 'bold'), fg=self.colors['text_primary'], 
                bg='white').pack(anchor='w', pady=(0, 8))
        
        self.token_name_entry = tk.Entry(content, textvariable=self.flipper_name_var,
                                        font=('Arial', 13), bg='white',
                                        fg=self.colors['text_primary'],
                                        relief='solid', bd=1)
        self.token_name_entry.pack(fill='x', pady=(0, 20), ipady=8)
        
        # Export buttons
        export_frame = tk.Frame(content, bg='white')
        export_frame.pack(fill='x')
        
        save_btn = tk.Button(export_frame, text="Save as Flipper .rfid File",
                            command=self.save_flipper_file,
                            bg=self.colors['primary'], fg='white',
                            font=('Arial', 12, 'bold'), relief='flat',
                            padx=18, pady=10)
        save_btn.pack(side='left')
        
        preview_btn = tk.Button(export_frame, text="Preview File Content",
                               command=self.preview_flipper_file,
                               bg=self.colors['secondary'], fg=self.colors['text_primary'],
                               font=('Arial', 11), relief='flat',
                               padx=18, pady=10)
        preview_btn.pack(side='right')

    # Core functionality methods
    def convert_token(self):
        """Convert decimal token number to 8-digit hex format"""
        try:
            # Get input value
            token_str = self.token_var.get().strip()
            
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
            self.hex_var.set(hex_value)
            
            # Auto-generate token name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.flipper_name_var.set(f"Paxton_Token_{timestamp}")
            
            messagebox.showinfo("Success", f"Converted {token_decimal} to {hex_value}\\nReady to save as Flipper file!")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid decimal number.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy hex output to clipboard"""
        hex_value = self.hex_var.get()
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
        self.token_var.set("")
        self.hex_var.set("")
        self.flipper_name_var.set("Paxton_Token")
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
    
    def save_flipper_file(self):
        """Save token as Flipper Zero .rfid file"""
        hex_value = self.hex_var.get()
        if not hex_value:
            messagebox.showwarning("No Data", "No hex value to save. Please convert a token first.")
            return
            
        token_name = self.flipper_name_var.get().strip()
        if not token_name:
            token_name = f"paxton_token_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.flipper_name_var.set(token_name)
            
        # Clean filename
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', token_name)
        
        filename = filedialog.asksaveasfilename(
            title="Save Flipper Zero RFID File",
            defaultextension=".rfid",
            filetypes=[("RFID files", "*.rfid"), ("All files", "*.*")],
            initialfile=f"{safe_name}.rfid"
        )
        
        if filename:
            try:
                content = self.generate_flipper_content(token_name, hex_value)
                
                with open(filename, 'w') as f:
                    f.write(content)
                    
                messagebox.showinfo("Success", f"Flipper Zero file saved successfully!\\n\\nFile: {filename}\\nToken: {self.current_token_decimal}\\nHex: {hex_value}")
                
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {e}")
    
    def preview_flipper_file(self):
        """Preview Flipper Zero file content"""
        hex_value = self.hex_var.get()
        if not hex_value:
            messagebox.showwarning("No Data", "No hex value to preview. Please convert a token first.")
            return
            
        try:
            token_name = self.flipper_name_var.get().strip() or "Preview_Token"
            content = self.generate_flipper_content(token_name, hex_value)
            
            # Show preview dialog
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Flipper Zero File Preview")
            preview_window.geometry("500x250")
            preview_window.configure(bg='white')
            
            tk.Label(preview_window, text="File Content Preview:", 
                    font=('Arial', 14, 'bold'), bg='white').pack(pady=15)
            
            text_widget = tk.Text(preview_window, height=10, font=('Courier', 11),
                                 bg=self.colors['light_gray'], relief='solid', bd=1)
            text_widget.pack(fill='both', expand=True, padx=25, pady=(0, 25))
            text_widget.insert(1.0, content)
            text_widget.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Preview Error", f"Failed to generate preview: {e}")
    
    def check_net2_service(self):
        """Check Net2 service status"""
        try:
            result = subprocess.run(['sc', 'query', 'Net2ClientSvc'], 
                                  capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                if 'RUNNING' in result.stdout:
                    self.service_status_var.set("Net2ClientSvc: RUNNING (may conflict with direct USB)")
                    self.service_label.config(fg=self.colors['warning'])
                else:
                    self.service_status_var.set("Net2ClientSvc: STOPPED (good for direct USB)")
                    self.service_label.config(fg=self.colors['success'])
            else:
                self.service_status_var.set("Net2ClientSvc: NOT FOUND")
                self.service_label.config(fg=self.colors['text_secondary'])
                
        except Exception:
            self.service_status_var.set("Net2ClientSvc: Unable to check status")
            self.service_label.config(fg=self.colors['text_secondary'])
    
    def stop_net2_service(self):
        """Stop Net2 service"""
        try:
            result = subprocess.run(['net', 'stop', 'Net2ClientSvc'], 
                                  capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Success", "Net2ClientSvc stopped successfully")
                self.check_net2_service()
            else:
                messagebox.showerror("Error", f"Failed to stop service: {result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error stopping service: {str(e)}")
    
    def start_net2_service(self):
        """Start Net2 service"""
        try:
            result = subprocess.run(['net', 'start', 'Net2ClientSvc'], 
                                  capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Success", "Net2ClientSvc started successfully")
                self.check_net2_service()
            else:
                messagebox.showerror("Error", f"Failed to start service: {result.stderr}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error starting service: {str(e)}")
    
    def open_website(self):
        """Open company website"""
        webbrowser.open("https://www.intercomserviceslondon.co.uk")
        
    def open_github(self):
        """Open GitHub repository"""
        webbrowser.open("https://github.com/ISLKey/PaxFlip")
        
    def show_about(self):
        """Show about dialog"""
        about_text = """PaxFlip Professional - Paxton Token to Flipper Zero Converter

Intercom Services London
Developed by Jamie Johnson (TriggerHappyMe)

Contact Information:
3rd Floor 86-90 Paul Street
London EC2A 4NE
United Kingdom

Phone: 0207 856 0515
Email: support@intercomserviceslondon.co.uk
Website: www.intercomserviceslondon.co.uk

GitHub: https://github.com/ISLKey/PaxFlip

This professional tool converts Paxton access control tokens to Flipper Zero compatible format.
Supports manual entry with complete .rfid file export.
"""
        messagebox.showinfo("About PaxFlip Professional", about_text)
    
    def on_closing(self):
        """Handle window closing"""
        self.root.destroy()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PaxFlipClean(root)
    root.mainloop()

if __name__ == "__main__":
    main()

