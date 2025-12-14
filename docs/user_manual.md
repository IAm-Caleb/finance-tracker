📖 Weather Dashboard - User Manual
Table of Contents
Getting Started
Interface Overview
Searching for Weather
Understanding Current Weather
Using Analytics
Working with Charts
Managing Search History
Settings and Configuration
Troubleshooting
FAQ
1. Getting Started
First Time Setup
Install the Application
Follow the installation instructions in the README.md
Ensure Python 3.8+ is installed on your system
Install all required dependencies using pip install -r requirements.txt
Obtain an API Key
Visit OpenWeatherMap.org
Create a free account
Navigate to your API keys section
Copy your API key
Configure the Application
Option A: Create a .env file in the project root with:
     OPENWEATHER_API_KEY=your_api_key_here
Option B: Enter your API key directly in the application interface
Launch the Application
bash
   streamlit run main.py
The application will open in your default web browser
Default address: http://localhost:8501
2. Interface Overview
Main Components
Header
Title: Weather Dashboard with weather icon
Subtitle: Brief description of the application
Sidebar (Left Panel)
Search Box: Input field for city names
Search Button: Initiates weather search
Recent Searches: Quick access to last 5 searches
Settings: Temperature unit selection
Clear History: Button to remove all search history
Main Content Area (Tabs)
🏠 Current Weather: Real-time weather conditions
📊 Analytics: Statistical analysis and insights
📈 Charts: Visual data representations
🕐 History: Complete search history
3. Searching for Weather
Basic Search
Locate the Search Box
Found in the left sidebar
Look for "🔍 Search Weather" section
Enter City Name
Type the name of any city worldwide
Examples: "London", "New York", "Tokyo"
For better accuracy, include country: "London,UK"
Click Search Button
Click the blue "🔎 Search" button
Wait for the loading indicator
Results will appear automatically
Quick Search Options
Recent Searches

Click on any city in the "Recent Searches" list
Instantly reload previous search results
Limited to last 5 searches for quick access
Example Cities

When no search is active, example city buttons appear
One-click search for: London, New York, Tokyo, Paris
Search Tips
✅ DO:

Use major city names for best results
Check spelling carefully
Try different variations if city not found
Include country code for common city names
❌ DON'T:

Use abbreviations or acronyms
Include special characters unnecessarily
Search for very small towns (may not be in database)
4. Understanding Current Weather
Weather Header Section
City Information

City name and country code
Weather condition description (e.g., "Clear Sky", "Light Rain")
Weather icon representing current conditions
Main Temperature Display
Large Temperature Card (Purple gradient)

Current temperature in large numbers
"Feels like" temperature below
Unit changes based on settings (°C or °F)
Sun Times Card (Gray background)

Sunrise time (24-hour format)
Sunset time (24-hour format)
Weather Metrics (4 Columns)
💧 Humidity
Relative humidity percentage
Comfort level: 30-50% is ideal
🌪️ Wind Speed
Current wind speed in m/s
Higher values indicate stronger winds
🔽 Pressure
Atmospheric pressure in hPa (hectopascals)
Normal: ~1013 hPa at sea level
👁️ Visibility
How far you can see in kilometers
10 km is excellent visibility
7-Day Forecast Cards
Each card shows:

Day of the week (abbreviated)
Date (month and day)
Maximum temperature (larger, colored)
Minimum temperature (smaller, blue)
Weather description
5. Using Analytics
Overview Statistics (Top Row)
Four Key Metrics:

Average Temperature: Mean temperature over forecast period
Maximum: Highest temperature with delta from average
Minimum: Lowest temperature with delta from average
Average Humidity: Mean humidity percentage
Trend Analysis Cards
Temperature Trend (Green card)

Shows if temperatures are: Increasing, Decreasing, or Stable
Displays slope (rate of change per day)
Uses linear regression for accurate trend detection
Variability (Blue card)

Temperature Standard Deviation: How much temps vary
Humidity Standard Deviation: Humidity variation
Lower values = more stable weather
Data Summary
Text Summary Section

Quick overview of forecast period
Temperature range
Average values
Trend description
Exporting Data
CSV Export Feature

Click "📥 Export to CSV" button
File saves to data/ directory
Filename includes city name and date
Open in Excel or any spreadsheet application
Use Cases for Exported Data:

Long-term weather tracking
Academic research
Personal weather journals
Further analysis in Excel/Python
6. Working with Charts
Chart Type Selection
Use the dropdown menu to select from 5 chart types:

1. Interactive Temperature Chart
Features:

Hover to see exact values
Three lines: Max, Avg, Min temperatures
Shaded area between max and min
Zoom and pan capabilities
Click legend items to show/hide
How to Use:

Move mouse over chart to see details
Double-click to reset zoom
Drag to pan across dates
Click legend to toggle lines
2. Static Temperature Line Chart
Features:

Professional publication-quality
Grid lines for easy reading
Value labels on points
Temperature range visualization
Best For:

Screenshots and reports
Printing
Academic presentations
3. Humidity Bar Chart
Features:

Gradient colored bars
Value labels on each bar
Reference lines at 30%, 50%, 70%
Comfort zone indicators
Interpretation:

Red dashed line: optimal humidity (50%)
Orange lines: comfortable range boundaries
Below 30%: too dry
Above 70%: too humid
4. Temperature vs Humidity Comparison
Features:

Dual Y-axes (temperature and humidity)
Interactive hover
Shows correlation between metrics
Different line styles for distinction
Use Cases:

Understanding weather comfort
Analyzing weather patterns
Predicting weather changes
5. Temperature Heatmap
Features:

Color-coded temperature visualization
Shows min, avg, max by day
Easy pattern recognition
Hover for exact values
Interpretation:

Dark red: high temperatures
Blue: low temperatures
Quick visual comparison across days
Chart Interaction Tips
For Interactive Charts (Plotly):

🖱️ Hover: See detailed information
🔍 Zoom: Use mouse wheel or zoom buttons
↔️ Pan: Click and drag to move
📸 Save: Use camera icon to download image
🏠 Reset: Double-click to reset view
For Static Charts (Matplotlib):

💾 Right-click to save image
🖨️ Print-friendly quality
📄 Copy to clipboard (browser dependent)
7. Managing Search History
Viewing History
Access:

Navigate to the "🕐 History" tab
See all past searches in chronological order
Most recent searches appear first
Information Displayed:

City name
Temperature at time of search
Weather condition
Date and time of search
Using History
Expandable Cards:

Click on any history entry to expand
View detailed information
Click "🔍 Search Again" to reload that city's weather
Quick Access:

Recent searches also appear in sidebar
Shows last 5 searches only
One-click to reload
Clearing History
Methods:

From History Tab:
Scroll to bottom
Click "🗑️ Clear All History" button
Confirm action
From Sidebar:
Find "Settings" section
Click "🗑️ Clear History" button
Note: This action cannot be undone. All search history will be permanently deleted.

8. Settings and Configuration
Temperature Units
Available Options:

Celsius (°C)
Metric system
Default setting
Used internationally
Fahrenheit (°F)
Imperial system
Common in USA
Converts automatically
How to Change:

Locate "Settings" in sidebar
Click dropdown under "Temperature Unit"
Select preferred unit
All temperatures update automatically
API Key Management
Entering API Key:

If not configured, prompt appears on startup
Enter key in password field
Click "Save API Key"
Application reloads automatically
Updating API Key:

Create new .env file
Replace old key with new one
Restart application
9. Troubleshooting
Common Issues and Solutions
Issue: "City Not Found"
Solutions:

✅ Check spelling of city name
✅ Try adding country code: "Springfield,US"
✅ Use major city names
✅ Avoid abbreviations
Issue: "Invalid API Key"
Solutions:

✅ Verify key is correct (no extra spaces)
✅ Check if key is activated (can take few minutes)
✅ Ensure key hasn't expired
✅ Generate new key if necessary
Issue: "Connection Error"
Solutions:

✅ Check internet connection
✅ Verify firewall isn't blocking
✅ Try different network
✅ Check OpenWeatherMap service status
Issue: Charts Not Displaying
Solutions:

✅ Refresh browser page
✅ Clear browser cache
✅ Try different browser
✅ Check if JavaScript is enabled
✅ Verify all dependencies installed
Issue: Application Won't Start
Solutions:

✅ Check Python version (3.8+ required)
✅ Install all requirements: pip install -r requirements.txt
✅ Verify no port conflicts (default: 8501)
✅ Check for error messages in terminal
10. FAQ
General Questions
Q: Is the Weather Dashboard free to use? A: Yes! The application is free. You only need a free OpenWeatherMap API key.

Q: How accurate is the weather data? A: Data comes directly from OpenWeatherMap, which aggregates from multiple meteorological sources. Accuracy is generally high for major cities.

Q: How often is weather data updated? A: Each search fetches real-time data. The API updates every 10-15 minutes.

Q: Can I use this offline? A: No, an internet connection is required to fetch weather data from the API.

Data Questions
Q: How far ahead is the forecast? A: The free tier provides up to 5 days of forecast data (displayed as 7-day based on 3-hour intervals).

Q: Where is my search history stored? A: Locally in data/search_history.json. Your data never leaves your computer.

Q: What's the maximum number of searches saved? A: The application keeps your last 10 searches automatically.

Q: Can I export weather data? A: Yes! Use the "Export to CSV" button in the Analytics tab.

Technical Questions
Q: What Python version do I need? A: Python 3.8 or higher is required.

Q: Can I run this on a server? A: Yes, Streamlit can be deployed to cloud services like Streamlit Cloud, Heroku, or AWS.

Q: Is my API key secure? A: Yes, when stored in .env file. Never share your .env file or commit it to version control.

Q: Can I customize the interface colors? A: Yes, but requires modifying the CSS in main.py or ui.py.

Feature Questions
Q: Can I compare multiple cities? A: Currently one city at a time. Multi-city comparison is a planned feature.

Q: Are weather alerts available? A: Not in current version. Consider this a feature request!

Q: Can I see historical weather data? A: The free API tier doesn't include historical data. Consider upgrading API plan.

Q: Is there a mobile app? A: No native app, but the web interface works on mobile browsers.

Support and Contact
Getting Help
Check Documentation
Read this manual thoroughly
Review README.md
Check troubleshooting section
Search Issues
Look for similar issues on GitHub
Check closed issues for solutions
Ask for Help
Open a new GitHub issue
Provide detailed description
Include error messages
Mention your OS and Python version
Reporting Bugs
When reporting bugs, include:

Steps to reproduce
Expected behavior
Actual behavior
Screenshots (if applicable)
Error messages
System information
Feature Requests
Have an idea? We'd love to hear it!

Open a GitHub issue with "Feature Request" label
Describe the feature in detail
Explain the use case
Include mockups if possible
Appendix
Keyboard Shortcuts
Shortcut	Action
Ctrl + R	Refresh page
Ctrl + L	Focus on search box
Esc	Close expanded elements
Weather Condition Codes
Common weather descriptions:

Clear Sky: No clouds, excellent visibility
Few Clouds: 11-25% cloud coverage
Scattered Clouds: 25-50% cloud coverage
Broken Clouds: 51-84% cloud coverage
Overcast: 85-100% cloud coverage
Light Rain: < 2.5mm/hour
Moderate Rain: 2.5-10mm/hour
Heavy Rain: > 10mm/hour
Understanding Metrics
Temperature:

Celsius: Water freezes at 0°C, boils at 100°C
Fahrenheit: Water freezes at 32°F, boils at 212°F
Humidity:

0-30%: Very dry
30-50%: Comfortable
50-70%: Slightly humid
70-100%: Very humid
Wind Speed:

< 5 m/s: Light breeze
5-10 m/s: Moderate wind
10-20 m/s: Strong wind
20 m/s: Gale force

Pressure:

< 1000 hPa: Low pressure (storm)
1000-1020 hPa: Normal
1020 hPa: High pressure (clear)

Last Updated: November 28, 2025 Version: 1.0.0 For Questions: Contact via GitHub Issues

