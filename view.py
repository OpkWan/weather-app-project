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
        # City name label
        self.city_label = tk.Label(
            self.current_frame,
            text="",
            font=('Arial', 24, 'bold'),
            bg='#2d2d44',
            fg='white'
        )
        self.city_label.pack(pady=(20, 5))
        
        # Weather icon
        self.icon_label = tk.Label(self.current_frame, bg='#2d2d44')
        self.icon_label.pack()
        
        # Temperature
        self.temp_label = tk.Label(
            self.current_frame,
            text="",
            font=('Arial', 48, 'bold'),
            bg='#2d2d44',
            fg='#5865f2'
        )
        self.temp_label.pack()
        
        # Description
        self.desc_label = tk.Label(
            self.current_frame,
            text="",
            font=('Arial', 16),
            bg='#2d2d44',
            fg='#a0a0b0'
        )
        self.desc_label.pack(pady=(0, 10))
        
        # Details frame (humidity, wind, etc.)
        details_frame = tk.Frame(self.current_frame, bg='#2d2d44')
        details_frame.pack(pady=(10, 20))
        
        self.feels_like_label = self._create_detail_label(details_frame, "Feels like: --°C")
        self.humidity_label = self._create_detail_label(details_frame, "Humidity: --%")
        self.wind_label = self._create_detail_label(details_frame, "Wind: -- m/s")
        self.pressure_label = self._create_detail_label(details_frame, "Pressure: -- hPa")
        
        # ===== Forecast Frame =====
        forecast_label = tk.Label(
            self.content_frame,
            text="5-Day Forecast",
            font=('Arial', 18, 'bold'),
            bg='#1e1e2e',
            fg='white'
        )
        forecast_label.pack(anchor='w', pady=(0, 10))
        
        self.forecast_frame = tk.Frame(self.content_frame, bg='#1e1e2e')
        self.forecast_frame.pack(fill='x')
        
        # Create 5 forecast cards
        self.forecast_cards = []
        for i in range(5):
            card = self._create_forecast_card(self.forecast_frame)
            card.pack(side='left', padx=5, expand=True, fill='both')
            self.forecast_cards.append(card)
        
        # Loading indicator
        self.loading_label = tk.Label(
            self.root,
            text="Loading...",
            font=('Arial', 16),
            bg='#1e1e2e',
            fg='#5865f2'
        )