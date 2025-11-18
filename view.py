# view.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import urllib.request
import io
import json
import os

class WeatherView:
    """Manages the GUI components"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("800x800")
        self.root.configure(bg='#1e1e2e')
        self.root.resizable(True, True)
        
        # Store weather icons and country flags
        self.icon_cache = {}
        self.flag_cache = {}
        
        # Search history file
        self.history_file = "search_history.json"
        self.search_history = self._load_search_history()
        
        # Loading animation
        self.loading_animation_id = None
        self.loading_angle = 0
        
        # Show splash screen first
        self._show_splash_screen()
        
    def _show_splash_screen(self):
        """Display splash screen on app start"""
        self.root.withdraw()
        self.splash = tk.Toplevel(self.root)
        self.splash.title("")
        self.splash.geometry("400x300")
        self.splash.configure(bg='#1e1e2e')
        self.splash.overrideredirect(True)
        self.splash.attributes('-topmost', True)
        
        # Center the splash screen
        self.splash.update_idletasks()
        x = (self.splash.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.splash.winfo_screenheight() // 2) - (300 // 2)
        self.splash.geometry(f"400x300+{x}+{y}")
        
        # Splash content
        title_label = tk.Label(
            self.splash,
            text="☀️ Weather App",
            font=('Arial', 32, 'bold'),
            bg='#1e1e2e',
            fg='#5865f2'
        )
        title_label.pack(pady=(80, 20))
        
        subtitle_label = tk.Label(
            self.splash,
            text="Loading...",
            font=('Arial', 14),
            bg='#1e1e2e',
            fg='#a0a0b0'
        )
        subtitle_label.pack()
        
        # Progress bar
        progress = ttk.Progressbar(
            self.splash,
            mode='indeterminate',
            length=300
        )
        progress.pack(pady=30)
        progress.start(10)
        
        # Close splash and show main window after 2 seconds
        self.root.after(2000, self._close_splash)
        
    def _close_splash(self):
        """Close splash and build + show the real UI."""
        self.splash.destroy()

        # build UI only once
        if not hasattr(self, 'ui_built'):
            self._create_widgets()
            self.ui_built = True

        # show main window on top
        self.root.deiconify()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(lambda: self.root.attributes('-topmost', False))
        self.root.focus_force()
        
    def _load_search_history(self):
        """Load search history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle old format (list of strings) and convert to new format
                    if data and isinstance(data[0], str):
                        from datetime import datetime
                        return [{'city': city, 'timestamp': datetime.now().isoformat(), 
                                'formatted_time': datetime.now().strftime('%b %d, %Y at %I:%M %p')} 
                               for city in data]
                    return data
            except Exception as e:
                print(f"Error loading history: {e}")
                return []
        return []
    
    def _save_search_history(self):
        """Save search history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.search_history[-10:], f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_to_history(self, city):
        """Add city to search history with timestamp"""
        from datetime import datetime
        if city:
            city = city.strip().title()
            # Check if city already exists and update timestamp
            for entry in self.search_history:
                if entry['city'] == city:
                    entry['timestamp'] = datetime.now().isoformat()
                    entry['formatted_time'] = datetime.now().strftime('%b %d, %Y at %I:%M %p')
                    self._save_search_history()
                    return
            # Add new entry
            self.search_history.append({
                'city': city,
                'timestamp': datetime.now().isoformat(),
                'formatted_time': datetime.now().strftime('%b %d, %Y at %I:%M %p')
            })
            self._save_search_history()
            self._update_history_dropdown()
    
    def _create_widgets(self):
        """Create all GUI components"""
        
        # ===== Search Frame =====
        search_frame = tk.Frame(self.root, bg='#1e1e2e', height=80)
        search_frame.pack(pady=20, fill='x')
        search_frame.pack_propagate(False)  # Maintain fixed height

        # Center container for search elements
        search_container = tk.Frame(search_frame, bg='#1e1e2e')
        search_container.place(relx=0.5, rely=0.5, anchor='center')

        # Input frame with entry and history button
        input_frame = tk.Frame(search_container, bg='#2d2d44', relief='solid', bd=1)
        input_frame.pack(side='left')
        
        self.city_entry = tk.Entry(
            input_frame,
            font=('Arial', 14),
            width=30,
            bg='#2d2d44',
            fg='white',
            insertbackground='white',
            relief='flat',
            bd=0
        )
        self.city_entry.pack(side='left', ipady=10, ipadx=10)
        self.city_entry.insert(0, "Enter city name...")
        self.city_entry.bind('<FocusIn>', self._on_entry_click)
        self.city_entry.bind('<FocusOut>', self._on_focus_out)
        
        # History dropdown button (inside the input frame)
        self.history_button = tk.Button(
            input_frame,
            text="⏱",
            font=('Arial', 16),
            bg='#2d2d44',
            fg='#a0a0b0',
            relief='flat',
            bd=0,
            padx=8,
            pady=10,
            cursor='hand2',
            command=self._show_history_menu
        )
        self.history_button.pack(side='left')
        self._create_tooltip(self.history_button, "Search History")
        
        # Search button positioned to the right
        self.search_button = tk.Button(
            search_container,
            text="🔍",
            font=('Arial', 18),
            bg='#5865f2',
            fg='white',
            relief='flat',
            bd=0,
            padx=18,
            pady=11,
            cursor='hand2'
        )
        self.search_button.pack(side='left', padx=(8, 0))
        self._create_tooltip(self.search_button, "Search Weather")
        
        # ===== Main Content Frame =====
        self.content_frame = tk.Frame(self.root, bg='#1e1e2e')
        self.content_frame.pack(fill='both', expand=True, padx=20)
        
        # ===== Current Weather Frame =====
        self.current_frame = tk.Frame(self.content_frame, bg='#2d2d44', relief='flat')
        self.current_frame.pack(fill='x', pady=(0, 20))
        
        # City name and flag container
        city_container = tk.Frame(self.current_frame, bg='#2d2d44')
        city_container.pack(pady=(20, 5))
        
        # City name label
        self.city_label = tk.Label(
            city_container,
            text="",
            font=('Arial', 24, 'bold'),
            bg='#2d2d44',
            fg='white'
        )
        self.city_label.pack(side='left', padx=(0, 10))
        
        # Country flag
        self.flag_label = tk.Label(city_container, bg='#2d2d44', cursor='hand2')
        self.flag_label.pack(side='left')
        
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
        
        # Loading spinner canvas
        self.loading_canvas = tk.Canvas(
            self.root,
            width=100,
            height=100,
            bg='#1e1e2e',
            highlightthickness=0
        )
    
    def _create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                background="#2d2d44",
                foreground="white",
                relief='solid',
                borderwidth=1,
                font=('Arial', 10),
                padx=5,
                pady=2
            )
            label.pack()
            
            widget.tooltip = tooltip
            widget.after(2000, tooltip.destroy)
        
        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
        
        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)
    
    def _show_history_menu(self):
        """Show search history with timestamps in a custom window"""
        if not self.search_history:
            messagebox.showinfo("History", "No search history yet!")
            return
        
        # Create custom window for history
        history_window = tk.Toplevel(self.root)
        history_window.title("Search History")
        history_window.geometry("450x400")
        history_window.configure(bg='#1e1e2e')
        
        # Title
        title_label = tk.Label(
            history_window,
            text="Recent Searches",
            font=('Arial', 16, 'bold'),
            bg='#1e1e2e',
            fg='white'
        )
        title_label.pack(pady=10)
        
        # Scrollable frame for history
        canvas = tk.Canvas(history_window, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1e1e2e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add history entries (most recent first)
        for entry in reversed(self.search_history[-10:]):
            entry_frame = tk.Frame(scrollable_frame, bg='#2d2d44', relief='solid', bd=1)
            entry_frame.pack(fill='x', padx=10, pady=5)
            
            # City name button
            city_button = tk.Button(
                entry_frame,
                text=entry['city'],
                font=('Arial', 12, 'bold'),
                bg='#2d2d44',
                fg='#5865f2',
                relief='flat',
                cursor='hand2',
                anchor='w',
                command=lambda c=entry['city']: self._select_from_history_window(c, history_window)
            )
            city_button.pack(fill='x', padx=10, pady=(5, 0))
            
            # Timestamp with clock icon
            time_label = tk.Label(
                entry_frame,
                text=f"🕒 {entry['formatted_time']}",
                font=('Arial', 9),
                bg='#2d2d44',
                fg='#a0a0b0',
                anchor='w'
            )
            time_label.pack(fill='x', padx=10, pady=(0, 5))
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Clear history button
        clear_button = tk.Button(
            history_window,
            text="Clear History",
            font=('Arial', 10),
            bg='#dc3545',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=lambda: self._clear_history(history_window)
        )
        clear_button.pack(pady=10)

    def _select_from_history_window(self, city, window):
        """Select city from history window"""
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self.city_entry.config(fg='white')
        window.destroy()
    
    def _clear_history(self, window):
        """Clear all search history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all search history?"):
            self.search_history = []
            self._save_search_history()
            window.destroy()
            messagebox.showinfo("Success", "Search history cleared!")

    def _select_from_history(self, city):
        """Select city from history"""
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self.city_entry.config(fg='white')
    
    def _update_history_dropdown(self):
        """Update history dropdown (called after new search)"""
        pass
    
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
        """Display loading spinner animation"""
        self.loading_canvas.place(relx=0.5, rely=0.5, anchor='center')
        self._animate_loading()
    
    def hide_loading(self):
        """Hide loading spinner"""
        if self.loading_animation_id:
            self.root.after_cancel(self.loading_animation_id)
            self.loading_animation_id = None
        self.loading_canvas.place_forget()
    
    def _animate_loading(self):
        """Animate the loading spinner"""
        self.loading_canvas.delete("spinner")
        
        # Draw spinning arc
        self.loading_angle = (self.loading_angle + 15) % 360
        self.loading_canvas.create_arc(
            10, 10, 90, 90,
            start=self.loading_angle,
            extent=300,
            outline='#5865f2',
            width=8,
            style='arc',
            tags="spinner"
        )
        
        # Continue animation
        self.loading_animation_id = self.root.after(50, self._animate_loading)
    
    def update_background(self, weather_condition):
        """Update background based on weather condition"""
        # Weather condition color mappings
        weather_colors = {
            'clear': '#87CEEB',      # Sky blue
            'clouds': '#778899',     # Light slate gray
            'rain': '#4682B4',       # Steel blue
            'drizzle': '#5F9EA0',    # Cadet blue
            'thunderstorm': '#2F4F4F',  # Dark slate gray
            'snow': '#F0F8FF',       # Alice blue
            'mist': '#D3D3D3',       # Light gray
            'fog': '#DCDCDC',        # Gainsboro
            'haze': '#E0E0E0',       # Light gray
        }
        
        condition_lower = weather_condition.lower()
        bg_color = '#1e1e2e'  # Default
        
        for key, color in weather_colors.items():
            if key in condition_lower:
                bg_color = color
                break
        
        # Update background with gradient effect
        self.root.configure(bg=bg_color)
        self.content_frame.configure(bg=bg_color)
        
        # Update labels to match
        for widget in [self.city_label, self.forecast_frame]:
            if hasattr(widget, 'configure'):
                try:
                    widget.configure(bg=bg_color)
                except:
                    pass
    
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
        
        # Load country flag
        self._load_country_flag(weather_data['country'])
        
        # Update background based on weather
        self.update_background(weather_data['description'])
        
        # Add to search history
        self.add_to_history(weather_data['city'])
    
    def _load_country_flag(self, country_code):
        """Load and display country flag"""
        try:
            url = f"https://flagcdn.com/w80/{country_code.lower()}.png"
            with urllib.request.urlopen(url, timeout=5) as u:
                raw_data = u.read()
            
            image = Image.open(io.BytesIO(raw_data))
            image = image.resize((40, 30), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            
            self.flag_cache[country_code] = photo
            self.flag_label.config(image=photo)
            self.flag_label.image = photo
            
            # Add tooltip
            self._create_tooltip(self.flag_label, f"Country: {country_code}")
            
        except Exception as e:
            print(f"Error loading flag: {e}")
            self.flag_label.config(image='', text=country_code)
    
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
            label_widget.image = photo
            
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
        if hasattr(self, 'search_button'):
            self.search_button.config(command=callback)
            self.city_entry.bind('<Return>', lambda e: callback())
        else:
            self.root.after(2100, lambda: self.bind_search(callback))