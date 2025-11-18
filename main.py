
import tkinter as tk
from model import WeatherModel
from view import WeatherView
from controller import WeatherController

def main():
    # Replace with your actual API key
    API_KEY = "c3b3f8a5bd07284fbcf1e04430c69738"
    
    # Create root window
    root = tk.Tk()
    
    # Initialize MVC components
    model = WeatherModel(API_KEY)
    view = WeatherView(root)
    controller = WeatherController(model, view)
    
    # Start application
    controller.run()

if __name__ == "__main__":
    main()