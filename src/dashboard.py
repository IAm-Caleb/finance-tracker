# import streamlit as st
# import plotly.graph_objects as go
# import plotly.express as px
# from datetime import datetime
# from utils.calculations import FinancialCalculator

# def render_dashboard():
#     data_handler = st.session_state.data_handler
#     transactions_df = data_handler.load_transactions()
#     currency = st.session_state.currency
    
#     current_date = datetime.now()
#     current_year = current_date.year
#     current_month = current_date.month
    
#     summary = FinancialCalculator.get_monthly_summary(transactions_df, current_year, current_month)
    
#     st.markdown(f'<h2 style="color: #2c3e50; font-size: 2rem; font-weight: 700; margin-bottom: 2rem;">Welcome Back! Here\'s Your Financial Overview</h2>', unsafe_allow_html=True)
    
#     col1, col2, col3, col4 = st.columns(4, gap="large")
    
#     with col1:
#         st.markdown(f"""
#             <div class="metric-card income">
#                 <div class="metric-label">Total Income</div>
#                 <div class="metric-value">{currency}{summary['total_income']:,.2f}</div>
#                 <div class="metric-change positive">+12.5% from last month</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown(f"""
#             <div class="metric-card expense">
#                 <div class="metric-label">Total Expenses</div>
#                 <div class="metric-value">{currency}{summary['total_expenses']:,.2f}</div>
#                 <div class="metric-change negative">+5.2% from last month</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         balance_class = "income" if summary['balance'] >= 0 else "expense"
#         st.markdown(f"""
#             <div class="metric-card {balance_class}">
#                 <div class="metric-label">Net Balance</div>
#                 <div class="metric-value">{currency}{summary['balance']:,.2f}</div>
#                 <div class="metric-change positive">Your monthly surplus</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown(f"""
#             <div class="metric-card savings">
#                 <div class="metric-label">Savings Rate</div>
#                 <div class="metric-value">{summary['savings_rate']:.1f}%</div>
#                 <div class="metric-change positive">Excellent progress!</div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     col_left, col_right = st.columns(2, gap="large")
    
#     with col_left:
#         st.markdown('<div class="content-card">', unsafe_allow_html=True)
#         st.markdown('<h3 class="section-title">Expense Distribution</h3>', unsafe_allow_html=True)
        
#         category_data = FinancialCalculator.get_expense_by_category(transactions_df, current_year, current_month)
        
#         if not category_data.empty:
#             colors = ['#FF8243', '#069494', '#FCE883', '#FFC0CB', '#667eea', '#f093fb', '#4facfe', '#43e97b']
            
#             fig = go.Figure(data=[go.Pie(
#                 labels=category_data['category'],
#                 values=category_data['amount'],
#                 hole=0.5,
#                 marker=dict(colors=colors, line=dict(color='white', width=3)),
#                 textposition='outside',
#                 textinfo='label+percent',
#                 textfont=dict(size=12, color='#2c3e50', family='Poppins'),
#                 hovertemplate='<b>%{label}</b><br>Amount: ' + currency + '%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
#             )])
            
#             fig.update_layout(
#                 showlegend=False,
#                 height=400,
#                 margin=dict(t=20, b=20, l=20, r=20),
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 font=dict(family='Poppins', size=12)
#             )
            
#             st.plotly_chart(fig, use_container_width=True)
            
#             total_expense = category_data['amount'].sum()
#             top_category = category_data.iloc[0]
#             st.markdown(f"""
#                 <div style="padding: 1rem; background: #f8f9fa; border-radius: 10px; margin-top: 1rem;">
#                     <p style="margin: 0; color: #2c3e50; font-weight: 600;">💡 <strong>{top_category['category']}</strong> is your biggest expense at <strong>{currency}{top_category['amount']:,.2f}</strong> ({top_category['amount']/total_expense*100:.1f}% of total)</p>
#                 </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.info("No expense data available for this month. Start tracking to see your spending patterns!")
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col_right:
#         st.markdown('<div class="content-card">', unsafe_allow_html=True)
#         st.markdown('<h3 class="section-title">Cashflow Trend (6 Months)</h3>', unsafe_allow_html=True)
        
#         trend_data = FinancialCalculator.get_monthly_trend(transactions_df, months=6)
        
#         if not trend_data.empty:
#             fig = go.Figure()
            
#             fig.add_trace(go.Scatter(
#                 x=trend_data.index,
#                 y=trend_data['Income'],
#                 mode='lines+markers',
#                 name='Income',
#                 line=dict(color='#069494', width=4, shape='spline'),
#                 marker=dict(size=10, color='#069494', line=dict(width=2, color='white')),
#                 fill='tonexty',
#                 fillcolor='rgba(6, 148, 148, 0.1)',
#                 hovertemplate='<b>Income</b><br>%{x|%B %Y}<br>' + currency + '%{y:,.2f}<extra></extra>'
#             ))
            
#             fig.add_trace(go.Scatter(
#                 x=trend_data.index,
#                 y=trend_data['Expenses'],
#                 mode='lines+markers',
#                 name='Expenses',
#                 line=dict(color='#FF8243', width=4, shape='spline'),
#                 marker=dict(size=10, color='#FF8243', line=dict(width=2, color='white')),
#                 fill='tozeroy',
#                 fillcolor='rgba(255, 130, 67, 0.1)',
#                 hovertemplate='<b>Expenses</b><br>%{x|%B %Y}<br>' + currency + '%{y:,.2f}<extra></extra>'
#             ))
            
#             fig.update_layout(
#                 height=400,
#                 margin=dict(t=20, b=20, l=20, r=20),
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 xaxis=dict(
#                     title="",
#                     showgrid=False,
#                     tickfont=dict(size=11, color='#7f8c8d', family='Poppins')
#                 ),
#                 yaxis=dict(
#                     title="",
#                     showgrid=True,
#                     gridcolor='rgba(0,0,0,0.05)',
#                     tickfont=dict(size=11, color='#7f8c8d', family='Poppins')
#                 ),
#                 hovermode='x unified',
#                 legend=dict(
#                     orientation="h",
#                     yanchor="bottom",
#                     y=1.02,
#                     xanchor="right",
#                     x=1,
#                     bgcolor='rgba(255,255,255,0.8)',
#                     bordercolor='rgba(0,0,0,0.1)',
#                     borderwidth=1,
#                     font=dict(size=12, family='Poppins')
#                 ),
#                 font=dict(family='Poppins')
#             )
            
#             st.plotly_chart(fig, use_container_width=True)
            
#             avg_income = trend_data['Income'].mean()
#             avg_expense = trend_data['Expenses'].mean()
#             st.markdown(f"""
#                 <div style="padding: 1rem; background: #f8f9fa; border-radius: 10px; margin-top: 1rem;">
#                     <p style="margin: 0; color: #2c3e50; font-weight: 600;">📊 6-month average: <strong style="color: #069494;">Income {currency}{avg_income:,.2f}</strong> | <strong style="color: #FF8243;">Expenses {currency}{avg_expense:,.2f}</strong></p>
#                 </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.info("Start adding transactions to see your financial trends over time!")
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     st.markdown('<div class="content-card">', unsafe_allow_html=True)
#     st.markdown('<h3 class="section-title">Recent Transactions</h3>', unsafe_allow_html=True)
    
#     if not transactions_df.empty:
#         recent = transactions_df.sort_values('date', ascending=False).head(5)
        
#         for idx, row in recent.iterrows():
#             trans_class = "income" if row['type'] == 'Income' else "expense"
#             trans_icon = "💰" if row['type'] == 'Income' else "💳"
#             trans_color = "#069494" if row['type'] == 'Income' else "#FF8243"
            
#             st.markdown(f"""
#                 <div class="transaction-item {trans_class}">
#                     <div style="display: flex; justify-content: space-between; align-items: center;">
#                         <div style="display: flex; align-items: center; gap: 1rem;">
#                             <div style="font-size: 2rem;">{trans_icon}</div>
#                             <div>
#                                 <div style="font-weight: 700; font-size: 1.1rem; color: #2c3e50;">{row['category']}</div>
#                                 <div style="color: #7f8c8d; font-size: 0.9rem;">{row['description']}</div>
#                             </div>
#                         </div>
#                         <div style="text-align: right;">
#                             <div style="font-weight: 800; font-size: 1.3rem; color: {trans_color};">{currency}{row['amount']:,.2f}</div>
#                             <div style="color: #7f8c8d; font-size: 0.85rem;">{row['date'].strftime('%b %d, %Y')}</div>
#                         </div>
#                     </div>
#                 </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.info("No transactions yet. Head over to the Transactions tab to add your first entry!")
    
#     st.markdown('</div>', unsafe_allow_html=True)


import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
from utils.calculations import FinancialCalculator

def render_dashboard():
    dh = st.session_state.data_handler
    df = dh.load_transactions()
    currency = st.session_state.currency

    now = datetime.now()
    summary = FinancialCalculator.get_monthly_summary(df, now.year, now.month)

    st.markdown("## 👋 Welcome back")
    st.markdown("Here’s a clear snapshot of your finances this month.")

    col1, col2, col3, col4 = st.columns(4)

    def metric(col, label, value, cls, note):
        with col:
            st.markdown(f"""
            <div class="card metric-card {cls}">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-sub">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    metric(col1, "Income", f"{currency}{summary['total_income']:,.2f}", "income", "Monthly earnings")
    metric(col2, "Expenses", f"{currency}{summary['total_expenses']:,.2f}", "expense", "Money spent")
    metric(col3, "Balance", f"{currency}{summary['balance']:,.2f}", "balance", "Net result")
    metric(col4, "Savings Rate", f"{summary['savings_rate']:.1f}%", "savings", "Income saved")

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Expense Breakdown</div>', unsafe_allow_html=True)

        cat = FinancialCalculator.get_expense_by_category(df, now.year, now.month)
        if cat.empty:
            st.info("No expenses recorded yet.")
        else:
            fig = go.Figure(go.Pie(
                labels=cat["category"],
                values=cat["amount"],
                hole=.5
            ))
            fig.update_layout(height=350, margin=dict(t=10,b=10))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Cashflow Trend</div>', unsafe_allow_html=True)

        trend = FinancialCalculator.get_monthly_trend(df, 6)
        if trend.empty:
            st.info("Add transactions to see trends.")
        else:
            fig = go.Figure()
            fig.add_scatter(x=trend.index, y=trend["Income"], name="Income")
            fig.add_scatter(x=trend.index, y=trend["Expenses"], name="Expenses")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recent Transactions</div>', unsafe_allow_html=True)

    if df.empty:
        st.info("No transactions yet.")
    else:
        for _, r in df.sort_values("date", ascending=False).head(5).iterrows():
            color = "#0f766e" if r["type"] == "Income" else "#ea580c"
            st.markdown(f"""
            <div class="transaction">
                <div class="transaction-left">
                    <strong>{r["category"]}</strong>
                    <span>{r["description"]}</span>
                </div>
                <div class="transaction-amount" style="color:{color}">
                    {currency}{r["amount"]:,.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
