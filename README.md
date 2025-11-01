## ✨ Features

- 🌍 **Global Coverage** - Search weather for any city worldwide
- 🌡️ **Current Weather** - Real-time temperature, humidity, wind speed, and more
- 📅 **5-Day Forecast** - Extended weather predictions
- 🎨 **Modern UI** - Clean, dark-themed interface with smooth animations
- 🖼️ **Weather Icons** - Visual representation of weather conditions
- ⚡ **Fast & Responsive** - Asynchronous API calls prevent UI freezing
- 🏗️ **MVC Architecture** - Clean code structure for easy maintenance

## 🛠️ Technologies Used

- **Python 3.8+** - Core programming language
- **Tkinter** - GUI framework
- **OpenWeatherMap API** - Weather data provider
- **Pillow (PIL)** - Image processing for weather icons
- **Requests** - HTTP library for API calls
- **Threading** - Asynchronous operations

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher ([Download Python](https://www.python.org/downloads/))
- pip (Python package installer)
- OpenWeatherMap API Key ([Get Free API Key](https://openweathermap.org/api))

## Using the App

1. **Launch** the application
2. **Enter** a city name in the search bar
3. **Press Enter** or click the "Search" button
4. **View** current weather and 5-day forecast

### Example Cities to Try

- New York
- London
- Tokyo
- Paris
- Sydney

## 📁 Project Structure
```
weather-app-project/
│
├── main.py              # Application entry point
├── model.py             # Data layer (API calls, data processing)
├── view.py              # Presentation layer (GUI components)
├── controller.py        # Logic layer (coordinates Model & View)
│
├── config.py            # API key configuration (not in git)
├── config.example.py    # Configuration template
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## 🏛️ Architecture

This project follows the **MVC (Model-View-Controller)** design pattern:

### Model (`model.py`)

- Handles all data operations
- Makes API requests to OpenWeatherMap
- Processes and formats weather data
- No knowledge of the UI

### View (`view.py`)

- Manages all GUI components
- Displays weather information
- Handles user interface events
- No business logic

### Controller (`controller.py`)

- Bridges Model and View
- Handles user input
- Updates View with data from Model
- Manages application flow

## 🔑 Getting Your API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Click "Sign Up" and create a free account
3. Verify your email address
4. Go to "API Keys" section in your dashboard
5. Copy your API key


**Note:** Free tier allows 60 API calls per minute, which is more than enough for this application.

## 👥 Authors

- **Alex Opoku** - [OpkWan](https://github.com/OpkWan)
- **Najeeb Dollah Hussein** - [Marsfelloff](https://github.com/Marsfelloff)

## 🙏 Acknowledgments

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Weather icons from OpenWeatherMap
- Inspired by modern weather applications
- Built as a learning project for MVC architecture

## 📞 Contact

Have questions or suggestions? Reach out!

- **GitHub:** [OpkWan](https://github.com/OpkWan) & [Marsfelloff](https://github.com/Marsfelloff)