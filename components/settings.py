import streamlit as st

def render_settings():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Application Settings</h2>', unsafe_allow_html=True)
    
    data_handler = st.session_state.data_handler
    
    st.subheader("General Settings")
    
    currencies = {
        "US Dollar": "$",
        "Euro": "€",
        "British Pound": "£",
        "Japanese Yen": "¥",
        "Indian Rupee": "₹",
        "Nigerian Naira": "₦",
        "Canadian Dollar": "C$",
        "Australian Dollar": "A$"
    }
    
    current_currency_name = [name for name, symbol in currencies.items() if symbol == st.session_state.currency][0] if st.session_state.currency in currencies.values() else "US Dollar"
    
    selected_currency = st.selectbox(
        "Currency",
        options=list(currencies.keys()),
        index=list(currencies.keys()).index(current_currency_name)
    )
    
    st.session_state.currency = currencies[selected_currency]
    
    st.markdown("---")
    
    st.subheader("Financial Goals")
    
    monthly_target = st.number_input(
        f"Monthly Income Target ({st.session_state.currency})",
        min_value=0.0,
        value=float(st.session_state.monthly_income_target),
        step=100.0,
        format="%.2f"
    )
    
    st.session_state.monthly_income_target = monthly_target
    
    if st.button("Save Settings", type="primary"):
        settings = {
            'currency': st.session_state.currency,
            'monthly_income_target': st.session_state.monthly_income_target
        }
        data_handler.save_settings(settings)
        st.success("Settings saved successfully!")
    
    st.markdown("---")
    
    st.subheader("Data Management")
    
    st.warning("Warning: The following actions cannot be undone.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Export Data**")
        st.write("Download all your transaction data as a CSV file for backup purposes.")
        
        transactions_df = data_handler.load_transactions()
        
        if not transactions_df.empty:
            csv = transactions_df.to_csv(index=False)
            st.download_button(
                label="Export Transactions",
                data=csv,
                file_name="finance_tracker_backup.csv",
                mime="text/csv"
            )
        else:
            st.info("No data to export.")
    
    with col2:
        st.write("**Reset All Data**")
        st.write("Permanently delete all transactions and budgets. This action cannot be undone.")
        
        if st.button("Reset All Data", type="secondary"):
            st.session_state.show_reset_confirm = True
    
    if st.session_state.get('show_reset_confirm', False):
        st.error("Are you sure you want to delete all data? This action is irreversible!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Yes, Delete Everything", type="primary"):
                data_handler.reset_all_data()
                st.session_state.show_reset_confirm = False
                st.success("All data has been deleted successfully.")
                st.rerun()
        
        with col2:
            if st.button("Cancel"):
                st.session_state.show_reset_confirm = False
                st.rerun()
    
    st.markdown("---")
    
    st.subheader("About")
    
    st.write("""
    **Personal Finance Tracker & Budget Planner**
    
    Version: 1.0.0
    
    A comprehensive financial management application built with Python and Streamlit.
    Track your income, expenses, set budgets, and gain insights into your financial health.
    
    Features:
    - Transaction tracking and management
    - Budget planning and monitoring
    - Detailed financial reports
    - Category-based expense analysis
    - Data export capabilities
    
    Built with modern technologies for a seamless user experience.
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)