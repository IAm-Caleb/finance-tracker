# src/charts.py
"""
Charts and Visualization Module
================================
Provides functions to create both static and interactive charts for
weather data visualization using Matplotlib and Plotly.

Features:
- Static charts (Matplotlib): Temperature trends, humidity bars
- Interactive charts (Plotly): Hoverable forecasts, comparisons
- Customizable styling and color schemes

Dependencies:
    - matplotlib: Static chart generation
    - plotly: Interactive chart generation
    - numpy: Data manipulation for charts
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from typing import List, Dict
import numpy as np

# Color schemes
PRIMARY_COLOR = '#667eea'
SECONDARY_COLOR = '#764ba2'
ACCENT_COLOR = '#f6ad55'
TEMP_COLOR = '#fc8181'
HUMIDITY_COLOR = '#4299e1'

def create_temperature_line_chart(forecast_data: List[Dict]) -> plt.Figure:
    """
    Create a static line chart showing 7-day temperature trends using Matplotlib.
    
    Args:
        forecast_data (List[Dict]): List of forecast entries containing dates
                                    and temperature data
                                    
    Returns:
        plt.Figure: Matplotlib figure object containing the chart
        
    Example:
        >>> forecast = [{'date': '2025-11-23', 'temp_avg': 20}, ...]
        >>> fig = create_temperature_line_chart(forecast)
        >>> plt.savefig('temp_chart.png')
    """
    try:
        # Extract data
        dates = [datetime.strptime(item['date'], '%Y-%m-%d') for item in forecast_data]
        temp_max = [item['temp_max'] for item in forecast_data]
        temp_min = [item['temp_min'] for item in forecast_data]
        temp_avg = [item['temp_avg'] for item in forecast_data]
        
        # Create figure with custom size and DPI
        fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
        
        # Plot lines with custom styling
        ax.plot(dates, temp_max, 
                marker='o', 
                linewidth=2.5, 
                color=TEMP_COLOR, 
                label='Max Temperature',
                markersize=8)
        ax.plot(dates, temp_avg, 
                marker='s', 
                linewidth=2.5, 
                color=PRIMARY_COLOR, 
                label='Avg Temperature',
                markersize=8)
        ax.plot(dates, temp_min, 
                marker='^', 
                linewidth=2.5, 
                color=HUMIDITY_COLOR, 
                label='Min Temperature',
                markersize=8)
        
        # Fill area between max and min
        ax.fill_between(dates, temp_min, temp_max, alpha=0.2, color=PRIMARY_COLOR)
        
        # Customize axes
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Temperature (°C)', fontsize=12, fontweight='bold')
        ax.set_title('7-Day Temperature Trend', 
                     fontsize=16, 
                     fontweight='bold', 
                     pad=20)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        plt.xticks(rotation=45, ha='right')
        
        # Add grid for better readability
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # Add legend
        ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
        
        # Add value labels on points
        for i, (date, temp) in enumerate(zip(dates, temp_avg)):
            if i % 2 == 0:  # Label every other point to avoid crowding
                ax.annotate(f'{temp}°C', 
                           xy=(date, temp), 
                           xytext=(0, 10),
                           textcoords='offset points',
                           ha='center',
                           fontsize=9,
                           bbox=dict(boxstyle='round,pad=0.3', 
                                   facecolor='white', 
                                   edgecolor=PRIMARY_COLOR,
                                   alpha=0.8))
        
        # Tight layout to prevent label cutoff
        plt.tight_layout()
        
        return fig
        
    except Exception as e:
        print(f"Error creating temperature line chart: {str(e)}")
        # Return empty figure on error
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, f'Error creating chart: {str(e)}', 
                ha='center', va='center', fontsize=12)
        return fig

def create_humidity_bar_chart(forecast_data: List[Dict]) -> plt.Figure:
    """
    Create a static bar chart showing humidity levels across forecast days.
    
    Args:
        forecast_data (List[Dict]): List of forecast entries with humidity data
        
    Returns:
        plt.Figure: Matplotlib figure object containing the chart
    """
    try:
        # Extract data
        dates = [datetime.strptime(item['date'], '%Y-%m-%d').strftime('%b %d') 
                for item in forecast_data]
        humidity = [item['humidity_avg'] for item in forecast_data]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
        
        # Create gradient colors for bars
        colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(humidity)))
        
        # Create bars
        bars = ax.bar(dates, humidity, color=colors, edgecolor='navy', linewidth=1.5)
        
        # Customize each bar
        for bar, hum in zip(bars, humidity):
            height = bar.get_height()
            # Add value label on top of each bar
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{hum}%',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # Add gradient effect (top part lighter)
            bar.set_alpha(0.8)
        
        # Customize axes
        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Humidity (%)', fontsize=12, fontweight='bold')
        ax.set_title('7-Day Humidity Forecast', 
                     fontsize=16, 
                     fontweight='bold', 
                     pad=20)
        
        # Set y-axis limits
        ax.set_ylim(0, 100)
        
        # Add horizontal line at 50% (comfortable humidity)
        ax.axhline(y=50, color='red', linestyle='--', linewidth=1, 
                  alpha=0.5, label='Comfortable Range')
        ax.axhline(y=30, color='orange', linestyle='--', linewidth=1, alpha=0.3)
        ax.axhline(y=70, color='orange', linestyle='--', linewidth=1, alpha=0.3)
        
        # Add grid
        ax.grid(True, axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        
        # Add legend
        ax.legend(loc='upper right', fontsize=10)
        
        plt.tight_layout()
        
        return fig
        
    except Exception as e:
        print(f"Error creating humidity bar chart: {str(e)}")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.text(0.5, 0.5, f'Error creating chart: {str(e)}', 
                ha='center', va='center', fontsize=12)
        return fig

def create_interactive_temperature_chart(forecast_data: List[Dict]) -> go.Figure:
    """
    Create an interactive temperature chart using Plotly with hover effects.
    
    Args:
        forecast_data (List[Dict]): List of forecast entries
        
    Returns:
        go.Figure: Plotly figure object with interactive features
    """
    try:
        # Extract data
        dates = [item['date'] for item in forecast_data]
        temp_max = [item['temp_max'] for item in forecast_data]
        temp_min = [item['temp_min'] for item in forecast_data]
        temp_avg = [item['temp_avg'] for item in forecast_data]
        descriptions = [item['description'] for item in forecast_data]
        
        # Create figure
        fig = go.Figure()
        
        # Add max temperature trace
        fig.add_trace(go.Scatter(
            x=dates,
            y=temp_max,
            mode='lines+markers',
            name='Max Temperature',
            line=dict(color=TEMP_COLOR, width=3),
            marker=dict(size=10, symbol='circle'),
            hovertemplate='<b>Max Temp</b><br>' +
                         'Date: %{x}<br>' +
                         'Temperature: %{y}°C<br>' +
                         '<extra></extra>'
        ))
        
        # Add average temperature trace
        fig.add_trace(go.Scatter(
            x=dates,
            y=temp_avg,
            mode='lines+markers',
            name='Avg Temperature',
            line=dict(color=PRIMARY_COLOR, width=3),
            marker=dict(size=10, symbol='square'),
            hovertemplate='<b>Avg Temp</b><br>' +
                         'Date: %{x}<br>' +
                         'Temperature: %{y}°C<br>' +
                         '<extra></extra>'
        ))
        
        # Add min temperature trace
        fig.add_trace(go.Scatter(
            x=dates,
            y=temp_min,
            mode='lines+markers',
            name='Min Temperature',
            line=dict(color=HUMIDITY_COLOR, width=3),
            marker=dict(size=10, symbol='triangle-up'),
            hovertemplate='<b>Min Temp</b><br>' +
                         'Date: %{x}<br>' +
                         'Temperature: %{y}°C<br>' +
                         '<extra></extra>'
        ))
        
        # Add filled area between max and min
        fig.add_trace(go.Scatter(
            x=dates + dates[::-1],
            y=temp_max + temp_min[::-1],
            fill='toself',
            fillcolor=f'rgba(102, 126, 234, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text='Interactive 7-Day Temperature Forecast',
                font=dict(size=20, color='#333', family='Arial Black'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title='Date',
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)',
                showline=True,
                linecolor='rgba(0,0,0,0.3)'
            ),
            yaxis=dict(
                title='Temperature (°C)',
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)',
                showline=True,
                linecolor='rgba(0,0,0,0.3)'
            ),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial', size=12),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            height=500
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating interactive temperature chart: {str(e)}")
        # Return empty figure with error message
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error creating chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig

def create_forecast_comparison_chart(forecast_data: List[Dict]) -> go.Figure:
    """
    Create an interactive chart comparing multiple weather metrics.
    
    Args:
        forecast_data (List[Dict]): List of forecast entries
        
    Returns:
        go.Figure: Plotly figure with multi-metric comparison
    """
    try:
        dates = [item['date'] for item in forecast_data]
        temp_avg = [item['temp_avg'] for item in forecast_data]
        humidity = [item['humidity_avg'] for item in forecast_data]
        
        # Create subplot with secondary y-axis
        fig = go.Figure()
        
        # Temperature trace
        fig.add_trace(go.Scatter(
            x=dates,
            y=temp_avg,
            name='Temperature',
            mode='lines+markers',
            line=dict(color=TEMP_COLOR, width=3),
            marker=dict(size=10),
            yaxis='y',
            hovertemplate='<b>Temperature</b><br>%{y}°C<extra></extra>'
        ))
        
        # Humidity trace (on secondary axis)
        fig.add_trace(go.Scatter(
            x=dates,
            y=humidity,
            name='Humidity',
            mode='lines+markers',
            line=dict(color=HUMIDITY_COLOR, width=3, dash='dash'),
            marker=dict(size=10, symbol='diamond'),
            yaxis='y2',
            hovertemplate='<b>Humidity</b><br>%{y}%<extra></extra>'
        ))
        
        # Update layout with dual axes
        fig.update_layout(
            title=dict(
                text='Temperature vs Humidity Comparison',
                font=dict(size=20, color='#333'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(title='Date', showgrid=True),
            yaxis=dict(
                title='Temperature (°C)',
                titlefont=dict(color=TEMP_COLOR),
                tickfont=dict(color=TEMP_COLOR)
            ),
            yaxis2=dict(
                title='Humidity (%)',
                titlefont=dict(color=HUMIDITY_COLOR),
                tickfont=dict(color=HUMIDITY_COLOR),
                anchor='x',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            legend=dict(x=0.01, y=0.99),
            height=500
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating comparison chart: {str(e)}")
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig

def create_temperature_heatmap(forecast_data: List[Dict]) -> go.Figure:
    """
    Create a heatmap showing temperature variations throughout the forecast period.
    
    Args:
        forecast_data (List[Dict]): List of forecast entries
        
    Returns:
        go.Figure: Plotly heatmap figure
    """
    try:
        dates = [item['date'] for item in forecast_data]
        metrics = ['Min Temp', 'Avg Temp', 'Max Temp']
        
        # Create data matrix
        data_matrix = [
            [item['temp_min'] for item in forecast_data],
            [item['temp_avg'] for item in forecast_data],
            [item['temp_max'] for item in forecast_data]
        ]
        
        fig = go.Figure(data=go.Heatmap(
            z=data_matrix,
            x=dates,
            y=metrics,
            colorscale='RdYlBu_r',
            text=data_matrix,
            texttemplate='%{text}°C',
            textfont={"size": 12},
            colorbar=dict(title='Temperature (°C)')
        ))
        
        fig.update_layout(
            title='Temperature Heatmap',
            xaxis_title='Date',
            height=400,
            plot_bgcolor='white'
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating heatmap: {str(e)}")
        fig = go.Figure()
        return fig