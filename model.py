# model.py
<<<<<<< HEAD
"""
Weather App - Model Entry Point
MVC Architecture
"""

=======
>>>>>>> c08361b (Debugging a few glitches)
import requests
from datetime import datetime

class WeatherModel:
    """Handles weather data fetching and processing"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city):
        """Fetch current weather data for a city"""
        try:
            endpoint = f"{self.base_url}/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # or 'imperial' for Fahrenheit
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_current_weather(data)
            
        except requests.exceptions.RequestException as e:
            return {'error': f"Network error: {str(e)}"}
        except Exception as e:
            return {'error': f"Error: {str(e)}"}
    
    def get_forecast(self, city):
        """Fetch 5-day forecast data"""
        try:
            endpoint = f"{self.base_url}/forecast"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_forecast(data)
            
        except requests.exceptions.RequestException as e:
            return {'error': f"Network error: {str(e)}"}
        except Exception as e:
            return {'error': f"Error: {str(e)}"}
    
    def _parse_current_weather(self, data):
        """Parse raw API data into usable format"""
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'description': data['weather'][0]['description'].title(),
            'icon': data['weather'][0]['icon'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': round(data['wind']['speed'], 1),
            'visibility': data.get('visibility', 0) // 1000,  # Convert to km
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        }
    
    def _parse_forecast(self, data):
        """Parse forecast data - get one reading per day"""
        daily_forecasts = []
        processed_dates = set()
        
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).date()
            
            # Get one forecast per day (around noon)
            if date not in processed_dates and '12:00:00' in item['dt_txt']:
                daily_forecasts.append({
                    'date': date.strftime('%a, %b %d'),
                    'temp_max': round(item['main']['temp_max']),
                    'temp_min': round(item['main']['temp_min']),
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon']
                })
                processed_dates.add(date)
                
                if len(daily_forecasts) >= 5:
                    break
        
        return daily_forecasts