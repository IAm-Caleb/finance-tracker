# src/api.py
"""
Weather API Integration Module
===============================
Handles all interactions with the OpenWeatherMap API including:
- Current weather data retrieval
- 7-day forecast data
- Error handling and response normalization
- API key management

Dependencies:
    - requests: HTTP library for API calls
    - json: JSON data handling
"""

import requests
import json
from typing import Dict, Optional, Tuple
from datetime import datetime, timezone

class WeatherAPI:
    """
    A class to handle all OpenWeatherMap API operations.
    
    Attributes:
        api_key (str): OpenWeatherMap API key
        base_url (str): Base URL for current weather API
        forecast_url (str): Base URL for forecast API
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the WeatherAPI with an API key.
        
        Args:
            api_key (str): Valid OpenWeatherMap API key
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
        self.onecall_url = "http://api.openweathermap.org/data/2.5/onecall"
    
    def get_current_weather(self, city: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Fetch current weather data for a specified city.
        
        Args:
            city (str): Name of the city to fetch weather for
            
        Returns:
            Tuple[Optional[Dict], Optional[str]]: 
                - Dictionary containing weather data if successful
                - Error message string if failed, None otherwise
                
        Example:
            >>> api = WeatherAPI("your_api_key")
            >>> data, error = api.get_current_weather("London")
            >>> if error is None:
            ...     print(f"Temperature: {data['main']['temp']}°C")
        """
        try:
            # Prepare API request parameters
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'  # Use metric units (Celsius, m/s)
            }
            
            # Make API request with timeout
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=10
            )
            
            # Check for HTTP errors
            response.raise_for_status()
            
            # Parse and return JSON data
            data = response.json()
            return self._normalize_current_weather(data), None
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return None, f"City '{city}' not found. Please check the spelling."
            elif response.status_code == 401:
                return None, "Invalid API key. Please check your configuration."
            else:
                return None, f"HTTP Error: {str(e)}"
                
        except requests.exceptions.ConnectionError:
            return None, "Connection error. Please check your internet connection."
            
        except requests.exceptions.Timeout:
            return None, "Request timed out. Please try again."
            
        except requests.exceptions.RequestException as e:
            return None, f"An error occurred: {str(e)}"
            
        except json.JSONDecodeError:
            return None, "Invalid response from weather service."
    
    def get_forecast(self, city: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Fetch 7-day weather forecast for a specified city.
        
        Args:
            city (str): Name of the city to fetch forecast for
            
        Returns:
            Tuple[Optional[Dict], Optional[str]]:
                - Dictionary containing forecast data if successful
                - Error message string if failed, None otherwise
        """
        try:
            # First get coordinates from city name
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            current_data = response.json()
            
            # Extract coordinates
            lat = current_data['coord']['lat']
            lon = current_data['coord']['lon']
            
            # Get 5-day forecast (free tier)
            forecast_params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            forecast_response = requests.get(
                self.forecast_url,
                params=forecast_params,
                timeout=10
            )
            forecast_response.raise_for_status()
            
            forecast_data = forecast_response.json()
            return self._normalize_forecast(forecast_data), None
            
        except requests.exceptions.RequestException as e:
            return None, f"Failed to fetch forecast: {str(e)}"
        except (KeyError, json.JSONDecodeError) as e:
            return None, f"Error parsing forecast data: {str(e)}"
    
    def _normalize_current_weather(self, data: Dict) -> Dict:
        """
        Normalize and structure current weather API response.
        
        Args:
            data (Dict): Raw API response data
            
        Returns:
            Dict: Normalized weather data with consistent structure
        """
        try:
            normalized = {
                'city': data.get('name', 'Unknown'),
                'country': data.get('sys', {}).get('country', ''),
                'temperature': round(data.get('main', {}).get('temp', 0), 1),
                'feels_like': round(data.get('main', {}).get('feels_like', 0), 1),
                'humidity': data.get('main', {}).get('humidity', 0),
                'pressure': data.get('main', {}).get('pressure', 0),
                'wind_speed': round(data.get('wind', {}).get('speed', 0), 1),
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'description': data.get('weather', [{}])[0].get('description', 'N/A').title(),
                'icon': data.get('weather', [{}])[0].get('icon', '01d'),
                'sunrise': datetime.fromtimestamp(
                    data.get('sys', {}).get('sunrise', 0),
                    tz=timezone.utc
                ).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(
                    data.get('sys', {}).get('sunset', 0),
                    tz=timezone.utc
                ).strftime('%H:%M'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            return normalized
        except Exception as e:
            # Return minimal data structure if normalization fails
            return {
                'city': data.get('name', 'Unknown'),
                'error': f'Data normalization error: {str(e)}'
            }
    
    def _normalize_forecast(self, data: Dict) -> Dict:
        """
        Normalize and structure forecast API response.
        
        Args:
            data (Dict): Raw forecast API response
            
        Returns:
            Dict: Normalized forecast data grouped by day
        """
        try:
            forecast_list = []
            daily_data = {}
            
            # Process each forecast entry (3-hour intervals)
            for item in data.get('list', []):
                date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                temp = item['main']['temp']
                humidity = item['main']['humidity']
                description = item['weather'][0]['description']
                
                if date not in daily_data:
                    daily_data[date] = {
                        'temps': [],
                        'humidity': [],
                        'descriptions': []
                    }
                
                daily_data[date]['temps'].append(temp)
                daily_data[date]['humidity'].append(humidity)
                daily_data[date]['descriptions'].append(description)
            
            # Aggregate daily data
            for date, values in sorted(daily_data.items())[:7]:  # Limit to 7 days
                forecast_list.append({
                    'date': date,
                    'temp_min': round(min(values['temps']), 1),
                    'temp_max': round(max(values['temps']), 1),
                    'temp_avg': round(sum(values['temps']) / len(values['temps']), 1),
                    'humidity_avg': round(sum(values['humidity']) / len(values['humidity']), 1),
                    'description': max(set(values['descriptions']), 
                                     key=values['descriptions'].count)
                })
            
            return {
                'city': data.get('city', {}).get('name', 'Unknown'),
                'forecast': forecast_list
            }
            
        except Exception as e:
            return {
                'error': f'Forecast normalization error: {str(e)}',
                'forecast': []
            }
    
    def validate_api_key(self) -> bool:
        """
        Validate that the API key is working.
        
        Returns:
            bool: True if API key is valid, False otherwise
        """
        try:
            params = {
                'q': 'London',
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            return response.status_code == 200
        except:
            return False