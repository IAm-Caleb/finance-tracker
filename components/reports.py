import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from utils.calculations import FinancialCalculator

def render_reports():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Financial Reports</h2>', unsafe_allow_html=True)
    
    data_handler = st.session_state.data_handler
    transactions_df = data_handler.load_transactions()
    currency = st.session_state.currency
    
    tab1, tab2, tab3 = st.tabs(["Monthly Report", "Yearly Report", "Category Analysis"])
    
    with tab1:
        st.subheader("Monthly Financial Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_year = st.number_input("Year", min_value=2020, max_value=2030, value=datetime.now().year, key="monthly_year")
        
        with col2:
            report_month = st.selectbox("Month", range(1, 13), index=datetime.now().month - 1, format_func=lambda x: datetime(2000, x, 1).strftime('%B'), key="monthly_month")
        
        summary = FinancialCalculator.get_monthly_summary(transactions_df, report_year, report_month)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Income", f"{currency}{summary['total_income']:,.2f}")
        
        with col2:
            st.metric("Total Expenses", f"{currency}{summary['total_expenses']:,.2f}")
        
        with col3:
            st.metric("Balance", f"{currency}{summary['balance']:,.2f}")
        
        with col4:
            st.metric("Savings Rate", f"{summary['savings_rate']:.1f}%")
        
        st.markdown("---")
        
        category_data = FinancialCalculator.get_expense_by_category(transactions_df, report_year, report_month)
        
        if not category_data.empty:
            st.subheader("Expense Distribution")
            
            colors = ['#FF8243', '#069494', '#FCE883', '#FFC0CB', '#FF6B6B', '#4ECDC4', '#95E1D3', '#F38181']
            
            fig = px.bar(
                category_data,
                x='category',
                y='amount',
                color='category',
                color_discrete_sequence=colors,
                labels={'amount': 'Amount', 'category': 'Category'}
            )
            
            fig.update_layout(
                showlegend=False,
                height=400,
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("Category Breakdown")
            st.dataframe(
                category_data.rename(columns={'category': 'Category', 'amount': f'Amount ({currency})'}),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No expense data available for this period.")
        
        st.markdown("---")
        st.subheader("Financial Summary")
        
        summary_text = f"""
        **Financial Report for {datetime(report_year, report_month, 1).strftime('%B %Y')}**
        
        This month, you earned a total income of {currency}{summary['total_income']:,.2f} and spent {currency}{summary['total_expenses']:,.2f} on various expenses.
        Your net balance for the month is {currency}{summary['balance']:,.2f}, representing a savings rate of {summary['savings_rate']:.1f}%.
        
        """
        
        if summary['savings_rate'] > 20:
            summary_text += "Your savings rate is excellent! You're managing your finances well."
        elif summary['savings_rate'] > 10:
            summary_text += "Your savings rate is good. Consider increasing it further for better financial security."
        elif summary['savings_rate'] > 0:
            summary_text += "You're saving money, but there's room for improvement. Review your expenses to find areas to cut back."
        else:
            summary_text += "Your expenses exceeded your income this month. Consider reviewing your spending habits and finding ways to reduce expenses."
        
        st.markdown(summary_text)
    
    with tab2:
        st.subheader("Yearly Financial Report")
        
        yearly_year = st.number_input("Select Year", min_value=2020, max_value=2030, value=datetime.now().year, key="yearly_year")
        
        yearly_summary = FinancialCalculator.get_yearly_summary(transactions_df, yearly_year)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Income", f"{currency}{yearly_summary['total_income']:,.2f}")
            st.metric("Avg Monthly Income", f"{currency}{yearly_summary['average_monthly_income']:,.2f}")
        
        with col2:
            st.metric("Total Expenses", f"{currency}{yearly_summary['total_expenses']:,.2f}")
            st.metric("Avg Monthly Expenses", f"{currency}{yearly_summary['average_monthly_expenses']:,.2f}")
        
        with col3:
            st.metric("Net Balance", f"{currency}{yearly_summary['balance']:,.2f}")
            savings_rate = (yearly_summary['balance'] / yearly_summary['total_income'] * 100) if yearly_summary['total_income'] > 0 else 0
            st.metric("Annual Savings Rate", f"{savings_rate:.1f}%")
        
        st.markdown("---")
        
        trend_data = FinancialCalculator.get_monthly_trend(transactions_df, months=12)
        
        if not trend_data.empty:
            yearly_trend = trend_data[trend_data.index.year == yearly_year]
            
            if not yearly_trend.empty:
                st.subheader("Monthly Trend")
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=yearly_trend.index.strftime('%B'),
                    y=yearly_trend['Income'],
                    name='Income',
                    marker_color='#069494'
                ))
                
                fig.add_trace(go.Bar(
                    x=yearly_trend.index.strftime('%B'),
                    y=yearly_trend['Expenses'],
                    name='Expenses',
                    marker_color='#FF8243'
                ))
                
                fig.update_layout(
                    barmode='group',
                    height=400,
                    xaxis_title="Month",
                    yaxis_title="Amount",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Category Analysis")
        
        category_year = st.number_input("Select Year", min_value=2020, max_value=2030, value=datetime.now().year, key="category_year")
        
        category_analysis = FinancialCalculator.get_category_analysis(transactions_df, category_year)
        
        if not category_analysis.empty:
            expenses = category_analysis[category_analysis['type'] == 'Expense']
            income = category_analysis[category_analysis['type'] == 'Income']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if not expenses.empty:
                    st.subheader("Expense Categories")
                    
                    fig = px.pie(
                        expenses,
                        values='amount',
                        names='category',
                        color_discrete_sequence=['#FF8243', '#069494', '#FCE883', '#FFC0CB', '#FF6B6B', '#4ECDC4']
                    )
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(
                        expenses[['category', 'amount']].rename(columns={'category': 'Category', 'amount': f'Amount ({currency})'}),
                        use_container_width=True,
                        hide_index=True
                    )
            
            with col2:
                if not income.empty:
                    st.subheader("Income Categories")
                    
                    fig = px.pie(
                        income,
                        values='amount',
                        names='category',
                        color_discrete_sequence=['#069494', '#FCE883', '#FFC0CB', '#FF8243']
                    )
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.dataframe(
                        income[['category', 'amount']].rename(columns={'category': 'Category', 'amount': f'Amount ({currency})'}),
                        use_container_width=True,
                        hide_index=True
                    )
        else:
            st.info("No data available for category analysis.")
    
    st.markdown("---")
    
    if st.button("Download Transaction Report (CSV)"):
        if not transactions_df.empty:
            csv = transactions_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"transactions_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.error("No transaction data to download.")
    
    st.markdown('</div>', unsafe_allow_html=True)