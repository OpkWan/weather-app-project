import threading
class WeatherController:
    """Manages application logic and coordinates Model-View interaction"""
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Bind view events to controller methods
        self.view.bind_search(self.search_weather)
    
    def search_weather(self):
        """Handle weather search request"""
        city = self.view.get_city_input()
        
        if not city:
            self.view.show_error("Please enter a city name")
            return
        
        # Show loading indicator
        self.view.show_loading()
        
        # Fetch data in background thread to prevent UI freezing
        thread = threading.Thread(target=self._fetch_weather_data, args=(city,))
        thread.daemon = True
        thread.start()
    
    def _fetch_weather_data(self, city):
        """Fetch weather data from API (runs in background)"""
        # Get current weather
        current_data = self.model.get_current_weather(city)
        
        if 'error' in current_data:
            self.view.root.after(0, self.view.hide_loading)
            self.view.root.after(0, self.view.show_error, current_data['error'])
            return
        
        # Get forecast
        forecast_data = self.model.get_forecast(city)
        
        # Update UI on main thread
        self.view.root.after(0, self._update_ui, current_data, forecast_data)
    
    def _update_ui(self, current_data, forecast_data):
        """Update the view with fetched data (runs on main thread)"""
        self.view.hide_loading()
        
        if 'error' not in current_data:
            self.view.update_current_weather(current_data)
        
        if 'error' not in forecast_data:
            self.view.update_forecast(forecast_data)
    
    def run(self):
        """Start the application"""
        self.view.root.mainloop()