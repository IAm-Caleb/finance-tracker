# import streamlit as st
# import pandas as pd
# from datetime import datetime, timedelta
# import plotly.graph_objects as go
# import plotly.express as px
# from utils.data_handler import DataHandler
# from utils.calculations import FinancialCalculator
# from components.dashboard import render_dashboard
# from components.transactions import render_transactions
# from components.budgets import render_budgets
# from components.reports import render_reports
# from components.settings import render_settings

# st.set_page_config(
#     page_title="Finance Pro",
#     page_icon="💰",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# def load_custom_css():
#     st.markdown("""
#         <style>
#         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
        
#         * {
#             font-family: 'Poppins', sans-serif;
#         }
        
#         .stApp {
#             background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         }
        
#         [data-testid="stHeader"] {
#             background: transparent;
#         }
        
#         .main-navbar {
#             background: linear-gradient(135deg, #069494 0%, #04716e 100%);
#             padding: 1rem 2rem;
#             margin: -6rem -4rem 2rem -4rem;
#             box-shadow: 0 4px 20px rgba(6, 148, 148, 0.2);
#             position: relative;
#         }
        
#         .navbar-content {
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#             max-width: 1400px;
#             margin: 0 auto;
#         }
        
#         .navbar-brand {
#             display: flex;
#             align-items: center;
#             gap: 1rem;
#         }
        
#         .navbar-title {
#             color: #2c3e50 !important;
#             font-size: 1.8rem;
#             font-weight: 800;
#             margin: 0;
#         }
        
#         .navbar-logo {
#             font-size: 2rem;
#         }
        
#         .nav-tabs-container {
#             display: flex;
#             gap: 0.8rem;
#             align-items: center;
#         }
        
#         div[data-testid="column"] button {
#             background: transparent !important;
#             color: white !important;
#             border: 2px solid transparent !important;
#             padding: 0.7rem 1.5rem !important;
#             border-radius: 10px !important;
#             font-weight: 600 !important;
#             font-size: 0.95rem !important;
#             transition: all 0.3s ease !important;
#             box-shadow: none !important;
#         }
        
#         div[data-testid="column"] button:hover {
#             background: rgba(255, 255, 255, 0.15) !important;
#             border-color: rgba(255, 255, 255, 0.3) !important;
#             transform: translateY(-2px);
#         }
        
#         .metric-card {
#             background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
#             padding: 2rem;
#             border-radius: 20px;
#             box-shadow: 0 10px 40px rgba(0,0,0,0.08);
#             border: 1px solid rgba(255,255,255,0.8);
#             transition: all 0.3s ease;
#             position: relative;
#             overflow: hidden;
#         }
        
#         .metric-card::before {
#             content: '';
#             position: absolute;
#             top: 0;
#             left: 0;
#             width: 5px;
#             height: 100%;
#             background: #FF8243;
#         }
        
#         .metric-card.income::before {
#             background: #069494;
#         }
        
#         .metric-card.expense::before {
#             background: #FF8243;
#         }
        
#         .metric-card.balance::before {
#             background: #FCE883;
#         }
        
#         .metric-card.savings::before {
#             background: #FFC0CB;
#         }
        
#         .metric-card:hover {
#             transform: translateY(-5px);
#             box-shadow: 0 15px 50px rgba(0,0,0,0.12);
#         }
        
#         .metric-icon {
#             font-size: 3rem;
#             opacity: 0.1;
#             position: absolute;
#             right: 1rem;
#             top: 50%;
#             transform: translateY(-50%);
#         }
        
#         .metric-value {
#             font-size: 2.5rem;
#             font-weight: 800;
#             color: #2c3e50;
#             margin: 0.5rem 0;
#             position: relative;
#             z-index: 1;
#         }
        
#         .metric-label {
#             font-size: 0.85rem;
#             color: #7f8c8d;
#             font-weight: 600;
#             text-transform: uppercase;
#             letter-spacing: 1px;
#             position: relative;
#             z-index: 1;
#         }
        
#         .metric-change {
#             font-size: 0.9rem;
#             font-weight: 600;
#             margin-top: 0.5rem;
#             position: relative;
#             z-index: 1;
#         }
        
#         .metric-change.positive {
#             color: #069494;
#         }
        
#         .metric-change.negative {
#             color: #FF8243;
#         }
        
#         .content-card {
#             background: white;
#             padding: 2.5rem;
#             border-radius: 20px;
#             box-shadow: 0 10px 40px rgba(0,0,0,0.08);
#             margin-bottom: 2rem;
#             border: 1px solid rgba(0,0,0,0.05);
#             transition: all 0.3s ease;
#         }
        
#         .content-card:hover {
#             box-shadow: 0 15px 50px rgba(0,0,0,0.12);
#         }
        
#         .section-title {
#             color: #2c3e50;
#             font-size: 1.8rem;
#             font-weight: 700;
#             margin-bottom: 1.5rem;
#         }
        
#         div[data-testid="stButton"] button {
#             background: linear-gradient(135deg, #FF8243 0%, #ff6b2e 100%) !important;
#             color: white !important;
#             border: none !important;
#             border-radius: 12px !important;
#             padding: 0.8rem 2.5rem !important;
#             font-weight: 600 !important;
#             font-size: 1rem !important;
#             transition: all 0.3s ease !important;
#             box-shadow: 0 5px 20px rgba(255, 130, 67, 0.3) !important;
#             cursor: pointer !important;
#             position: relative !important;
#             overflow: hidden !important;
#         }

#         div[data-testid="stButton"] button::before {
#             content: '';
#             position: absolute;
#             top: 0;
#             left: -100%;
#             width: 100%;
#             height: 100%;
#             background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
#             transition: left 0.5s ease;
#         }

#         div[data-testid="stButton"] button:hover::before {
#             left: 100%;
#         }

#         div[data-testid="stButton"] button:hover {
#             transform: translateY(-2px) !important;
#             box-shadow: 0 8px 30px rgba(255, 130, 67, 0.4) !important;
#         }

#         div[data-testid="stButton"] button:active {
#             transform: translateY(0px) !important;
#             box-shadow: 0 2px 10px rgba(255, 130, 67, 0.3) !important;
#             transition: all 0.1s ease !important;
#         }
        
#         .stTabs [data-baseweb="tab-list"] {
#             gap: 0.5rem;
#             background: transparent;
#         }
        
#         .stTabs [data-baseweb="tab"] {
#             background: white;
#             border-radius: 12px;
#             padding: 0.8rem 2rem;
#             font-weight: 600;
#             border: 2px solid transparent;
#             transition: all 0.3s ease;
#         }
        
#         .stTabs [data-baseweb="tab"]:hover {
#             border-color: #FF8243;
#         }
        
#         .stTabs [aria-selected="true"] {
#             background: linear-gradient(135deg, #FF8243 0%, #ff6b2e 100%);
#             color: white;
#             box-shadow: 0 5px 20px rgba(255, 130, 67, 0.3);
#         }
        
#         .stDataFrame {
#             border-radius: 12px;
#             overflow: hidden;
#             box-shadow: 0 5px 20px rgba(0,0,0,0.05);
#         }
        
#         div[data-testid="stExpander"] {
#             background: white;
#             border-radius: 12px;
#             border: 1px solid #e0e0e0;
#             margin-bottom: 1rem;
#             transition: all 0.3s ease;
#         }
        
#         div[data-testid="stExpander"]:hover {
#             box-shadow: 0 5px 20px rgba(0,0,0,0.08);
#             border-color: #FF8243;
#         }
        
#         .stProgress > div > div {
#             background: linear-gradient(90deg, #069494 0%, #FF8243 100%);
#             border-radius: 10px;
#         }
        
#         input, select, textarea {
#             border-radius: 10px !important;
#             border: 2px solid #e0e0e0 !important;
#             transition: all 0.3s ease !important;
#         }
        
#         input:focus, select:focus, textarea:focus {
#             border-color: #FF8243 !important;
#             box-shadow: 0 0 0 3px rgba(255, 130, 67, 0.1) !important;
#         }
        
#         .transaction-item {
#             background: white;
#             padding: 1.5rem;
#             border-radius: 12px;
#             border-left: 4px solid #FF8243;
#             margin-bottom: 1rem;
#             box-shadow: 0 3px 15px rgba(0,0,0,0.05);
#             transition: all 0.3s ease;
#         }
        
#         .transaction-item:hover {
#             transform: translateX(5px);
#             box-shadow: 0 5px 25px rgba(0,0,0,0.1);
#         }
        
#         .transaction-item.income {
#             border-left-color: #069494;
#         }
        
#         .alert-success {
#             background: linear-gradient(135deg, #069494 0%, #04716e 100%);
#             color: white;
#             padding: 1rem 1.5rem;
#             border-radius: 12px;
#             font-weight: 600;
#         }
        
#         .alert-warning {
#             background: linear-gradient(135deg, #FCE883 0%, #f4d842 100%);
#             color: #5a4a00;
#             padding: 1rem 1.5rem;
#             border-radius: 12px;
#             font-weight: 600;
#         }
        
#         .alert-danger {
#             background: linear-gradient(135deg, #FF8243 0%, #ff6b2e 100%);
#             color: white;
#             padding: 1rem 1.5rem;
#             border-radius: 12px;
#             font-weight: 600;
#         }
        
#         .stMetric {
#             background: white;
#             padding: 1.5rem;
#             border-radius: 12px;
#             box-shadow: 0 3px 15px rgba(0,0,0,0.05);
#         }

#         .stMetric label {
#             color: #7f8c8d !important;
#         }

#         .stMetric .stMetricValue {
#             color: #2c3e50 !important;
#         }
        
#         .chart-container {
#             background: white;
#             padding: 1.5rem;
#             border-radius: 12px;
#             box-shadow: 0 5px 20px rgba(0,0,0,0.05);
#         }
        
#         </style>
#     """, unsafe_allow_html=True)

# def render_navbar():
#     st.markdown('<div class="main-navbar">', unsafe_allow_html=True)
#     st.markdown('<div class="navbar-content">', unsafe_allow_html=True)
    
#     cols = st.columns([2, 1, 1, 1, 1, 1, 2])
    
#     with cols[0]:
#         st.markdown('<div class="navbar-brand"><div class="navbar-logo">💰</div><h1 class="navbar-title">Finance Pro</h1></div>', unsafe_allow_html=True)
    
#     tabs = ["Dashboard", "Transactions", "Budgets", "Reports", "Settings"]
    
#     for i, (col, tab) in enumerate(zip(cols[1:6], tabs)):
#         with col:
#             if st.button(tab, key=f"nav_{tab}", use_container_width=True):
#                 st.session_state.current_page = tab
    
#     st.markdown('</div></div>', unsafe_allow_html=True)

# def initialize_session_state():
#     if 'current_page' not in st.session_state:
#         st.session_state.current_page = "Dashboard"
    
#     if 'data_handler' not in st.session_state:
#         st.session_state.data_handler = DataHandler()
    
#     if 'currency' not in st.session_state:
#         st.session_state.currency = "$"
    
#     if 'monthly_income_target' not in st.session_state:
#         st.session_state.monthly_income_target = 5000

# def main():
#     load_custom_css()
#     initialize_session_state()
#     render_navbar()
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     page = st.session_state.current_page
    
#     if page == "Dashboard":
#         render_dashboard()
#     elif page == "Transactions":
#         render_transactions()
#     elif page == "Budgets":
#         render_budgets()
#     elif page == "Reports":
#         render_reports()
#     elif page == "Settings":
#         render_settings()

# if __name__ == "__main__":
#     main()


import streamlit as st
from utils.data_handler import DataHandler
from components.dashboard import render_dashboard
from components.transactions import render_transactions
from components.budgets import render_budgets
from components.reports import render_reports
from components.settings import render_settings

st.set_page_config(
    page_title="Finance Pro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }

    body {
        color: #1f2937;
    }

    .stApp {
        background: #f1f5f9;
    }

    /* ===== NAVBAR ===== */
    .main-navbar {
        background: #0f766e;
        padding: 1rem 2rem;
        margin: -4rem -4rem 2rem -4rem;
        box-shadow: 0 10px 30px rgba(0,0,0,.15);
    }

    .navbar-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
    }

    .navbar-brand {
        display: flex;
        align-items: center;
        gap: .75rem;
        color: white;
        font-size: 1.6rem;
        font-weight: 800;
    }

    .nav-buttons {
        display: flex;
        gap: .5rem;
        flex-wrap: wrap;
    }

    .nav-buttons button {
        background: rgba(255,255,255,.15) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: .5rem 1.2rem !important;
        border: none !important;
        font-weight: 600 !important;
    }

    .nav-buttons button:hover {
        background: rgba(255,255,255,.3) !important;
    }

    /* ===== CARDS ===== */
    .card {
        background: white;
        border-radius: 18px;
        padding: 1.8rem;
        box-shadow: 0 10px 25px rgba(0,0,0,.08);
        margin-bottom: 1.5rem;
    }

    .metric-card {
        position: relative;
        border-left: 6px solid;
    }

    .income { border-color: #0f766e; }
    .expense { border-color: #ea580c; }
    .balance { border-color: #2563eb; }
    .savings { border-color: #16a34a; }

    .metric-label {
        font-size: .75rem;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: #6b7280;
        font-weight: 700;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin: .4rem 0;
        color: #111827;
    }

    .metric-sub {
        font-size: .9rem;
        font-weight: 600;
        color: #374151;
    }

    /* ===== SECTION TITLES ===== */
    .section-title {
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #111827;
    }

    /* ===== TRANSACTIONS ===== */
    .transaction {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border-radius: 12px;
        background: #f9fafb;
        margin-bottom: .75rem;
    }

    .transaction-left {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .transaction-amount {
        font-weight: 800;
        font-size: 1.1rem;
    }
    /* ===== FORCE TEXT VISIBILITY ===== */
    * {
        color: #111827 !important;
    }

    /* Override for navbar brand */
    .navbar-brand {
        color: #ffffff !important;
    }

    /* Override for buttons */
    button {
        color: white !important;
    }

    /* Override for specific elements that should be white */
    .alert-success,
    .alert-danger,
    .stTabs [aria-selected="true"] {
        color: white !important;
    }

    /* Override for warning alerts */
    .alert-warning {
        color: #5a4a00 !important;
    }

    /* Override for navbar buttons */
    .nav-buttons button {
        color: white !important;
    }

    /* Override for selected tabs */
    .stTabs [aria-selected="true"] {
        color: white !important;
    }

    /* ===== SELECT DROPDOWN STYLING ===== */
    div[data-testid="stSelectbox"] {
        background-color: #f9fafb !important;
        border-radius: 10px !important;
        border: 1px solid #d1d5db !important;
    }

    div[data-testid="stSelectbox"] select {
        color: #111827 !important;
        background-color: #f9fafb !important;
        border: none !important;
        border-radius: 10px !important;
    }

    div[data-testid="stSelectbox"] select option {
        color: #111827 !important;
        background-color: #f9fafb !important;
    }

    div[data-testid="stSelectbox"] select:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
        outline: none !important;
    }


    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .metric-value {
            font-size: 1.8rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def render_navbar():
    st.markdown('<div class="main-navbar"><div class="navbar-content">', unsafe_allow_html=True)

    st.markdown('<div class="navbar-brand">💰 Finance Pro</div>', unsafe_allow_html=True)

    tabs = ["Dashboard", "Transactions", "Budgets", "Reports", "Settings"]
    cols = st.columns(len(tabs))

    for col, tab in zip(cols, tabs):
        with col:
            if st.button(tab, use_container_width=True):
                st.session_state.current_page = tab

    st.markdown('</div></div>', unsafe_allow_html=True)

def init_state():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if "data_handler" not in st.session_state:
        st.session_state.data_handler = DataHandler()
    if "currency" not in st.session_state:
        st.session_state.currency = "$"

def main():
    load_custom_css()
    init_state()
    render_navbar()

    page = st.session_state.current_page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Transactions":
        render_transactions()
    elif page == "Budgets":
        render_budgets()
    elif page == "Reports":
        render_reports()
    elif page == "Settings":
        render_settings()

if __name__ == "__main__":
    main()
