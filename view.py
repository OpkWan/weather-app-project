# model.py
"""
Weather App - Model Entry Point
MVC Architecture
"""

# view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import urllib.request
import io

class WeatherView:
    """Manages the GUI components"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("800x800")
        self.root.configure(bg='#1e1e2e')
        self.root.resizable(True, True)
        
        # Store weather icons
        self.icon_cache = {}
        
        # Create UI components
        self._create_widgets()
    
    def _create_widgets(self):
        """Create all GUI components"""
        
        # ===== Search Frame =====
        search_frame = tk.Frame(self.root, bg='#1e1e2e')
        search_frame.pack(pady=20, padx=20, fill='x')
        
        # City input
        self.city_entry = tk.Entry(
            search_frame,
            font=('Arial', 14),
            width=30,
            bg='#2d2d44',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=0
        )
        self.city_entry.pack(side='left', padx=(0, 10), ipady=8, ipadx=10)
        self.city_entry.insert(0, "Enter city name...")
        self.city_entry.bind('<FocusIn>', self._on_entry_click)
        self.city_entry.bind('<FocusOut>', self._on_focus_out)
        
        # Search button
        self.search_button = tk.Button(
            search_frame,
            text="Search",
            font=('Arial', 12, 'bold'),
            bg='#5865f2',
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.search_button.pack(side='left')
        
        # ===== Main Content Frame =====
        self.content_frame = tk.Frame(self.root, bg='#1e1e2e')
        self.content_frame.pack(fill='both', expand=True, padx=20)
        
        # ===== Current Weather Frame =====
        self.current_frame = tk.Frame(self.content_frame, bg='#2d2d44', relief='flat')
        self.current_frame.pack(fill='x', pady=(0, 20))
