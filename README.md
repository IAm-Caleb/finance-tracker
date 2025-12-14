🌤️ Weather Dashboard Application
A comprehensive, production-ready Python weather dashboard application with real-time data, forecasts, analytics, and beautiful visualizations.

Show Image
Show Image
Show Image

📋 Table of Contents
Features
Screenshots
Technologies Used
Installation
Configuration
Usage
Project Structure
API Reference
Contributing
License
✨ Features
Core Functionality
Real-time Weather Data - Get current weather conditions for any city worldwide
7-Day Forecast - Comprehensive weather forecasts with detailed metrics
Search History - Track and quickly access your last 10 weather searches
Multiple Temperature Units - Switch between Celsius and Fahrenheit
Data Visualization
Static Charts (Matplotlib)
7-day temperature line chart with min/max/average temperatures
Humidity bar chart with color gradients
Professional styling and annotations
Interactive Charts (Plotly)
Hoverable temperature forecast with detailed tooltips
Temperature vs Humidity comparison with dual axes
Temperature heatmap visualization
Smooth animations and zoom capabilities
Analytics & Insights
Temperature statistics (min, max, average, standard deviation)
Humidity analysis with trends
Temperature trend detection (increasing/decreasing/stable)
Data export to CSV format
Comprehensive weather summaries
User Interface
Modern, responsive design with gradient styling
Tab-based navigation (Current Weather, Analytics, Charts, History)
Sidebar with quick search and recent searches
Customizable settings
Error handling with friendly messages
Loading indicators for better UX
📸 Screenshots
Main Dashboard
Show Image
Main weather dashboard showing current conditions

Interactive Charts
Show Image
Interactive temperature and humidity visualizations

Analytics Dashboard
Show Image
Comprehensive weather analytics and trends

🛠️ Technologies Used
Technology	Purpose
Python 3.8+	Core programming language
Streamlit	Web UI framework for rapid development
OpenWeatherMap API	Real-time weather data source
Pandas	Data manipulation and analysis
NumPy	Numerical computations and statistics
Matplotlib	Static chart generation
Plotly	Interactive visualizations
Requests	HTTP API calls
python-dotenv	Environment variable management
📦 Installation
Prerequisites
Python 3.8 or higher
pip package manager
OpenWeatherMap API key (free tier available)
Step-by-Step Installation
Clone the repository
bash
git clone https://github.com/yourusername/weather-dashboard.git
cd weather-dashboard
Create a virtual environment (recommended)
bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install required packages
bash
pip install -r requirements.txt
Set up your API key
Create a .env file in the project root:

bash
OPENWEATHER_API_KEY=your_api_key_here
Or you can enter it directly in the application interface.

⚙️ Configuration
Getting an API Key
Visit OpenWeatherMap
Sign up for a free account
Navigate to API Keys section
Copy your API key
Add it to .env file or enter it in the app
Environment Variables
Create a .env file with the following:

env
OPENWEATHER_API_KEY=your_api_key_here
🚀 Usage
Running the Application
bash
streamlit run main.py
The application will open automatically in your default web browser at http://localhost:8501

Using the Dashboard
Search for Weather
Enter a city name in the sidebar search box
Click the "Search" button
View current weather and 7-day forecast
View Analytics
Navigate to the "Analytics" tab
See statistical analysis of forecast data
Export data to CSV for further analysis
Explore Charts
Go to the "Charts" tab
Select different chart types from the dropdown
Interact with charts (hover, zoom, pan)
Check History
Visit the "History" tab
Click on any previous search to reload it
Clear history when needed
Customize Settings
Use the sidebar settings
Switch temperature units
Manage search history
📁 Project Structure
WeatherApp/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── README.md              # This file
│
├── src/                   # Source code modules
│   ├── __init__.py
│   ├── api.py            # Weather API integration
│   ├── charts.py         # Chart generation (Matplotlib & Plotly)
│   ├── utils.py          # Utility functions & data processing
│   └── ui.py             # Streamlit UI components
│
├── data/                  # Data storage
│   └── search_history.json  # Search history (auto-created)
│
├── assets/                # Static assets
│   ├── icons/            # Weather icons
│   └── screenshots/      # Application screenshots
│
└── docs/                  # Documentation
    ├── user_manual.md    # User guide
    └── report_outline.md # Project report structure
Module Descriptions
main.py
Entry point for the application. Initializes Streamlit configuration and launches the UI.

src/api.py
WeatherAPI class for OpenWeatherMap integration
Current weather data retrieval
7-day forecast fetching
Error handling and response normalization
src/charts.py
Static chart generation with Matplotlib
Interactive charts with Plotly
Temperature trends, humidity charts, heatmaps
Custom styling and professional layouts
src/utils.py
File handling (JSON read/write)
Search history management
Data analysis with pandas and numpy
Temperature conversions
Statistical computations
src/ui.py
Main UI layout and components
Tab-based navigation
Weather display cards
Settings and configuration
User interaction handlers
📚 API Reference
WeatherAPI Class
python
from src.api import WeatherAPI

api = WeatherAPI(api_key="your_key")

# Get current weather
current, error = api.get_current_weather("London")

# Get 7-day forecast
forecast, error = api.get_forecast("London")

# Validate API key
is_valid = api.validate_api_key()
Utility Functions
python
from src.utils import (
    save_search_to_history,
    load_search_history,
    analyze_forecast_data,
    celsius_to_fahrenheit
)

# Save search
save_search_to_history("London", weather_data)

# Load history
history = load_search_history()

# Analyze forecast
stats = analyze_forecast_data(forecast_list)

# Convert temperature
temp_f = celsius_to_fahrenheit(25)
Chart Functions
python
from src.charts import (
    create_temperature_line_chart,
    create_interactive_temperature_chart
)

# Create static chart
fig = create_temperature_line_chart(forecast_data)

# Create interactive chart
plotly_fig = create_interactive_temperature_chart(forecast_data)
🧪 Testing
Run the application in debug mode:

bash
streamlit run main.py --logger.level=debug
🐛 Troubleshooting
Common Issues
1. API Key Error

Ensure your API key is valid
Check the .env file is in the project root
Wait a few minutes after creating a new API key
2. City Not Found

Check spelling of city name
Try including country code: "London,UK"
Use major city names for better results
3. Import Errors

Ensure all dependencies are installed: pip install -r requirements.txt
Check Python version: python --version (should be 3.8+)
4. Charts Not Displaying

Clear browser cache
Check console for JavaScript errors
Ensure matplotlib and plotly are installed correctly
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👥 Authors
Your Name - Initial work - YourGitHub
🙏 Acknowledgments
OpenWeatherMap for providing the weather API
Streamlit team for the amazing framework
Python community for excellent libraries
📞 Support
For support, email your-email@example.com or open an issue in the GitHub repository.

🔄 Version History
1.0.0 (2025-11-28)
Initial release
Core weather features
Analytics dashboard
Interactive charts
Search history
🚀 Future Enhancements
 Weather alerts and notifications
 Multiple location comparison
 Historical weather data analysis
 Mobile responsive improvements
 Dark mode theme
 Weather maps integration
 Social sharing features
 Favorite locations
Built with ❤️ using Python and Streamlit

