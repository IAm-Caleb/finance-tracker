import streamlit as st
from datetime import datetime
from utils.calculations import FinancialCalculator

def render_budgets():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Budget Planner</h2>', unsafe_allow_html=True)
    
    data_handler = st.session_state.data_handler
    categories = data_handler.load_categories()
    currency = st.session_state.currency
    
    tab1, tab2 = st.tabs(["🎯 Set Budget", "📊 Analysis"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div style="background: #f8f9fa; padding: 2rem; border-radius: 15px;">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                year = st.number_input("📅 Year", min_value=2020, max_value=2030, value=datetime.now().year)
            
            with col2:
                month = st.selectbox("📆 Month", range(1, 13), index=datetime.now().month - 1, format_func=lambda x: datetime(2000, x, 1).strftime('%B'))
            
            with col3:
                category = st.selectbox("📁 Category", categories['expense'])
            
            budget_amount = st.number_input(f"💰 Budget Amount ({currency})", min_value=0.01, step=50.0, format="%.2f", value=500.0)
            
            if st.button("💾 Set Budget", use_container_width=True):
                month_str = f"{year}-{month:02d}"
                data_handler.save_budget(category, budget_amount, month_str)
                st.markdown(f"""
                    <div class="alert-success">
                        ✅ Budget set for {category} in {datetime(year, month, 1).strftime('%B %Y')}
                    </div>
                """, unsafe_allow_html=True)
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Current Month Budgets")
        
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_month_str = f"{current_year}-{current_month:02d}"
        
        budgets_df = data_handler.load_budgets()
        current_budgets = budgets_df[budgets_df['month'] == current_month_str]
        
        if not current_budgets.empty:
            for _, budget in current_budgets.iterrows():
                st.markdown(f"""
                    <div style="padding: 1.5rem; background: white; border-radius: 12px; border-left: 4px solid #FF8243; margin-bottom: 1rem; box-shadow: 0 3px 15px rgba(0,0,0,0.05);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="font-weight: 700; font-size: 1.1rem; color: #2c3e50;">📁 {budget['category']}</div>
                            <div style="font-weight: 800; font-size: 1.3rem; color: #FF8243;">{currency}{budget['amount']:,.2f}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No budgets set for current month.")
    
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                analysis_year = st.number_input("Year", min_value=2020, max_value=2030, value=datetime.now().year, key="analysis_year")
            
            with col2:
                analysis_month = st.selectbox("Month", range(1, 13), index=datetime.now().month - 1, format_func=lambda x: datetime(2000, x, 1).strftime('%B'), key="analysis_month")
        
        transactions_df = data_handler.load_transactions()
        budgets_df = data_handler.load_budgets()
        
        comparison = FinancialCalculator.get_budget_comparison(
            transactions_df,
            budgets_df,
            analysis_year,
            analysis_month
        )
        
        if not comparison.empty:
            total_budget = comparison['amount'].sum()
            total_spent = comparison['actual'].sum()
            total_remaining = total_budget - total_spent
            overall_percent = (total_spent / total_budget * 100) if total_budget > 0 else 0
            
            st.markdown(f"""
                <div style="padding: 2rem; background: #069494; border-radius: 15px; color: white; margin-bottom: 2rem;">
                    <h3 style="margin-top: 0; font-size: 1.5rem;">Overall Budget Summary</h3>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem;">
                        <div>
                            <div style="opacity: 0.9; font-size: 0.9rem;">Total Budget</div>
                            <div style="font-size: 1.8rem; font-weight: 800;">{currency}{total_budget:,.2f}</div>
                        </div>
                        <div>
                            <div style="opacity: 0.9; font-size: 0.9rem;">Total Spent</div>
                            <div style="font-size: 1.8rem; font-weight: 800;">{currency}{total_spent:,.2f}</div>
                        </div>
                        <div>
                            <div style="opacity: 0.9; font-size: 0.9rem;">Remaining</div>
                            <div style="font-size: 1.8rem; font-weight: 800;">{currency}{total_remaining:,.2f}</div>
                        </div>
                        <div>
                            <div style="opacity: 0.9; font-size: 0.9rem;">Used</div>
                            <div style="font-size: 1.8rem; font-weight: 800;">{overall_percent:.1f}%</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            for _, row in comparison.iterrows():
                progress = min(row['percentage'] / 100, 1.0)
                
                if row['percentage'] >= 100:
                    status_color = "#FF8243"
                    status_text = "⚠️ Over Budget"
                    status_class = "alert-danger"
                elif row['percentage'] >= 80:
                    status_color = "#FCE883"
                    status_text = "⚡ Approaching Limit"
                    status_class = "alert-warning"
                else:
                    status_color = "#069494"
                    status_text = "✅ On Track"
                    status_class = "alert-success"
                
                st.markdown(f"""
                    <div style="padding: 2rem; background: white; border-radius: 15px; margin-bottom: 1.5rem; box-shadow: 0 5px 20px rgba(0,0,0,0.08); border-left: 5px solid {status_color};">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                            <h3 style="margin: 0; color: #2c3e50; font-size: 1.4rem;">📁 {row['category']}</h3>
                            <div style="padding: 0.5rem 1rem; background: {status_color}; color: {'white' if row['percentage'] >= 100 else ('#2c3e50' if row['percentage'] >= 80 else 'white')}; border-radius: 20px; font-weight: 700; font-size: 0.9rem;">
                                {status_text}
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
                            <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                                <div style="color: #7f8c8d; font-size: 0.85rem; margin-bottom: 0.5rem;">BUDGET</div>
                                <div style="font-size: 1.5rem; font-weight: 800; color: #2c3e50;">{currency}{row['amount']:,.2f}</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                                <div style="color: #7f8c8d; font-size: 0.85rem; margin-bottom: 0.5rem;">SPENT</div>
                                <div style="font-size: 1.5rem; font-weight: 800; color: {status_color};">{currency}{row['actual']:,.2f}</div>
                            </div>
                            <div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
                                <div style="color: #7f8c8d; font-size: 0.85rem; margin-bottom: 0.5rem;">REMAINING</div>
                                <div style="font-size: 1.5rem; font-weight: 800; color: {'#FF8243' if row['remaining'] < 0 else '#069494'};">{currency}{row['remaining']:,.2f}</div>
                            </div>
                        </div>
                        
                        <div style="background: #f0f0f0; height: 20px; border-radius: 10px; overflow: hidden; margin-bottom: 0.5rem;">
                            <div style="background: {status_color}; height: 100%; width: {progress * 100}%; transition: width 0.3s ease;"></div>
                        </div>
                        
                        <div style="text-align: center; font-weight: 700; color: {status_color}; font-size: 1.1rem;">
                            {row['percentage']:.1f}% Used
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="padding: 3rem; text-align: center; background: #f8f9fa; border-radius: 15px;">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
                    <h3 style="color: #2c3e50; margin-bottom: 0.5rem;">No Budgets Set</h3>
                    <p style="color: #7f8c8d;">Set budgets for {datetime(analysis_year, analysis_month, 1).strftime('%B %Y')} to start tracking!</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)