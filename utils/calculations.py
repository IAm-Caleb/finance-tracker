import pandas as pd
from datetime import datetime

class FinancialCalculator:
    
    @staticmethod
    def get_monthly_summary(df, year, month):
        if df.empty:
            return {
                'total_income': 0,
                'total_expenses': 0,
                'balance': 0,
                'savings_rate': 0
            }
        
        monthly_data = df[
            (df['date'].dt.year == year) & 
            (df['date'].dt.month == month)
        ]
        
        total_income = monthly_data[monthly_data['type'] == 'Income']['amount'].sum()
        total_expenses = monthly_data[monthly_data['type'] == 'Expense']['amount'].sum()
        balance = total_income - total_expenses
        
        savings_rate = 0
        if total_income > 0:
            savings_rate = (balance / total_income) * 100
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance,
            'savings_rate': savings_rate
        }
    
    @staticmethod
    def get_expense_by_category(df, year, month):
        if df.empty:
            return pd.DataFrame()
        
        monthly_expenses = df[
            (df['date'].dt.year == year) & 
            (df['date'].dt.month == month) &
            (df['type'] == 'Expense')
        ]
        
        if monthly_expenses.empty:
            return pd.DataFrame()
        
        category_summary = monthly_expenses.groupby('category')['amount'].sum().reset_index()
        category_summary = category_summary.sort_values('amount', ascending=False)
        
        return category_summary
    
    @staticmethod
    def get_monthly_trend(df, months=6):
        if df.empty:
            return pd.DataFrame()
        
        df['year_month'] = df['date'].dt.to_period('M')
        
        income_trend = df[df['type'] == 'Income'].groupby('year_month')['amount'].sum()
        expense_trend = df[df['type'] == 'Expense'].groupby('year_month')['amount'].sum()
        
        trend_df = pd.DataFrame({
            'Income': income_trend,
            'Expenses': expense_trend
        }).fillna(0)
        
        trend_df['Balance'] = trend_df['Income'] - trend_df['Expenses']
        trend_df.index = trend_df.index.to_timestamp()
        
        trend_df = trend_df.sort_index().tail(months)
        
        return trend_df
    
    @staticmethod
    def get_budget_comparison(transactions_df, budgets_df, year, month):
        if budgets_df.empty:
            return pd.DataFrame()
        
        month_str = f"{year}-{month:02d}"
        monthly_budgets = budgets_df[budgets_df['month'] == month_str]
        
        if monthly_budgets.empty:
            return pd.DataFrame()
        
        monthly_expenses = transactions_df[
            (transactions_df['date'].dt.year == year) & 
            (transactions_df['date'].dt.month == month) &
            (transactions_df['type'] == 'Expense')
        ]
        
        actual_expenses = monthly_expenses.groupby('category')['amount'].sum()
        
        comparison = monthly_budgets.copy()
        comparison['actual'] = comparison['category'].map(actual_expenses).fillna(0)
        comparison['remaining'] = comparison['amount'] - comparison['actual']
        comparison['percentage'] = (comparison['actual'] / comparison['amount'] * 100).round(1)
        
        return comparison
    
    @staticmethod
    def get_yearly_summary(df, year):
        if df.empty:
            return {
                'total_income': 0,
                'total_expenses': 0,
                'balance': 0,
                'average_monthly_income': 0,
                'average_monthly_expenses': 0
            }
        
        yearly_data = df[df['date'].dt.year == year]
        
        total_income = yearly_data[yearly_data['type'] == 'Income']['amount'].sum()
        total_expenses = yearly_data[yearly_data['type'] == 'Expense']['amount'].sum()
        balance = total_income - total_expenses
        
        months_count = yearly_data['date'].dt.month.nunique()
        if months_count == 0:
            months_count = 1
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': balance,
            'average_monthly_income': total_income / months_count,
            'average_monthly_expenses': total_expenses / months_count
        }
    
    @staticmethod
    def get_category_analysis(df, year):
        if df.empty:
            return pd.DataFrame()
        
        yearly_data = df[df['date'].dt.year == year]
        
        category_summary = yearly_data.groupby(['type', 'category'])['amount'].sum().reset_index()
        category_summary = category_summary.sort_values('amount', ascending=False)
        
        return category_summary