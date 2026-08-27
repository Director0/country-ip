import tkinter as tk
from tkinter import font
import requests

class IPCountryWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.85)
        
        # Get screen dimensions and position in bottom-right corner
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.widget_width = 300
        self.widget_height = 70
        x = screen_width - self.widget_width - 20
        y = screen_height - self.widget_height - 20
        self.root.geometry(f"{self.widget_width}x{self.widget_height}+{x}+{y}")
        
        # Variables
        self.country_name = "Loading..."
        self.country_code = ""
        self.ip_address = "..."
        self.is_russia = False
        
        # Create main canvas for liquid glass effect with rounded corners
        self.canvas = tk.Canvas(
            self.root, 
            width=self.widget_width, 
            height=self.widget_height, 
            bg='#0d0d0d', 
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw rounded rectangle background (liquid glass effect)
        self.draw_liquid_background()
        
        # Custom font
        try:
            self.text_font = font.Font(family="Segoe UI", size=12, weight="normal")
            self.ip_font = font.Font(family="Segoe UI", size=10, weight="normal")
        except:
            self.text_font = font.Font(family="Arial", size=12)
            self.ip_font = font.Font(family="Arial", size=10)
        
        # Flag label
        self.flag_label = tk.Label(
            self.root, 
            text="🌐", 
            fg='white', 
            bg='#1a1a2e',
            font=("Segoe UI Emoji", 20),
            cursor="fleur"
        )
        self.flag_label.place(x=15, y=25)
        
        # Country name label
        self.country_label = tk.Label(
            self.root,
            text=self.country_name,
            fg='white',
            bg='#1a1a2e',
            font=self.text_font,
            anchor='w',
            cursor="fleur"
        )
        self.country_label.place(x=55, y=20)
        
        # IP address label
        self.ip_label = tk.Label(
            self.root,
            text=self.ip_address,
            fg='#999999',
            bg='#1a1a2e',
            font=self.ip_font,
            anchor='w',
            cursor="fleur"
        )
        self.ip_label.place(x=55, y=42)
        
        # Status indicator canvas (right side)
        self.indicator_canvas = tk.Canvas(
            self.root, 
            width=20, 
            height=20, 
            bg='#1a1a2e', 
            highlightthickness=0,
            cursor="fleur"
        )
        self.indicator_canvas.place(x=self.widget_width - 35, y=25)
        
        # Draw initial indicator (gray while loading)
        self.draw_indicator('#666666')
        
        # Drag functionality
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Bind drag to all elements
        widgets = [self.canvas, self.flag_label, self.country_label, self.ip_label, self.indicator_canvas]
        for widget in widgets:
            widget.bind("<Button-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.do_drag)
        
        # Hover effects
        self.root.bind("<Enter>", self.on_enter)
        self.root.bind("<Leave>", self.on_leave)
        
        # Double-click to close
        self.root.bind("<Double-Button-1>", lambda e: self.root.quit())
        
        # Load IP data
        self.load_ip_data()
        
    def draw_liquid_background(self):
        """Draw a rounded rectangle with liquid glass effect"""
        r = 20  # Corner radius
        
        # Main background with gradient-like layers
        self.canvas.create_roundrect(5, 5, self.widget_width-5, self.widget_height-5, r, 
                                     fill='#1a1a2e', outline='')
        
        # Subtle inner glow
        self.canvas.create_roundrect(8, 8, self.widget_width-8, self.widget_height-8, r-2, 
                                     fill='#252538', outline='')
    
    def draw_indicator(self, color):
        """Draw a realistic glossy indicator with light effects"""
        self.indicator_canvas.delete("all")
        
        # Main circle
        self.indicator_canvas.create_oval(2, 2, 18, 18, outline='', fill=color)
        
        # Top-left highlight (glossy effect)
        self.indicator_canvas.create_oval(4, 4, 10, 10, outline='', fill='white', stipple='gray25')
        
        # Small bright highlight
        self.indicator_canvas.create_oval(5, 5, 8, 8, outline='', fill='white')
    
    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_start_x)
        y = self.root.winfo_y() + (event.y - self.drag_start_y)
        self.root.geometry(f"+{x}+{y}")
    
    def on_enter(self, event):
        self.root.attributes('-alpha', 1.0)
    
    def on_leave(self, event):
        self.root.attributes('-alpha', 0.85)
    
    def get_flag_emoji(self, country_code):
        """Convert country code to flag emoji using Unicode regional indicators"""
        if not country_code or len(country_code) != 2:
            return "🌐"
        
        # Convert country code to regional indicator symbols
        base = ord('🇦') - ord('A')
        flag = chr(base + ord(country_code[0].upper())) + chr(base + ord(country_code[1].upper()))
        return flag
    
    def load_ip_data(self):
        try:
            # Fast IP geolocation API
            response = requests.get('http://ip-api.com/json/', timeout=5)
            data = response.json()
            
            if data.get('status') == 'success':
                self.country_name = data.get('country', 'Unknown')
                self.country_code = data.get('countryCode', '')
                self.ip_address = data.get('query', 'Unknown')
                self.is_russia = self.country_code.upper() == 'RU'
                
                # Update UI
                flag = self.get_flag_emoji(self.country_code)
                self.flag_label.config(text=flag)
                self.country_label.config(text=self.country_name)
                self.ip_label.config(text=self.ip_address)
                
                # Update indicator color
                if self.is_russia:
                    self.draw_indicator('#ff3333')  # Red for Russia
                else:
                    self.draw_indicator('#33ff33')  # Green for others
            else:
                self.country_label.config(text="API Error")
                self.ip_label.config(text="Failed to fetch")
                self.draw_indicator('#ffaa00')  # Yellow for error
                
        except Exception as e:
            self.country_label.config(text="Connection Error")
            self.ip_label.config(text=str(e)[:20])
            self.draw_indicator('#ff3333')  # Red for error

# Add rounded rectangle support to Canvas
def create_roundrect(self, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

tk.Canvas.create_roundrect = create_roundrect

if __name__ == "__main__":
    app = IPCountryWidget()
    app.root.mainloop()
