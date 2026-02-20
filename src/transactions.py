import streamlit as st
from datetime import datetime
import pandas as pd

def render_transactions():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Transactions</h2>', unsafe_allow_html=True)
    
    data_handler = st.session_state.data_handler
    categories = data_handler.load_categories()
    currency = st.session_state.currency
    
    tab1, tab2 = st.tabs(["➕ Add Transaction", "📋 View & Manage Transactions"])
    
    with tab1:
        st.markdown("### Add a New Transaction", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            col1, col2 = st.columns([1, 1], gap="large")
            
            with col1:
                st.markdown('<div style="background: #f8f9fa; padding: 1.8rem; border-radius: 12px;">', unsafe_allow_html=True)
                
                trans_type = st.selectbox(
                    "Transaction Type",
                    ["Income", "Expense"],
                    key="add_type"
                )
                
                date = st.date_input(
                    "Date",
                    value=datetime.now().date(),
                    key="add_date"
                )
                
                amount = st.number_input(
                    f"Amount ({currency})",
                    min_value=0.01,
                    step=0.01,
                    format="%.2f",
                    key="add_amount"
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div style="background: #f8f9fa; padding: 1.8rem; border-radius: 12px;">', unsafe_allow_html=True)
                
                category_list = categories['income'] if trans_type == 'Income' else categories['expense']
                
                category = st.selectbox(
                    "Category",
                    options=category_list,
                    key="add_category"
                )
                
                description = st.text_input(
                    "Description (optional)",
                    placeholder="e.g. January salary, Grocery shopping, etc.",
                    key="add_description"
                )
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    add_button = st.button(
                        "✔️ Save Transaction",
                        use_container_width=True,
                        type="primary",
                        key="add_trans_btn"
                    )
                
                with col_btn2:
                    if st.button("➕ Add New Category", use_container_width=True, key="new_cat_btn"):
                        st.session_state.show_category_form = True
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # ── Add new category form ────────────────────────────────────────
        if st.session_state.get('show_category_form', False):
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form("add_category_form", clear_on_submit=True):
                st.markdown("#### Add New Category")
                new_category = st.text_input("Category name", placeholder="e.g. Freelance, Transport, Entertainment")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.form_submit_button("Save Category", use_container_width=True, type="primary"):
                        if new_category.strip():
                            data_handler.save_category(trans_type.lower(), new_category.strip())
                            st.success(f"Category **{new_category}** added successfully!")
                            st.session_state.show_category_form = False
                            st.rerun()
                        else:
                            st.warning("Please enter a category name.")
                
                with c2:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.session_state.show_category_form = False
                        st.rerun()
        
        # ── Feedback after adding transaction ────────────────────────────
        if add_button:
            if amount > 0:
                data_handler.save_transaction(
                    date=date.strftime('%Y-%m-%d'),
                    amount=amount,
                    category=category,
                    description=description.strip() if description.strip() else "No description",
                    trans_type=trans_type
                )
                st.success("Transaction saved successfully!")
                st.rerun()
            else:
                st.error("Amount must be greater than 0.")
    
    # ────────────────────────────────────────────────────────────────
    #                   VIEW ALL TRANSACTIONS TAB
    # ────────────────────────────────────────────────────────────────
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        transactions_df = data_handler.load_transactions()
        
        if not transactions_df.empty:
            with st.container():
                f1, f2, f3 = st.columns(3)
                
                with f1:
                    filter_type = st.multiselect(
                        "Transaction Type",
                        options=['Income', 'Expense'],
                        default=['Income', 'Expense'],
                        key="filter_type"
                    )
                
                with f2:
                    all_cats = sorted(transactions_df['category'].unique())
                    filter_category = st.multiselect(
                        "Category",
                        options=all_cats,
                        default=all_cats,
                        key="filter_cat"
                    )
                
                with f3:
                    sort_order = st.selectbox(
                        "Sort by",
                        ["Newest first", "Oldest first", "Highest amount", "Lowest amount"],
                        key="sort_order"
                    )
            
            filtered_df = transactions_df[
                (transactions_df['type'].isin(filter_type)) &
                (transactions_df['category'].isin(filter_category))
            ].copy()
            
            # Apply sorting
            if sort_order == "Newest first":
                filtered_df = filtered_df.sort_values('date', ascending=False)
            elif sort_order == "Oldest first":
                filtered_df = filtered_df.sort_values('date', ascending=True)
            elif sort_order == "Highest amount":
                filtered_df = filtered_df.sort_values('amount', ascending=False)
            else:
                filtered_df = filtered_df.sort_values('amount', ascending=True)
            
            st.markdown(f"**Showing {len(filtered_df)} transaction{'s' if len(filtered_df) != 1 else ''}**")
            
            for idx, row in filtered_df.iterrows():
                color = "#2ecc71" if row['type'] == 'Income' else "#e74c3c"
                icon  = "↑" if row['type'] == 'Income' else "↓"
                
                with st.expander(
                    f"{icon} {row['date'].strftime('%d %b %Y')} • {row['category']} • {currency}{row['amount']:,.2f}"
                ):
                    st.markdown(f"**Type:** {row['type']}")
                    st.markdown(f"**Category:** {row['category']}")
                    st.markdown(f"**Amount:** <span style='color:{color};font-weight:bold;font-size:1.25rem;'>{currency}{row['amount']:,.2f}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Description:** {row['description']}")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🗑️ Delete", key=f"del_{idx}", use_container_width=True):
                            data_handler.delete_transaction(idx)
                            st.success("Transaction deleted.")
                            st.rerun()
                    
                    with c2:
                        if st.button("✏️ Edit", key=f"edit_{idx}", use_container_width=True):
                            st.session_state[f'editing_{idx}'] = True
                            st.rerun()
                    
                    if st.session_state.get(f'editing_{idx}', False):
                        with st.form(f"edit_form_{idx}"):
                            st.markdown("#### Edit Transaction")
                            
                            edit_type = st.selectbox("Type", ["Income", "Expense"], index=0 if row['type'] == 'Income' else 1, key=f"etype_{idx}")
                            edit_date = st.date_input("Date", row['date'], key=f"edate_{idx}")
                            edit_amount = st.number_input("Amount", value=float(row['amount']), min_value=0.01, step=0.01, format="%.2f", key=f"eamt_{idx}")
                            
                            edit_cat_list = categories['income'] if edit_type == 'Income' else categories['expense']
                            try:
                                idx_cat = edit_cat_list.index(row['category'])
                            except ValueError:
                                idx_cat = 0
                            edit_category = st.selectbox("Category", edit_cat_list, index=idx_cat, key=f"ecat_{idx}")
                            
                            edit_desc = st.text_input("Description", value=row['description'], key=f"edesc_{idx}")
                            
                            cc1, cc2 = st.columns(2)
                            with cc1:
                                if st.form_submit_button("💾 Save Changes", type="primary"):
                                    data_handler.update_transaction(
                                        idx,
                                        edit_date.strftime('%Y-%m-%d'),
                                        edit_amount,
                                        edit_category,
                                        edit_desc,
                                        edit_type
                                    )
                                    st.session_state[f'editing_{idx}'] = False
                                    st.success("Transaction updated!")
                                    st.rerun()
                            with cc2:
                                if st.form_submit_button("Cancel"):
                                    st.session_state[f'editing_{idx}'] = False
                                    st.rerun()
        else:
            st.markdown("""
                <div style="padding: 4rem 2rem; text-align: center; background: #f8f9fa; border-radius: 16px; margin: 2rem 0;">
                    <div style="font-size: 5rem; margin-bottom: 1.5rem;">💸</div>
                    <h3 style="color: #34495e; margin-bottom: 0.8rem;">No transactions yet</h3>
                    <p style="color: #7f8c8d; font-size: 1.1rem;">
                        Add your first income or expense using the <strong>Add Transaction</strong> tab above.
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)