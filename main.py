# main.py
"""
Weather Dashboard Application - Main Entry Point
================================================
A production-ready weather dashboard application with GUI, API integration,
data analysis, and visualization capabilities.

Author: Weather Dashboard Team
Date: November 2025
Version: 1.0.0
"""

import streamlit as st
from src.ui import WeatherUI
from src.utils import initialize_data_directory

def main():
    """
    Main entry point for the Weather Dashboard Application.
    
    This function initializes the application by:
    1. Setting up the data directory structure
    2. Configuring Streamlit page settings
    3. Launching the Weather UI
    
    Returns:
        None
    """
    # Initialize data directory and required files
    initialize_data_directory()
    
    # Configure Streamlit page settings
    st.set_page_config(
        page_title="Weather Dashboard",
        page_icon="🌤️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for modern styling
    st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .weather-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            margin: 10px 0;
        }
        h1 {
            color: #667eea;
        }
        .stButton>button {
            background-color: #667eea;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            border: none;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Mobile Responsive Styles */
        @media (max-width: 768px) {
            .main {
                padding: 0rem 0.5rem;
            }
            .weather-card {
                padding: 15px;
            }
            h1 {
                font-size: 1.8rem;
            }
            h2 {
                font-size: 1.4rem;
            }
            h3 {
                font-size: 1.2rem;
            }
            .stButton>button {
                padding: 0.4rem 1rem;
                font-size: 0.9rem;
            }
        }
        
        /* Better spacing for mobile */
        @media (max-width: 480px) {
            .main {
                padding: 0rem 0.25rem;
            }
            h1 {
                font-size: 1.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize and run the Weather UI
    weather_ui = WeatherUI()
    weather_ui.render()

if __name__ == "__main__":
    main()