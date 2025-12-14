# # src/ui.py
# """
# User Interface Module
# =====================
# Handles all Streamlit UI components and page layouts for the Weather Dashboard.

# Features:
# - Modern, responsive layout
# - Weather search interface
# - Current weather display
# - Forecast visualization
# - Search history management
# - Analytics dashboard
# - Settings and configuration

# Dependencies:
#     - streamlit: Web UI framework
#     - All other modules (api, charts, utils)
# """

# import streamlit as st
# from typing import Optional
# import os
# from datetime import datetime

# from src.api import WeatherAPI
# from src.charts import (
#     create_temperature_line_chart,
#     create_humidity_bar_chart,
#     create_interactive_temperature_chart,
#     create_forecast_comparison_chart,
#     create_temperature_heatmap
# )
# from src.utils import (
#     save_search_to_history,
#     load_search_history,
#     clear_search_history,
#     analyze_forecast_data,
#     get_weather_icon_url,
#     celsius_to_fahrenheit,
#     get_data_summary,
#     export_data_to_csv
# )

# class WeatherUI:
#     """
#     Main UI class for the Weather Dashboard application.
    
#     Manages all UI components, user interactions, and data flow
#     between the interface and backend services.
#     """
    
#     def __init__(self):
#         """Initialize the Weather UI with API configuration."""
#         self.initialize_session_state()
#         self.api_key = self.get_api_key()
#         if self.api_key:
#             self.weather_api = WeatherAPI(self.api_key)
#         else:
#             self.weather_api = None
    
#     def initialize_session_state(self) -> None:
#         """
#         Initialize Streamlit session state variables.
        
#         Session state maintains data across reruns and user interactions.
#         """
#         if 'current_weather' not in st.session_state:
#             st.session_state.current_weather = None
#         if 'forecast_data' not in st.session_state:
#             st.session_state.forecast_data = None
#         if 'selected_city' not in st.session_state:
#             st.session_state.selected_city = None
#         if 'temp_unit' not in st.session_state:
#             st.session_state.temp_unit = 'Celsius'
#         if 'api_key_input' not in st.session_state:
#             st.session_state.api_key_input = ''
    
#     def get_api_key(self) -> Optional[str]:
#         """
#         Retrieve API key from environment or session state.
        
#         Returns:
#             Optional[str]: API key if available, None otherwise
#         """
#         # First try environment variable
#         api_key = os.getenv('OPENWEATHER_API_KEY')
        
#         # Then try session state
#         if not api_key and st.session_state.api_key_input:
#             api_key = st.session_state.api_key_input
        
#         return api_key
    
#     def render(self) -> None:
#         """
#         Main render method that displays the entire UI.
        
#         This method orchestrates all UI components and handles
#         the overall page layout.
#         """
#         # Display header
#         self.render_header()
        
#         # Check if API key is configured
#         if not self.api_key:
#             self.render_api_key_setup()
#             return
        
#         # Main content area with sidebar
#         with st.sidebar:
#             self.render_sidebar()
        
#         # Main content tabs
#         tab1, tab2, tab3, tab4 = st.tabs([
#             "🏠 Current Weather",
#             "📊 Analytics",
#             "📈 Charts",
#             "🕐 History"
#         ])
        
#         with tab1:
#             self.render_current_weather_tab()
        
#         with tab2:
#             self.render_analytics_tab()
        
#         with tab3:
#             self.render_charts_tab()
        
#         with tab4:
#             self.render_history_tab()
    
#     def render_header(self) -> None:
#         """Render the application header with title and description."""
#         st.markdown("""
#             <div style='text-align: center; padding: 1rem 0;'>
#                 <h1 style='color: #667eea; margin-bottom: 0;'>
#                     🌤️ Weather Dashboard
#                 </h1>
#                 <p style='color: #666; font-size: 1.1rem;'>
#                     Real-time weather data, forecasts, and analytics
#                 </p>
#             </div>
#         """, unsafe_allow_html=True)
    
#     def render_api_key_setup(self) -> None:
#         """Render API key configuration interface."""
#         st.warning("⚠️ API Key Required")
        
#         st.markdown("""
#         ### 🔑 Setup Instructions
        
#         1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
#         2. Sign up for a free account
#         3. Copy your API key
#         4. Enter it below
#         """)
        
#         col1, col2 = st.columns([3, 1])
        
#         with col1:
#             api_key = st.text_input(
#                 "Enter your OpenWeatherMap API Key:",
#                 type="password",
#                 placeholder="Enter API key here..."
#             )
        
#         with col2:
#             st.write("")  # Spacing
#             st.write("")  # Spacing
#             if st.button("Save API Key", type="primary"):
#                 if api_key:
#                     st.session_state.api_key_input = api_key
#                     self.api_key = api_key
#                     self.weather_api = WeatherAPI(api_key)
#                     st.success("✅ API key saved! Reloading...")
#                     st.rerun()
#                 else:
#                     st.error("Please enter a valid API key")
        
#         st.info("💡 **Tip:** You can also set the `OPENWEATHER_API_KEY` environment variable")
    
#     def render_sidebar(self) -> None:
#         """Render sidebar with search, settings, and navigation."""
#         st.title("🔍 Search Weather")
        
#         # City search input
#         city_input = st.text_input(
#             "Enter city name:",
#             placeholder="e.g., London, New York, Tokyo",
#             help="Enter a city name to get weather information"
#         )
        
#         # Search button
#         if st.button("🔎 Search", type="primary", use_container_width=True):
#             if city_input:
#                 self.search_weather(city_input)
#             else:
#                 st.warning("Please enter a city name")
        
#         st.divider()
        
#         # Quick access to recent searches
#         st.subheader("📍 Recent Searches")
#         history = load_search_history()
        
#         if history:
#             for entry in history[:5]:  # Show last 5
#                 col1, col2 = st.columns([3, 1])
#                 with col1:
#                     if st.button(
#                         f"{entry['city']} - {entry['temperature']}°C",
#                         key=f"history_{entry['city']}",
#                         use_container_width=True
#                     ):
#                         self.search_weather(entry['city'])
#                 with col2:
#                     st.caption(entry.get('timestamp', '')[:10])
#         else:
#             st.info("No recent searches")
        
#         st.divider()
        
#         # Settings
#         st.subheader("⚙️ Settings")
        
#         st.session_state.temp_unit = st.selectbox(
#             "Temperature Unit:",
#             ["Celsius", "Fahrenheit"],
#             index=0 if st.session_state.temp_unit == "Celsius" else 1
#         )
        
#         # Clear history button
#         if st.button("🗑️ Clear History", use_container_width=True):
#             if clear_search_history():
#                 st.success("History cleared!")
#                 st.rerun()
        
#         # App info
#         st.divider()
#         st.caption("Weather Dashboard v1.0")
#         st.caption("Data from OpenWeatherMap")
    
#     def render_current_weather_tab(self) -> None:
#         """Render the current weather display tab."""
#         if not st.session_state.current_weather:
#             st.info("👋 Search for a city to see current weather conditions")
            
#             # Show example cities
#             st.subheader("🌍 Try These Cities:")
            
#             col1, col2, col3, col4 = st.columns(4)
            
#             example_cities = ["London", "New York", "Tokyo", "Paris"]
#             columns = [col1, col2, col3, col4]
            
#             for city, col in zip(example_cities, columns):
#                 with col:
#                     if st.button(city, use_container_width=True):
#                         self.search_weather(city)
            
#             return
        
#         weather = st.session_state.current_weather
        
#         # Weather header with icon
#         col1, col2 = st.columns([1, 4])
        
#         with col1:
#             icon_url = get_weather_icon_url(weather.get('icon', '01d'))
#             st.image(icon_url, width=100)
        
#         with col2:
#             st.markdown(f"""
#                 <div style='padding: 1rem 0;'>
#                     <h2 style='margin: 0; color: #667eea;'>
#                         {weather['city']}, {weather['country']}
#                     </h2>
#                     <p style='font-size: 1.2rem; margin: 0.5rem 0; color: #666;'>
#                         {weather['description']}
#                     </p>
#                 </div>
#             """, unsafe_allow_html=True)
        
#         st.divider()
        
#         # Main temperature display
#         temp = weather['temperature']
#         feels_like = weather['feels_like']
        
#         if st.session_state.temp_unit == "Fahrenheit":
#             temp = celsius_to_fahrenheit(temp)
#             feels_like = celsius_to_fahrenheit(feels_like)
#             unit = "°F"
#         else:
#             unit = "°C"
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown(f"""
#                 <div class='weather-card'>
#                     <h1 style='font-size: 4rem; margin: 0;'>{temp}{unit}</h1>
#                     <p style='font-size: 1.2rem; margin: 0;'>Feels like {feels_like}{unit}</p>
#                 </div>
#             """, unsafe_allow_html=True)
        
#         with col2:
#             st.markdown(f"""
#                 <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px;'>
#                     <h3 style='margin-top: 0;'>🌅 Sun Times</h3>
#                     <p><strong>Sunrise:</strong> {weather['sunrise']}</p>
#                     <p><strong>Sunset:</strong> {weather['sunset']}</p>
#                 </div>
#             """, unsafe_allow_html=True)
        
#         st.divider()
        
#         # Weather metrics in columns
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.metric(
#                 label="💧 Humidity",
#                 value=f"{weather['humidity']}%"
#             )
        
#         with col2:
#             st.metric(
#                 label="🌪️ Wind Speed",
#                 value=f"{weather['wind_speed']} m/s"
#             )
        
#         with col3:
#             st.metric(
#                 label="🔽 Pressure",
#                 value=f"{weather['pressure']} hPa"
#             )
        
#         with col4:
#             st.metric(
#                 label="👁️ Visibility",
#                 value=f"{weather['visibility']} km"
#             )
        
#         # Forecast section
#         if st.session_state.forecast_data:
#             st.divider()
#             st.subheader("📅 7-Day Forecast")
            
#             forecast = st.session_state.forecast_data['forecast']
            
#             # Display forecast cards
#             cols = st.columns(min(7, len(forecast)))
            
#             for i, day in enumerate(forecast):
#                 if i < len(cols):
#                     with cols[i]:
#                         date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
#                         day_name = date_obj.strftime('%a')
                        
#                         st.markdown(f"""
#                             <div style='text-align: center; padding: 1rem; 
#                                  background: #f8f9fa; border-radius: 8px;'>
#                                 <p style='font-weight: bold; margin: 0;'>{day_name}</p>
#                                 <p style='font-size: 0.9rem; color: #666; margin: 0.5rem 0;'>
#                                     {date_obj.strftime('%b %d')}
#                                 </p>
#                                 <p style='font-size: 1.5rem; color: #667eea; margin: 0.5rem 0;'>
#                                     {day['temp_max']}°C
#                                 </p>
#                                 <p style='font-size: 1rem; color: #4299e1; margin: 0;'>
#                                     {day['temp_min']}°C
#                                 </p>
#                                 <p style='font-size: 0.85rem; color: #666; margin: 0.5rem 0;'>
#                                     {day['description'].title()}
#                                 </p>
#                             </div>
#                         """, unsafe_allow_html=True)
    
#     def render_analytics_tab(self) -> None:
#         """Render analytics and statistics tab."""
#         if not st.session_state.forecast_data:
#             st.info("Search for a city to see weather analytics")
#             return
        
#         forecast = st.session_state.forecast_data['forecast']
#         analysis = analyze_forecast_data(forecast)
        
#         st.subheader("📊 Weather Analytics")
        
#         # Key metrics
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.metric(
#                 label="🌡️ Average Temperature",
#                 value=f"{analysis['temp_avg']}°C",
#                 delta=None
#             )
        
#         with col2:
#             st.metric(
#                 label="📈 Maximum",
#                 value=f"{analysis['temp_max']}°C",
#                 delta=f"+{round(analysis['temp_max'] - analysis['temp_avg'], 1)}°C"
#             )
        
#         with col3:
#             st.metric(
#                 label="📉 Minimum",
#                 value=f"{analysis['temp_min']}°C",
#                 delta=f"{round(analysis['temp_min'] - analysis['temp_avg'], 1)}°C"
#             )
        
#         with col4:
#             st.metric(
#                 label="💧 Avg Humidity",
#                 value=f"{analysis['humidity_avg']}%"
#             )
        
#         st.divider()
        
#         # Trend analysis
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.markdown(f"""
#                 <div style='background: #e6f4ea; padding: 1.5rem; border-radius: 10px; 
#                      border-left: 5px solid #48bb78;'>
#                     <h3 style='margin-top: 0; color: #2d5f3f;'>
#                         📈 Temperature Trend
#                     </h3>
#                     <p style='font-size: 1.5rem; font-weight: bold; color: #2d5f3f;'>
#                         {analysis['trend']}
#                     </p>
#                     <p style='color: #5f8d70;'>
#                         Slope: {analysis['slope']}°C per day
#                     </p>
#                 </div>
#             """, unsafe_allow_html=True)
        
#         with col2:
#             st.markdown(f"""
#                 <div style='background: #e6f7ff; padding: 1.5rem; border-radius: 10px; 
#                      border-left: 5px solid #4299e1;'>
#                     <h3 style='margin-top: 0; color: #2b5f7f;'>
#                         📊 Variability
#                     </h3>
#                     <p style='color: #5f8fb3;'>
#                         <strong>Temp Std Dev:</strong> {analysis['temp_std']}°C
#                     </p>
#                     <p style='color: #5f8fb3;'>
#                         <strong>Humidity Std Dev:</strong> {analysis['humidity_std']}%
#                     </p>
#                 </div>
#             """, unsafe_allow_html=True)
        
#         st.divider()
        
#         # Data summary
#         st.subheader("📝 Summary")
#         summary = get_data_summary(forecast)
#         st.text(summary)
        
#         # Export options
#         st.divider()
#         st.subheader("💾 Export Data")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             if st.button("📥 Export to CSV", use_container_width=True):
#                 filename = f"weather_{st.session_state.selected_city}_{datetime.now().strftime('%Y%m%d')}.csv"
#                 if export_data_to_csv(st.session_state.forecast_data, filename):
#                     st.success(f"✅ Data exported to data/{filename}")
#                 else:
#                     st.error("Failed to export data")
        
#         with col2:
#             st.info("CSV file will be saved to the data/ directory")
    
#     def render_charts_tab(self) -> None:
#         """Render charts and visualizations tab."""
#         if not st.session_state.forecast_data:
#             st.info("Search for a city to see weather charts")
#             return
        
#         forecast = st.session_state.forecast_data['forecast']
        
#         st.subheader("📈 Weather Visualizations")
        
#         # Chart type selector
#         chart_type = st.selectbox(
#             "Select Chart Type:",
#             [
#                 "Interactive Temperature Chart",
#                 "Static Temperature Line Chart",
#                 "Humidity Bar Chart",
#                 "Temperature vs Humidity Comparison",
#                 "Temperature Heatmap"
#             ]
#         )
        
#         st.divider()
        
#         try:
#             if chart_type == "Interactive Temperature Chart":
#                 st.plotly_chart(
#                     create_interactive_temperature_chart(forecast),
#                     use_container_width=True
#                 )
#                 st.info("💡 Hover over the chart to see detailed information")
            
#             elif chart_type == "Static Temperature Line Chart":
#                 fig = create_temperature_line_chart(forecast)
#                 st.pyplot(fig)
#                 st.info("📊 Static chart showing temperature trends")
            
#             elif chart_type == "Humidity Bar Chart":
#                 fig = create_humidity_bar_chart(forecast)
#                 st.pyplot(fig)
#                 st.info("💧 Humidity levels across the forecast period")
            
#             elif chart_type == "Temperature vs Humidity Comparison":
#                 st.plotly_chart(
#                     create_forecast_comparison_chart(forecast),
#                     use_container_width=True
#                 )
#                 st.info("📊 Dual-axis comparison of temperature and humidity")
            
#             elif chart_type == "Temperature Heatmap":
#                 st.plotly_chart(
#                     create_temperature_heatmap(forecast),
#                     use_container_width=True
#                 )
#                 st.info("🔥 Heatmap visualization of temperature ranges")
        
#         except Exception as e:
#             st.error(f"Error creating chart: {str(e)}")
    
#     def render_history_tab(self) -> None:
#         """Render search history tab."""
#         st.subheader("🕐 Search History")
        
#         history = load_search_history()
        
#         if not history:
#             st.info("No search history available. Start searching to build your history!")
#             return
        
#         st.write(f"Total searches: **{len(history)}**")
        
#         # Display history in a table format
#         for i, entry in enumerate(history):
#             with st.expander(
#                 f"🏙️ {entry['city']} - {entry['temperature']}°C",
#                 expanded=(i == 0)
#             ):
#                 col1, col2, col3 = st.columns(3)
                
#                 with col1:
#                     st.write("**City:**", entry['city'])
#                 with col2:
#                     st.write("**Temperature:**", f"{entry['temperature']}°C")
#                 with col3:
#                     st.write("**Weather:**", entry['description'])
                
#                 st.write("**Searched at:**", entry['timestamp'])
                
#                 if st.button(f"🔍 Search Again", key=f"search_again_{i}"):
#                     self.search_weather(entry['city'])
        
#         st.divider()
        
#         # Clear history button
#         col1, col2 = st.columns([1, 3])
#         with col1:
#             if st.button("🗑️ Clear All History", type="secondary"):
#                 if clear_search_history():
#                     st.success("History cleared!")
#                     st.rerun()
    
#     def search_weather(self, city: str) -> None:
#         """
#         Search for weather data for a given city.
        
#         Args:
#             city (str): Name of the city to search
#         """
#         with st.spinner(f"🔍 Searching weather for {city}..."):
#             # Get current weather
#             current_data, error = self.weather_api.get_current_weather(city)
            
#             if error:
#                 st.error(f"❌ {error}")
#                 return
            
#             # Get forecast
#             forecast_data, forecast_error = self.weather_api.get_forecast(city)
            
#             if forecast_error:
#                 st.warning(f"⚠️ Forecast unavailable: {forecast_error}")
#                 forecast_data = None
            
#             # Update session state
#             st.session_state.current_weather = current_data
#             st.session_state.forecast_data = forecast_data
#             st.session_state.selected_city = city
            
#             # Save to history
#             save_search_to_history(city, current_data)
            
#             st.success(f"✅ Weather data loaded for {city}")
#             st.rerun()




# src/ui.py
"""
User Interface Module
=====================
Handles all Streamlit UI components and page layouts for the Weather Dashboard.

Features:
- Modern, responsive layout
- Weather search interface
- Current weather display
- Forecast visualization
- Search history management
- Analytics dashboard
- Settings and configuration

Dependencies:
    - streamlit: Web UI framework
    - All other modules (api, charts, utils)
"""

import streamlit as st
from typing import Optional
import os
from datetime import datetime

from src.api import WeatherAPI
from src.charts import (
    create_temperature_line_chart,
    create_humidity_bar_chart,
    create_interactive_temperature_chart,
    create_forecast_comparison_chart,
    create_temperature_heatmap
)
from src.utils import (
    save_search_to_history,
    load_search_history,
    clear_search_history,
    analyze_forecast_data,
    get_weather_icon_url,
    celsius_to_fahrenheit,
    get_data_summary,
    export_data_to_csv
)

class WeatherUI:
    """
    Main UI class for the Weather Dashboard application.
    
    Manages all UI components, user interactions, and data flow
    between the interface and backend services.
    """
    
    def __init__(self):
        """Initialize the Weather UI with API configuration."""
        self.initialize_session_state()
        self.api_key = self.get_api_key()
        if self.api_key:
            self.weather_api = WeatherAPI(self.api_key)
        else:
            self.weather_api = None
    
    def initialize_session_state(self) -> None:
        """
        Initialize Streamlit session state variables.
        
        Session state maintains data across reruns and user interactions.
        """
        if 'current_weather' not in st.session_state:
            st.session_state.current_weather = None
        if 'forecast_data' not in st.session_state:
            st.session_state.forecast_data = None
        if 'selected_city' not in st.session_state:
            st.session_state.selected_city = None
        if 'temp_unit' not in st.session_state:
            st.session_state.temp_unit = 'Celsius'
        if 'api_key_input' not in st.session_state:
            st.session_state.api_key_input = ''
    
    def get_api_key(self) -> Optional[str]:
        """
        Retrieve API key from environment or session state.
        
        Returns:
            Optional[str]: API key if available, None otherwise
        """
        # First try environment variable (.env file)
        api_key = os.getenv('OPENWEATHER_API_KEY')
        
        # If not in .env, check if we have it saved in data/config.json
        if not api_key:
            try:
                config_path = os.path.join('data', 'config.json')
                if os.path.exists(config_path):
                    import json
                    with open(config_path, 'r') as f:
                        config = json.load(f)
                        api_key = config.get('api_key', '')
            except Exception as e:
                pass
        
        # Finally try session state
        if not api_key and st.session_state.api_key_input:
            api_key = st.session_state.api_key_input
        
        return api_key
    
    def render(self) -> None:
        """
        Main render method that displays the entire UI.
        
        This method orchestrates all UI components and handles
        the overall page layout.
        """
        # Display header
        self.render_header()
        
        # Check if API key is configured
        if not self.api_key:
            self.render_api_key_setup()
            return
        
        # Main content area with sidebar
        with st.sidebar:
            self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏠 Current Weather",
            "📊 Analytics",
            "📈 Charts",
            "🕐 History"
        ])
        
        with tab1:
            self.render_current_weather_tab()
        
        with tab2:
            self.render_analytics_tab()
        
        with tab3:
            self.render_charts_tab()
        
        with tab4:
            self.render_history_tab()
    
    def render_header(self) -> None:
        """Render the application header with title and description."""
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0;'>
                <h1 style='color: #667eea; margin-bottom: 0;'>
                    🌤️ Weather Dashboard
                </h1>
                <p style='color: #666; font-size: 1.1rem;'>
                    Real-time weather data, forecasts, and analytics
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_api_key_setup(self) -> None:
        """Render API key configuration interface."""
        st.warning("⚠️ API Key Required")
        
        st.markdown("""
        ### 🔑 Setup Instructions
        
        1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
        2. Sign up for a free account
        3. Copy your API key
        4. Enter it below
        """)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            api_key = st.text_input(
                "Enter your OpenWeatherMap API Key:",
                type="password",
                placeholder="Enter API key here..."
            )
        
        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("Save API Key", type="primary"):
                if api_key:
                    st.session_state.api_key_input = api_key
                    self.api_key = api_key
                    self.weather_api = WeatherAPI(api_key)
                    
                    # Save to config file for persistence
                    try:
                        import json
                        config_path = os.path.join('data', 'config.json')
                        os.makedirs('data', exist_ok=True)
                        with open(config_path, 'w') as f:
                            json.dump({'api_key': api_key}, f)
                    except Exception as e:
                        pass
                    
                    st.success("✅ API key saved! Reloading...")
                    st.rerun()
                else:
                    st.error("Please enter a valid API key")
        
        st.info("💡 **Tip:** You can also set the `OPENWEATHER_API_KEY` environment variable")
    
    def render_sidebar(self) -> None:
        """Render sidebar with search, settings, and navigation."""
        st.title("🔍 Search Weather")
        
        # City search input
        city_input = st.text_input(
            "Enter city name:",
            placeholder="e.g., London, New York, Tokyo",
            help="Enter a city name to get weather information"
        )
        
        # Search button
        if st.button("🔎 Search", type="primary", use_container_width=True):
            if city_input:
                self.search_weather(city_input)
            else:
                st.warning("Please enter a city name")
        
        st.divider()
        
        # Quick access to recent searches
        st.subheader("📍 Recent Searches")
        history = load_search_history()
        
        if history:
            for entry in history[:5]:  # Show last 5
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(
                        f"{entry['city']} - {entry['temperature']}°C",
                        key=f"history_{entry['city']}",
                        use_container_width=True
                    ):
                        self.search_weather(entry['city'])
                with col2:
                    st.caption(entry.get('timestamp', '')[:10])
        else:
            st.info("No recent searches")
        
        st.divider()
        
        # Settings
        st.subheader("⚙️ Settings")
        
        st.session_state.temp_unit = st.selectbox(
            "Temperature Unit:",
            ["Celsius", "Fahrenheit"],
            index=0 if st.session_state.temp_unit == "Celsius" else 1
        )
        
        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            if clear_search_history():
                st.success("History cleared!")
                st.rerun()
        
        # App info
        st.divider()
        st.caption("Weather Dashboard v1.0")
        st.caption("Data from OpenWeatherMap")
    
    def render_current_weather_tab(self) -> None:
        """Render the current weather display tab."""
        if not st.session_state.current_weather:
            st.info("👋 Search for a city to see current weather conditions")
            
            # Show example cities
            st.subheader("🌍 Try These Cities:")
            
            col1, col2, col3, col4 = st.columns(4)
            
            example_cities = ["London", "New York", "Tokyo", "Paris"]
            columns = [col1, col2, col3, col4]
            
            for city, col in zip(example_cities, columns):
                with col:
                    if st.button(city, use_container_width=True):
                        self.search_weather(city)
            
            return
        
        weather = st.session_state.current_weather
        
        # Weather header with icon
        col1, col2 = st.columns([1, 4])
        
        with col1:
            icon_url = get_weather_icon_url(weather.get('icon', '01d'))
            st.image(icon_url, width=100)
        
        with col2:
            st.markdown(f"""
                <div style='padding: 1rem 0;'>
                    <h2 style='margin: 0; color: #667eea;'>
                        {weather['city']}, {weather['country']}
                    </h2>
                    <p style='font-size: 1.2rem; margin: 0.5rem 0; color: #666;'>
                        {weather['description']}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Main temperature display
        temp = weather['temperature']
        feels_like = weather['feels_like']
        
        if st.session_state.temp_unit == "Fahrenheit":
            temp = celsius_to_fahrenheit(temp)
            feels_like = celsius_to_fahrenheit(feels_like)
            unit = "°F"
        else:
            unit = "°C"
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div class='weather-card'>
                    <h1 style='font-size: 4rem; margin: 0;'>{temp}{unit}</h1>
                    <p style='font-size: 1.2rem; margin: 0;'>Feels like {feels_like}{unit}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; color:#333;'>
                    <h3 style='margin-top: 0;'>🌅 Sun Times</h3>
                    <p><strong>Sunrise:</strong> {weather['sunrise']}</p>
                    <p><strong>Sunset:</strong> {weather['sunset']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Weather metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>💧 Humidity</p>
                    <p style='color: #333; font-size: 2rem; font-weight: bold; margin: 10px 0;'>{weather['humidity']}%</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>🌪️ Wind Speed</p>
                    <p style='color: #333; font-size: 2rem; font-weight: bold; margin: 10px 0;'>{weather['wind_speed']} m/s</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>🔽 Pressure</p>
                    <p style='color: #333; font-size: 2rem; font-weight: bold; margin: 10px 0;'>{weather['pressure']} hPa</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center;'>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>👁️ Visibility</p>
                    <p style='color: #333; font-size: 2rem; font-weight: bold; margin: 10px 0;'>{weather['visibility']} km</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Forecast section
        if st.session_state.forecast_data:
            st.divider()
            st.subheader("📅 7-Day Forecast")
            
            forecast = st.session_state.forecast_data['forecast']
            
            # Display forecast cards
            cols = st.columns(min(7, len(forecast)))
            
            for i, day in enumerate(forecast):
                if i < len(cols):
                    with cols[i]:
                        date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
                        day_name = date_obj.strftime('%a')
                        
                        st.markdown(f"""
                            <div style='text-align: center; padding: 1rem; 
                                 background: #f8f9fa; border-radius: 8px;'>
                                <p style='font-weight: bold; margin: 0;'>{day_name}</p>
                                <p style='font-size: 0.9rem; color: #666; margin: 0.5rem 0;'>
                                    {date_obj.strftime('%b %d')}
                                </p>
                                <p style='font-size: 1.5rem; color: #667eea; margin: 0.5rem 0;'>
                                    {day['temp_max']}°C
                                </p>
                                <p style='font-size: 1rem; color: #4299e1; margin: 0;'>
                                    {day['temp_min']}°C
                                </p>
                                <p style='font-size: 0.85rem; color: #666; margin: 0.5rem 0;'>
                                    {day['description'].title()}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
    
    def render_analytics_tab(self) -> None:
        """Render analytics and statistics tab."""
        if not st.session_state.forecast_data:
            st.info("Search for a city to see weather analytics")
            return
        
        forecast = st.session_state.forecast_data['forecast']
        analysis = analyze_forecast_data(forecast)
        
        st.subheader("📊 Weather Analytics")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>🌡️ Average Temperature</p>
                    <p style='color: #667eea; font-size: 2.5rem; font-weight: bold; margin: 10px 0;'>{analysis['temp_avg']}°C</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            delta = round(analysis['temp_max'] - analysis['temp_avg'], 1)
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>📈 Maximum</p>
                    <p style='color: #fc8181; font-size: 2.5rem; font-weight: bold; margin: 10px 0;'>{analysis['temp_max']}°C</p>
                    <p style='color: #48bb78; font-size: 0.85rem; margin: 0;'>+{delta}°C from avg</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            delta = round(analysis['temp_min'] - analysis['temp_avg'], 1)
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>📉 Minimum</p>
                    <p style='color: #4299e1; font-size: 2.5rem; font-weight: bold; margin: 10px 0;'>{analysis['temp_min']}°C</p>
                    <p style='color: #e53e3e; font-size: 0.85rem; margin: 0;'>{delta}°C from avg</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div style='background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <p style='color: #666; font-size: 0.9rem; margin: 0;'>💧 Avg Humidity</p>
                    <p style='color: #4299e1; font-size: 2.5rem; font-weight: bold; margin: 10px 0;'>{analysis['humidity_avg']}%</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Trend analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div style='background: #e6f4ea; padding: 1.5rem; border-radius: 10px; 
                     border-left: 5px solid #48bb78;'>
                    <h3 style='margin-top: 0; color: #2d5f3f;'>
                        📈 Temperature Trend
                    </h3>
                    <p style='font-size: 1.5rem; font-weight: bold; color: #2d5f3f;'>
                        {analysis['trend']}
                    </p>
                    <p style='color: #5f8d70;'>
                        Slope: {analysis['slope']}°C per day
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='background: #e6f7ff; padding: 1.5rem; border-radius: 10px; 
                     border-left: 5px solid #4299e1;'>
                    <h3 style='margin-top: 0; color: #2b5f7f;'>
                        📊 Variability
                    </h3>
                    <p style='color: #5f8fb3;'>
                        <strong>Temp Std Dev:</strong> {analysis['temp_std']}°C
                    </p>
                    <p style='color: #5f8fb3;'>
                        <strong>Humidity Std Dev:</strong> {analysis['humidity_std']}%
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Data summary
        st.subheader("📝 Summary")
        summary = get_data_summary(forecast)
        st.text(summary)
        
        # Export options
        st.divider()
        st.subheader("💾 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export to CSV", use_container_width=True):
                filename = f"weather_{st.session_state.selected_city}_{datetime.now().strftime('%Y%m%d')}.csv"
                if export_data_to_csv(st.session_state.forecast_data, filename):
                    st.success(f"✅ Data exported to data/{filename}")
                else:
                    st.error("Failed to export data")
        
        with col2:
            st.info("CSV file will be saved to the data/ directory")
    
    def render_charts_tab(self) -> None:
        """Render charts and visualizations tab."""
        if not st.session_state.forecast_data:
            st.info("Search for a city to see weather charts")
            return
        
        forecast = st.session_state.forecast_data['forecast']
        
        st.subheader("📈 Weather Visualizations")
        
        # Chart type selector
        chart_type = st.selectbox(
            "Select Chart Type:",
            [
                "Interactive Temperature Chart",
                "Static Temperature Line Chart",
                "Humidity Bar Chart",
                "Temperature vs Humidity Comparison",
                "Temperature Heatmap"
            ]
        )
        
        st.divider()
        
        try:
            if chart_type == "Interactive Temperature Chart":
                st.plotly_chart(
                    create_interactive_temperature_chart(forecast),
                    use_container_width=True
                )
                st.info("💡 Hover over the chart to see detailed information")
            
            elif chart_type == "Static Temperature Line Chart":
                fig = create_temperature_line_chart(forecast)
                st.pyplot(fig)
                st.info("📊 Static chart showing temperature trends")
            
            elif chart_type == "Humidity Bar Chart":
                fig = create_humidity_bar_chart(forecast)
                st.pyplot(fig)
                st.info("💧 Humidity levels across the forecast period")
            
            elif chart_type == "Temperature vs Humidity Comparison":
                st.plotly_chart(
                    create_forecast_comparison_chart(forecast),
                    use_container_width=True
                )
                st.info("📊 Dual-axis comparison of temperature and humidity")
            
            elif chart_type == "Temperature Heatmap":
                st.plotly_chart(
                    create_temperature_heatmap(forecast),
                    use_container_width=True
                )
                st.info("🔥 Heatmap visualization of temperature ranges")
        
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
    
    def render_history_tab(self) -> None:
        """Render search history tab."""
        st.subheader("🕐 Search History")
        
        history = load_search_history()
        
        if not history:
            st.info("No search history available. Start searching to build your history!")
            return
        
        st.write(f"Total searches: **{len(history)}**")
        
        # Display history in a table format
        for i, entry in enumerate(history):
            with st.expander(
                f"🏙️ {entry['city']} - {entry['temperature']}°C",
                expanded=(i == 0)
            ):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**City:**", entry['city'])
                with col2:
                    st.write("**Temperature:**", f"{entry['temperature']}°C")
                with col3:
                    st.write("**Weather:**", entry['description'])
                
                st.write("**Searched at:**", entry['timestamp'])
                
                if st.button(f"🔍 Search Again", key=f"search_again_{i}"):
                    self.search_weather(entry['city'])
        
        st.divider()
        
        # Clear history button
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🗑️ Clear All History", type="secondary"):
                if clear_search_history():
                    st.success("History cleared!")
                    st.rerun()
    
    def search_weather(self, city: str) -> None:
        """
        Search for weather data for a given city.
        
        Args:
            city (str): Name of the city to search
        """
        with st.spinner(f"🔍 Searching weather for {city}..."):
            # Get current weather
            current_data, error = self.weather_api.get_current_weather(city)
            
            if error:
                st.error(f"❌ {error}")
                return
            
            # Get forecast
            forecast_data, forecast_error = self.weather_api.get_forecast(city)
            
            if forecast_error:
                st.warning(f"⚠️ Forecast unavailable: {forecast_error}")
                forecast_data = None
            
            # Update session state
            st.session_state.current_weather = current_data
            st.session_state.forecast_data = forecast_data
            st.session_state.selected_city = city
            
            # Save to history
            save_search_to_history(city, current_data)
            
            st.success(f"✅ Weather data loaded for {city}")
            st.rerun()