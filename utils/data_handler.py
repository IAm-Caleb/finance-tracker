import pandas as pd
import os
from datetime import datetime
import json

class DataHandler:
    def __init__(self):
        self.data_dir = "data"
        self.transactions_file = os.path.join(self.data_dir, "transactions.csv")
        self.budgets_file = os.path.join(self.data_dir, "budgets.csv")
        self.settings_file = os.path.join(self.data_dir, "settings.json")
        self.categories_file = os.path.join(self.data_dir, "categories.json")
        
        self._ensure_data_directory()
        self._initialize_files()
    
    def _ensure_data_directory(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _initialize_files(self):
        if not os.path.exists(self.transactions_file):
            df = pd.DataFrame(columns=['date', 'amount', 'category', 'description', 'type'])
            df.to_csv(self.transactions_file, index=False)
        
        if not os.path.exists(self.budgets_file):
            df = pd.DataFrame(columns=['category', 'amount', 'month'])
            df.to_csv(self.budgets_file, index=False)
        
        if not os.path.exists(self.settings_file):
            settings = {
                'currency': '$',
                'monthly_income_target': 5000
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        
        if not os.path.exists(self.categories_file):
            categories = {
                'expense': [
                    'Food & Dining',
                    'Transportation',
                    'Shopping',
                    'Entertainment',
                    'Bills & Utilities',
                    'Healthcare',
                    'Education',
                    'Travel',
                    'Other'
                ],
                'income': [
                    'Salary',
                    'Freelance',
                    'Investment',
                    'Business',
                    'Gift',
                    'Other'
                ]
            }
            with open(self.categories_file, 'w') as f:
                json.dump(categories, f)
    
    def load_transactions(self):
        df = pd.read_csv(self.transactions_file)
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')

        return df
    
    def save_transaction(self, date, amount, category, description, trans_type):
        df = self.load_transactions()
        new_row = pd.DataFrame([{
            'date': date,
            'amount': amount,
            'category': category,
            'description': description,
            'type': trans_type
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.transactions_file, index=False)
        return True
    
    def delete_transaction(self, index):
        df = self.load_transactions()
        df = df.drop(index)
        df = df.reset_index(drop=True)
        df.to_csv(self.transactions_file, index=False)
        return True
    
    def update_transaction(self, index, date, amount, category, description, trans_type):
        df = self.load_transactions()
        df.loc[index, 'date'] = date
        df.loc[index, 'amount'] = amount
        df.loc[index, 'category'] = category
        df.loc[index, 'description'] = description
        df.loc[index, 'type'] = trans_type
        df.to_csv(self.transactions_file, index=False)
        return True
    
    def load_budgets(self):
        df = pd.read_csv(self.budgets_file)
        return df
    
    def save_budget(self, category, amount, month):
        df = self.load_budgets()
        existing = df[(df['category'] == category) & (df['month'] == month)]
        
        if not existing.empty:
            df.loc[(df['category'] == category) & (df['month'] == month), 'amount'] = amount
        else:
            new_row = pd.DataFrame([{
                'category': category,
                'amount': amount,
                'month': month
            }])
            df = pd.concat([df, new_row], ignore_index=True)
        
        df.to_csv(self.budgets_file, index=False)
        return True
    
    def load_categories(self):
        with open(self.categories_file, 'r') as f:
            return json.load(f)
    
    def save_category(self, category_type, category_name):
        categories = self.load_categories()
        if category_name not in categories[category_type]:
            categories[category_type].append(category_name)
            with open(self.categories_file, 'w') as f:
                json.dump(categories, f)
        return True
    
    def load_settings(self):
        with open(self.settings_file, 'r') as f:
            return json.load(f)
    
    def save_settings(self, settings):
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)
        return True
    
    def reset_all_data(self):
        if os.path.exists(self.transactions_file):
            df = pd.DataFrame(columns=['date', 'amount', 'category', 'description', 'type'])
            df.to_csv(self.transactions_file, index=False)
        
        if os.path.exists(self.budgets_file):
            df = pd.DataFrame(columns=['category', 'amount', 'month'])
            df.to_csv(self.budgets_file, index=False)
        
        return True