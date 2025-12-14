# src/utils.py
"""
Utility Functions Module
========================
Provides utility functions for:
- File handling (JSON read/write)
- Data processing and conversions
- Search history management
- Data analysis using pandas and numpy

Dependencies:
    - json: JSON file operations
    - os: File system operations
    - pandas: Data analysis and manipulation
    - numpy: Numerical computations
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import numpy as np

# Constants
DATA_DIR = "data"
SEARCH_HISTORY_FILE = os.path.join(DATA_DIR, "search_history.json")
MAX_HISTORY_ITEMS = 10

def initialize_data_directory() -> None:
    """
    Initialize the data directory and required files.
    
    Creates the data directory if it doesn't exist and initializes
    the search_history.json file with an empty list if not present.
    
    Returns:
        None
    """
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"Created directory: {DATA_DIR}")
        
        # Initialize search history file if it doesn't exist
        if not os.path.exists(SEARCH_HISTORY_FILE):
            with open(SEARCH_HISTORY_FILE, 'w') as f:
                json.dump([], f)
            print(f"Initialized file: {SEARCH_HISTORY_FILE}")
            
    except Exception as e:
        print(f"Error initializing data directory: {str(e)}")

def save_search_to_history(city: str, weather_data: Dict) -> bool:
    """
    Save a weather search to the history file.
    
    Maintains a maximum of 10 recent searches. If the limit is exceeded,
    the oldest search is removed.
    
    Args:
        city (str): Name of the city searched
        weather_data (Dict): Weather data returned from API
        
    Returns:
        bool: True if save was successful, False otherwise
        
    Example:
        >>> save_search_to_history("London", weather_data)
        True
    """
    try:
        # Read existing history
        history = load_search_history()
        
        # Create new search entry
        search_entry = {
            'city': city,
            'temperature': weather_data.get('temperature', 0),
            'description': weather_data.get('description', 'N/A'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Remove duplicate city entries (keep most recent)
        history = [h for h in history if h.get('city', '').lower() != city.lower()]
        
        # Add new entry at the beginning
        history.insert(0, search_entry)
        
        # Keep only last MAX_HISTORY_ITEMS entries
        history = history[:MAX_HISTORY_ITEMS]
        
        # Save to file
        with open(SEARCH_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error saving search history: {str(e)}")
        return False

def load_search_history() -> List[Dict]:
    """
    Load search history from the JSON file.
    
    Returns:
        List[Dict]: List of search history entries, empty list if file
                    doesn't exist or is corrupted
                    
    Example:
        >>> history = load_search_history()
        >>> for entry in history:
        ...     print(f"{entry['city']}: {entry['temperature']}°C")
    """
    try:
        if os.path.exists(SEARCH_HISTORY_FILE):
            with open(SEARCH_HISTORY_FILE, 'r') as f:
                return json.load(f)
        return []
        
    except (json.JSONDecodeError, Exception) as e:
        print(f"Error loading search history: {str(e)}")
        return []

def clear_search_history() -> bool:
    """
    Clear all entries from the search history.
    
    Returns:
        bool: True if clearing was successful, False otherwise
    """
    try:
        with open(SEARCH_HISTORY_FILE, 'w') as f:
            json.dump([], f)
        return True
        
    except Exception as e:
        print(f"Error clearing search history: {str(e)}")
        return False

def analyze_forecast_data(forecast_data: List[Dict]) -> Dict:
    """
    Perform statistical analysis on forecast data using pandas and numpy.
    
    Args:
        forecast_data (List[Dict]): List of forecast entries with temperature
                                    and humidity data
                                    
    Returns:
        Dict: Dictionary containing various statistical metrics:
            - temp_min: Minimum temperature
            - temp_max: Maximum temperature
            - temp_avg: Average temperature
            - temp_std: Standard deviation of temperature
            - humidity_avg: Average humidity
            - humidity_std: Standard deviation of humidity
            - trend: Temperature trend (increasing/decreasing/stable)
            
    Example:
        >>> forecast = [{'temp_avg': 20, 'humidity_avg': 65}, ...]
        >>> stats = analyze_forecast_data(forecast)
        >>> print(f"Average temp: {stats['temp_avg']}°C")
    """
    try:
        if not forecast_data:
            return {
                'temp_min': 0,
                'temp_max': 0,
                'temp_avg': 0,
                'temp_std': 0,
                'humidity_avg': 0,
                'humidity_std': 0,
                'trend': 'No data'
            }
        
        # Convert to pandas DataFrame for easy analysis
        df = pd.DataFrame(forecast_data)
        
        # Temperature statistics
        temps = df['temp_avg'].values if 'temp_avg' in df else df['temp_max'].values
        temp_min = float(np.min(temps))
        temp_max = float(np.max(temps))
        temp_avg = float(np.mean(temps))
        temp_std = float(np.std(temps))
        
        # Humidity statistics
        humidity = df['humidity_avg'].values
        humidity_avg = float(np.mean(humidity))
        humidity_std = float(np.std(humidity))
        
        # Calculate temperature trend using linear regression
        x = np.arange(len(temps))
        slope = np.polyfit(x, temps, 1)[0]
        
        if slope > 0.5:
            trend = "Increasing"
        elif slope < -0.5:
            trend = "Decreasing"
        else:
            trend = "Stable"
        
        return {
            'temp_min': round(temp_min, 1),
            'temp_max': round(temp_max, 1),
            'temp_avg': round(temp_avg, 1),
            'temp_std': round(temp_std, 2),
            'humidity_avg': round(humidity_avg, 1),
            'humidity_std': round(humidity_std, 2),
            'trend': trend,
            'slope': round(slope, 3)
        }
        
    except Exception as e:
        print(f"Error analyzing forecast data: {str(e)}")
        return {
            'temp_min': 0,
            'temp_max': 0,
            'temp_avg': 0,
            'temp_std': 0,
            'humidity_avg': 0,
            'humidity_std': 0,
            'trend': 'Error'
        }

def format_temperature(temp: float, unit: str = "C") -> str:
    """
    Format temperature value with appropriate unit symbol.
    
    Args:
        temp (float): Temperature value
        unit (str): Temperature unit ('C' for Celsius, 'F' for Fahrenheit)
        
    Returns:
        str: Formatted temperature string
        
    Example:
        >>> format_temperature(25.5, "C")
        '25.5°C'
    """
    return f"{temp}°{unit}"

def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Convert temperature from Celsius to Fahrenheit.
    
    Args:
        celsius (float): Temperature in Celsius
        
    Returns:
        float: Temperature in Fahrenheit
        
    Example:
        >>> celsius_to_fahrenheit(25)
        77.0
    """
    return round((celsius * 9/5) + 32, 1)

def get_weather_icon_url(icon_code: str) -> str:
    """
    Generate URL for weather icon from OpenWeatherMap.
    
    Args:
        icon_code (str): Weather icon code from API (e.g., '01d')
        
    Returns:
        str: Full URL to weather icon image
        
    Example:
        >>> get_weather_icon_url('01d')
        'http://openweathermap.org/img/wn/01d@2x.png'
    """
    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

def calculate_heat_index(temp: float, humidity: float) -> float:
    """
    Calculate heat index (feels like temperature) based on temperature and humidity.
    
    This is a simplified heat index calculation. For more accurate results,
    use the actual 'feels_like' value from the API.
    
    Args:
        temp (float): Temperature in Celsius
        humidity (float): Relative humidity percentage
        
    Returns:
        float: Calculated heat index in Celsius
        
    Example:
        >>> calculate_heat_index(30, 70)
        34.5
    """
    try:
        # Convert to Fahrenheit for calculation
        temp_f = celsius_to_fahrenheit(temp)
        
        # Simplified heat index formula
        if temp_f >= 80:
            hi = -42.379 + 2.04901523*temp_f + 10.14333127*humidity
            hi = hi - 0.22475541*temp_f*humidity - 0.00683783*temp_f**2
            hi = hi - 0.05481717*humidity**2 + 0.00122874*temp_f**2*humidity
            hi = hi + 0.00085282*temp_f*humidity**2 - 0.00000199*temp_f**2*humidity**2
            
            # Convert back to Celsius
            heat_index_c = (hi - 32) * 5/9
            return round(heat_index_c, 1)
        else:
            return temp
            
    except Exception:
        return temp

def export_data_to_csv(data: Dict, filename: str) -> bool:
    """
    Export weather data to CSV file for further analysis.
    
    Args:
        data (Dict): Weather or forecast data dictionary
        filename (str): Output CSV filename
        
    Returns:
        bool: True if export was successful, False otherwise
    """
    try:
        if 'forecast' in data:
            df = pd.DataFrame(data['forecast'])
        else:
            df = pd.DataFrame([data])
        
        filepath = os.path.join(DATA_DIR, filename)
        df.to_csv(filepath, index=False)
        return True
        
    except Exception as e:
        print(f"Error exporting to CSV: {str(e)}")
        return False

def get_data_summary(forecast_data: List[Dict]) -> str:
    """
    Generate a human-readable summary of forecast data.
    
    Args:
        forecast_data (List[Dict]): List of forecast entries
        
    Returns:
        str: Formatted summary string
    """
    if not forecast_data:
        return "No forecast data available."
    
    analysis = analyze_forecast_data(forecast_data)
    
    summary = f"""
    📊 Forecast Summary (Next {len(forecast_data)} Days)
    
    🌡️ Temperature Range: {analysis['temp_min']}°C to {analysis['temp_max']}°C
    📈 Average Temperature: {analysis['temp_avg']}°C
    💧 Average Humidity: {analysis['humidity_avg']}%
    📉 Temperature Trend: {analysis['trend']}
    """
    
    return summary.strip()




# # src/utils.py
# """
# Utility Functions Module
# ========================
# Provides utility functions for:
# - File handling (JSON read/write)
# - Data processing and conversions
# - Search history management
# - Data analysis using pandas and numpy

# Dependencies:
#     - json: JSON file operations
#     - os: File system operations
#     - pandas: Data analysis and manipulation
#     - numpy: Numerical computations
# """

# import json
# import os
# from typing import List, Dict, Optional
# from datetime import datetime
# import pandas as pd
# import numpy as np

# # Constants
# DATA_DIR = "data"
# SEARCH_HISTORY_FILE = os.path.join(DATA_DIR, "search_history.json")
# MAX_HISTORY_ITEMS = 10

# def initialize_data_directory() -> None:
#     """
#     Initialize the data directory and required files.
    
#     Creates the data directory if it doesn't exist and initializes
#     the search_history.json file with an empty list if not present.
    
#     Returns:
#         None
#     """
#     try:
#         # Create data directory if it doesn't exist
#         if not os.path.exists(DATA_DIR):
#             os.makedirs(DATA_DIR)
#             print(f"Created directory: {DATA_DIR}")
        
#         # Initialize search history file if it doesn't exist
#         if not os.path.exists(SEARCH_HISTORY_FILE):
#             with open(SEARCH_HISTORY_FILE, 'w') as f:
#                 json.dump([], f)
#             print(f"Initialized file: {SEARCH_HISTORY_FILE}")
            
#     except Exception as e:
#         print(f"Error initializing data directory: {str(e)}")

# def save_search_to_history(city: str, weather_data: Dict) -> bool:
#     """
#     Save a weather search to the history file.
    
#     Maintains a maximum of 10 recent searches. If the limit is exceeded,
#     the oldest search is removed.
    
#     Args:
#         city (str): Name of the city searched
#         weather_data (Dict): Weather data returned from API
        
#     Returns:
#         bool: True if save was successful, False otherwise
        
#     Example:
#         >>> save_search_to_history("London", weather_data)
#         True
#     """
#     try:
#         # Read existing history
#         history = load_search_history()
        
#         # Create new search entry
#         search_entry = {
#             'city': city,
#             'temperature': weather_data.get('temperature', 0),
#             'description': weather_data.get('description', 'N/A'),
#             'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         }
        
#         # Remove duplicate city entries (keep most recent)
#         history = [h for h in history if h.get('city', '').lower() != city.lower()]
        
#         # Add new entry at the beginning
#         history.insert(0, search_entry)
        
#         # Keep only last MAX_HISTORY_ITEMS entries
#         history = history[:MAX_HISTORY_ITEMS]
        
#         # Save to file
#         with open(SEARCH_HISTORY_FILE, 'w') as f:
#             json.dump(history, f, indent=2)
        
#         return True
        
#     except Exception as e:
#         print(f"Error saving search history: {str(e)}")
#         return False

# def load_search_history() -> List[Dict]:
#     """
#     Load search history from the JSON file.
    
#     Returns:
#         List[Dict]: List of search history entries, empty list if file
#                     doesn't exist or is corrupted
                    
#     Example:
#         >>> history = load_search_history()
#         >>> for entry in history:
#         ...     print(f"{entry['city']}: {entry['temperature']}°C")
#     """
#     try:
#         if os.path.exists(SEARCH_HISTORY_FILE):
#             with open(SEARCH_HISTORY_FILE, 'r') as f:
#                 return json.load(f)
#         return []
        
#     except (json.JSONDecodeError, Exception) as e:
#         print(f"Error loading search history: {str(e)}")
#         return []

# def clear_search_history() -> bool:
#     """
#     Clear all entries from the search history.
    
#     Returns:
#         bool: True if clearing was successful, False otherwise
#     """
#     try:
#         with open(SEARCH_HISTORY_FILE, 'w') as f:
#             json.dump([], f)
#         return True
        
#     except Exception as e:
#         print(f"Error clearing search history: {str(e)}")
#         return False

# def analyze_forecast_data(forecast_data: List[Dict]) -> Dict:
#     """
#     Perform statistical analysis on forecast data using pandas and numpy.
    
#     Args:
#         forecast_data (List[Dict]): List of forecast entries with temperature
#                                     and humidity data
                                    
#     Returns:
#         Dict: Dictionary containing various statistical metrics:
#             - temp_min: Minimum temperature
#             - temp_max: Maximum temperature
#             - temp_avg: Average temperature
#             - temp_std: Standard deviation of temperature
#             - humidity_avg: Average humidity
#             - humidity_std: Standard deviation of humidity
#             - trend: Temperature trend (increasing/decreasing/stable)
            
#     Example:
#         >>> forecast = [{'temp_avg': 20, 'humidity_avg': 65}, ...]
#         >>> stats = analyze_forecast_data(forecast)
#         >>> print(f"Average temp: {stats['temp_avg']}°C")
#     """
#     try:
#         if not forecast_data:
#             return {
#                 'temp_min': 0,
#                 'temp_max': 0,
#                 'temp_avg': 0,
#                 'temp_std': 0,
#                 'humidity_avg': 0,
#                 'humidity_std': 0,
#                 'trend': 'No data'
#             }
        
#         # Convert to pandas DataFrame for easy analysis
#         df = pd.DataFrame(forecast_data)
        
#         # Temperature statistics
#         temps = df['temp_avg'].values if 'temp_avg' in df else df['temp_max'].values
#         temp_min = float(np.min(temps))
#         temp_max = float(np.max(temps))
#         temp_avg = float(np.mean(temps))
#         temp_std = float(np.std(temps))
        
#         # Humidity statistics
#         humidity = df['humidity_avg'].values
#         humidity_avg = float(np.mean(humidity))
#         humidity_std = float(np.std(humidity))
        
#         # Calculate temperature trend using linear regression
#         x = np.arange(len(temps))
#         slope = np.polyfit(x, temps, 1)[0]
        
#         if slope > 0.5:
#             trend = "Increasing"
#         elif slope < -0.5:
#             trend = "Decreasing"
#         else:
#             trend = "Stable"
        
#         return {
#             'temp_min': round(temp_min, 1),
#             'temp_max': round(temp_max, 1),
#             'temp_avg': round(temp_avg, 1),
#             'temp_std': round(temp_std, 2),
#             'humidity_avg': round(humidity_avg, 1),
#             'humidity_std': round(humidity_std, 2),
#             'trend': trend,
#             'slope': round(slope, 3)
#         }
        
#     except Exception as e:
#         print(f"Error analyzing forecast data: {str(e)}")
#         return {
#             'temp_min': 0,
#             'temp_max': 0,
#             'temp_avg': 0,
#             'temp_std': 0,
#             'humidity_avg': 0,
#             'humidity_std': 0,
#             'trend': 'Error'
#         }

# def format_temperature(temp: float, unit: str = "C") -> str:
#     """
#     Format temperature value with appropriate unit symbol.
    
#     Args:
#         temp (float): Temperature value
#         unit (str): Temperature unit ('C' for Celsius, 'F' for Fahrenheit)
        
#     Returns:
#         str: Formatted temperature string
        
#     Example:
#         >>> format_temperature(25.5, "C")
#         '25.5°C'
#     """
#     return f"{temp}°{unit}"

# def celsius_to_fahrenheit(celsius: float) -> float:
#     """
#     Convert temperature from Celsius to Fahrenheit.
    
#     Args:
#         celsius (float): Temperature in Celsius
        
#     Returns:
#         float: Temperature in Fahrenheit
        
#     Example:
#         >>> celsius_to_fahrenheit(25)
#         77.0
#     """
#     return round((celsius * 9/5) + 32, 1)

# def get_weather_icon_url(icon_code: str) -> str:
#     """
#     Generate URL for weather icon from OpenWeatherMap.
    
#     Args:
#         icon_code (str): Weather icon code from API (e.g., '01d')
        
#     Returns:
#         str: Full URL to weather icon image
        
#     Example:
#         >>> get_weather_icon_url('01d')
#         'http://openweathermap.org/img/wn/01d@2x.png'
#     """
#     return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

# def get_weather_animation_url(description: str, icon_code: str) -> str:
#     """
#     Get animated weather GIF URL based on weather condition.
    
#     Args:
#         description (str): Weather description from API
#         icon_code (str): Weather icon code from API
        
#     Returns:
#         str: URL to animated weather GIF
#     """
#     # Map weather conditions to GIF URLs
#     desc_lower = description.lower()
    
#     # Using Giphy API-style URLs for weather animations
#     weather_gifs = {
#         'clear': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDRzaWJ5NnE2Zzd4YnJ3OHZoZGVqM2k4bTVvNzFjYTJpbWF4ZW9mYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7btPCcdNniyf0ArS/giphy.gif',
#         'clouds': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExMnoyaG5xdGt3aGZqZzRqZnc4OGRpN2FrMnE4YWJtcjN2dGoxeGg4ZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0K4mVE5b5WZ1sctW/giphy.gif',
#         'rain': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGo2ZHl3enN4eWJ5d2ZwYzN4cjZxYnBnemF3bDVrYnp6YzJ6dnVkZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0Iy5fjHyedk9TfjO/giphy.gif',
#         'drizzle': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaGo2ZHl3enN4eWJ5d2ZwYzN4cjZxYnBnemF3bDVrYnp6YzJ6dnVkZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0Iy5fjHyedk9TfjO/giphy.gif',
#         'thunderstorm': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDV2ZHduZGd3YjJpbWR0M3A2NmN6M2N5Ym5xY2NnMHo4bzB2enJhcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4N5vB4aErlVtVsywBw/giphy.gif',
#         'snow': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3p5dGQ0aGphZGJxZnd6NjI3dHNkaDh5aGF1anRraWt6dGd4MzJpYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xT0BKqB8KIOuqJemVW/giphy.gif',
#         'mist': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnFxdnU5OWNsMnE4Ym02M3drYTZveXFnYXc0N2NwZHh1dWJqd3p5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/12WEBZaeMLsMnu/giphy.gif',
#         'fog': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnFxdnU5OWNsMnE4Ym02M3drYTZveXFnYXc0N2NwZHh1dWJqd3p5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/12WEBZaeMLsMnu/giphy.gif',
#         'haze': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnFxdnU5OWNsMnE4Ym02M3drYTZveXFnYXc0N2NwZHh1dWJqd3p5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/12WEBZaeMLsMnu/giphy.gif',
#         'smoke': 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnFxdnU5OWNsMnE4Ym02M3drYTZveXFnYXc0N2NwZHh1dWJqd3p5eCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/12WEBZaeMLsMnu/giphy.gif',
#     }
    
#     # Check for specific conditions
#     for condition, gif_url in weather_gifs.items():
#         if condition in desc_lower:
#             return gif_url
    
#     # Default based on icon code (day/night)
#     if 'd' in icon_code:  # Daytime
#         return weather_gifs['clear']
#     else:  # Nighttime
#         return 'https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGo4cWJqN3h5bDl5OGE4eWJxYnR6cWt5bTZxY3FxaGRxNmE5Y3l0aSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/26FPCXdkvDbKBbgOI/giphy.gif'

# def calculate_heat_index(temp: float, humidity: float) -> float:
#     """
#     Calculate heat index (feels like temperature) based on temperature and humidity.
    
#     This is a simplified heat index calculation. For more accurate results,
#     use the actual 'feels_like' value from the API.
    
#     Args:
#         temp (float): Temperature in Celsius
#         humidity (float): Relative humidity percentage
        
#     Returns:
#         float: Calculated heat index in Celsius
        
#     Example:
#         >>> calculate_heat_index(30, 70)
#         34.5
#     """
#     try:
#         # Convert to Fahrenheit for calculation
#         temp_f = celsius_to_fahrenheit(temp)
        
#         # Simplified heat index formula
#         if temp_f >= 80:
#             hi = -42.379 + 2.04901523*temp_f + 10.14333127*humidity
#             hi = hi - 0.22475541*temp_f*humidity - 0.00683783*temp_f**2
#             hi = hi - 0.05481717*humidity**2 + 0.00122874*temp_f**2*humidity
#             hi = hi + 0.00085282*temp_f*humidity**2 - 0.00000199*temp_f**2*humidity**2
            
#             # Convert back to Celsius
#             heat_index_c = (hi - 32) * 5/9
#             return round(heat_index_c, 1)
#         else:
#             return temp
            
#     except Exception:
#         return temp

# def export_data_to_csv(data: Dict, filename: str) -> bool:
#     """
#     Export weather data to CSV file for further analysis.
    
#     Args:
#         data (Dict): Weather or forecast data dictionary
#         filename (str): Output CSV filename
        
#     Returns:
#         bool: True if export was successful, False otherwise
#     """
#     try:
#         if 'forecast' in data:
#             df = pd.DataFrame(data['forecast'])
#         else:
#             df = pd.DataFrame([data])
        
#         filepath = os.path.join(DATA_DIR, filename)
#         df.to_csv(filepath, index=False)
#         return True
        
#     except Exception as e:
#         print(f"Error exporting to CSV: {str(e)}")
#         return False

# def get_data_summary(forecast_data: List[Dict]) -> str:
#     """
#     Generate a human-readable summary of forecast data.
    
#     Args:
#         forecast_data (List[Dict]): List of forecast entries
        
#     Returns:
#         str: Formatted summary string
#     """
#     if not forecast_data:
#         return "No forecast data available."
    
#     analysis = analyze_forecast_data(forecast_data)
    
#     summary = f"""
#     📊 Forecast Summary (Next {len(forecast_data)} Days)
    
#     🌡️ Temperature Range: {analysis['temp_min']}°C to {analysis['temp_max']}°C
#     📈 Average Temperature: {analysis['temp_avg']}°C
#     💧 Average Humidity: {analysis['humidity_avg']}%
#     📉 Temperature Trend: {analysis['trend']}
#     """
    
#     return summary.strip()