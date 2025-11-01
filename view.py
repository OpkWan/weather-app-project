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
        self.root.minsize(650, 800)
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
    def _create_detail_label(self, parent, text):
        """Create a styled detail label"""
        label = tk.Label(
            parent,
            text=text,
            font=('Arial', 12),
            bg='#2d2d44',
            fg='#a0a0b0'
        )
        label.pack(side='left', padx=15)
        return label
    
    def _create_forecast_card(self, parent):
        """Create a forecast card widget"""
        card_frame = tk.Frame(parent, bg='#2d2d44', relief='flat')
        
        date_label = tk.Label(card_frame, text="", font=('Arial', 10, 'bold'), 
                           bg='#2d2d44', fg='white')
        icon_label = tk.Label(card_frame, bg='#2d2d44')
        
        # Container for temperatures with labels
        temp_container = tk.Frame(card_frame, bg='#2d2d44')
        
        # Max temperature with label
        max_temp_frame = tk.Frame(temp_container, bg='#2d2d44')
        max_label = tk.Label(max_temp_frame, text="High: ", font=('Arial', 9), 
                           bg='#2d2d44', fg='#a0a0b0')
        max_temp_label = tk.Label(max_temp_frame, text="", font=('Arial', 12, 'bold'), 
                           bg='#2d2d44', fg='#ff6b6b')
        max_label.pack(side='left')
        max_temp_label.pack(side='left')
        max_temp_frame.pack()
        
        # Min temperature with label
        min_temp_frame = tk.Frame(temp_container, bg='#2d2d44')
        min_label = tk.Label(min_temp_frame, text="Low: ", font=('Arial', 9), 
                           bg='#2d2d44', fg='#a0a0b0')
        min_temp_label = tk.Label(min_temp_frame, text="", font=('Arial', 12, 'bold'), 
                           bg='#2d2d44', fg='#4dabf7')
        min_label.pack(side='left')
        min_temp_label.pack(side='left')
        min_temp_frame.pack()
        
        desc_label = tk.Label(card_frame, text="", font=('Arial', 9), 
                           bg='#2d2d44', fg='#a0a0b0', wraplength=100)
        
        date_label.pack(pady=(10, 5))
        icon_label.pack()
        temp_container.pack(pady=5)
        desc_label.pack(pady=(0, 10))
        
        # Store references as attributes of the frame
        card_frame.date_label = date_label
        card_frame.icon_label = icon_label
        card_frame.max_temp_label = max_temp_label
        card_frame.min_temp_label = min_temp_label
        card_frame.desc_label = desc_label
        
        return card_frame
    
    def _on_entry_click(self, event):
        """Clear placeholder text on focus"""
        if self.city_entry.get() == "Enter city name...":
            self.city_entry.delete(0, tk.END)
            self.city_entry.config(fg='white')
    
    def _on_focus_out(self, event):
        """Restore placeholder if empty"""
        if self.city_entry.get() == "":
            self.city_entry.insert(0, "Enter city name...")
            self.city_entry.config(fg='#a0a0b0')
    
    def show_loading(self):
        """Display loading indicator"""
        self.loading_label.place(relx=0.5, rely=0.5, anchor='center')
        self.root.update()
    
    def hide_loading(self):
        """Hide loading indicator"""
        self.loading_label.place_forget()
    
    def update_current_weather(self, weather_data):
        """Update UI with current weather data"""
        self.city_label.config(text=f"{weather_data['city']}, {weather_data['country']}")
        self.temp_label.config(text=f"{weather_data['temperature']}°C")
        self.desc_label.config(text=weather_data['description'])
        
        self.feels_like_label.config(text=f"Feels like: {weather_data['feels_like']}°C")
        self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        self.wind_label.config(text=f"Wind: {weather_data['wind_speed']} m/s")
        self.pressure_label.config(text=f"Pressure: {weather_data['pressure']} hPa")
        
        # Load weather icon
        self._load_weather_icon(weather_data['icon'], self.icon_label, size=(100, 100))
    
    def update_forecast(self, forecast_data):
        """Update UI with forecast data"""
        for i, (card_frame, day_data) in enumerate(zip(self.forecast_cards, forecast_data)):
            card_frame.date_label.config(text=day_data['date'])
            card_frame.max_temp_label.config(text=f"{day_data['temp_max']}°C")
            card_frame.min_temp_label.config(text=f"{day_data['temp_min']}°C")
            card_frame.desc_label.config(text=day_data['description'])
            
            # Load forecast icon
            self._load_weather_icon(day_data['icon'], card_frame.icon_label, size=(50, 50))
    
    def _load_weather_icon(self, icon_code, label_widget, size=(100, 100)):
        """Download and display weather icon"""
        if icon_code in self.icon_cache:
            label_widget.config(image=self.icon_cache[icon_code])
            return
        
        try:
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()
            
            image = Image.open(io.BytesIO(raw_data))
            image = image.resize(size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            self.icon_cache[icon_code] = photo
            label_widget.config(image=photo)
            label_widget.image = photo  # Keep reference
            
        except Exception as e:
            print(f"Error loading icon: {e}")
    
    def show_error(self, message):
        """Display error message"""
        messagebox.showerror("Error", message)
    
    def get_city_input(self):
        """Get city name from input field"""
        city = self.city_entry.get()
        return city if city != "Enter city name..." else ""
    
    def bind_search(self, callback):
        """Bind search button and Enter key to callback"""
        self.search_button.config(command=callback)
        self.city_entry.bind('<Return>', lambda e: callback())