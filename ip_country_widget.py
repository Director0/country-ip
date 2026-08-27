"""
Windows IP Country Widget
- Shows current IP country as flag icon and country name
- Black theme, rounded corners
- Stays in desktop corner
- 85% opacity when not hovered, 100% when hovered
- Fast connection test using ip-api.com
"""

import tkinter as tk
from tkinter import font
import requests
import threading
import json
import os

class IPCountryWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IP Country Widget")
        
        # Window configuration
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes('-topmost', True)  # Always on top
        self.root.configure(bg='#1a1a1a')
        
        # Set initial opacity to 85%
        self.root.attributes('-alpha', 0.85)
        
        # Get screen dimensions and position in bottom-right corner
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Widget dimensions
        self.widget_width = 200
        self.widget_height = 60
        
        # Position in bottom-right corner with padding
        padding = 20
        x = screen_width - self.widget_width - padding
        y = screen_height - self.widget_height - padding
        
        self.root.geometry(f"{self.widget_width}x{self.widget_height}+{x}+{y}")
        
        # Make widget click-through when not hovering (optional, commented out for interaction)
        # self.root.attributes('-transparentcolor', '#1a1a1a')
        
        # Track mouse hover state
        self.is_hovered = False
        
        # Create main frame with rounded appearance
        self.main_frame = tk.Frame(
            self.root, 
            bg='#1a1a1a',
            highlightthickness=0
        )
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create custom font
        self.text_font = font.Font(family="Segoe UI", size=14, weight="normal")
        
        # Flag label (emoji will be used as flag)
        self.flag_label = tk.Label(
            self.main_frame,
            text="🌐",
            font=font.Font(size=24),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        self.flag_label.pack(side=tk.LEFT, padx=(10, 5))
        
        # Country name label
        self.country_label = tk.Label(
            self.main_frame,
            text="Loading...",
            font=self.text_font,
            bg='#1a1a1a',
            fg='#ffffff'
        )
        self.country_label.pack(side=tk.LEFT, padx=(5, 10))
        
        # Bind mouse events for hover effect
        self.root.bind('<Enter>', self.on_enter)
        self.root.bind('<Leave>', self.on_leave)
        
        # Bind double-click to close
        self.root.bind('<Double-Button-1>', lambda e: self.root.quit())
        
        # Start IP detection in background thread
        self.detect_ip_country()
        
    def on_enter(self, event):
        """Handle mouse enter - set opacity to 100%"""
        self.is_hovered = True
        self.root.attributes('-alpha', 1.0)
        
    def on_leave(self, event):
        """Handle mouse leave - set opacity to 85%"""
        self.is_hovered = False
        self.root.attributes('-alpha', 0.85)
    
    def detect_ip_country(self):
        """Detect IP country using fast API"""
        def fetch_ip_info():
            try:
                # Use ip-api.com for fast response (no authentication required)
                response = requests.get('http://ip-api.com/json/', timeout=5)
                data = response.json()
                
                if data.get('status') == 'success':
                    country = data.get('country', 'Unknown')
                    country_code = data.get('countryCode', '')
                    
                    # Get flag emoji from country code
                    flag = self.get_flag_emoji(country_code)
                    
                    # Update UI in main thread
                    self.root.after(0, lambda: self.update_display(flag, country))
                else:
                    self.root.after(0, lambda: self.update_display("❓", "Unknown"))
                    
            except Exception as e:
                print(f"Error fetching IP info: {e}")
                self.root.after(0, lambda: self.update_display("❓", "Error"))
        
        # Run in background thread to not block UI
        thread = threading.Thread(target=fetch_ip_info, daemon=True)
        thread.start()
    
    def get_flag_emoji(self, country_code):
        """Convert country code to flag emoji"""
        if not country_code or len(country_code) != 2:
            return "🌐"
        
        # Convert country code to flag emoji
        # Regional indicator symbols start at U+1F1E6
        base = ord('🇦') - ord('A')
        flag = ""
        for char in country_code.upper():
            if 'A' <= char <= 'Z':
                flag += chr(base + ord(char))
        
        return flag if flag else "🌐"
    
    def update_display(self, flag, country):
        """Update the display with flag and country name"""
        self.flag_label.config(text=flag)
        self.country_label.config(text=country)
    
    def run(self):
        """Start the widget"""
        self.root.mainloop()


if __name__ == "__main__":
    widget = IPCountryWidget()
    widget.run()
