from datetime import datetime

import streamlit as st

st.set_page_config("Expense Tracker")
st.header("Expense Tracker")

if "transaction" not in st.session_state:
    st.session_state.transaction = []

if "balance" not in st.session_state:
    st.session_state.balance = 0.0

if "last_action" not in st.session_state:
    st.session_state.last_action = ""


st.subheader("Add Transaction")

col1, col2, col3, col4 = st.columns(4)
with col1:
    t_type = st.selectbox("Type",["Income","Expense"])

with col2:
    category = st.selectbox("Category",["Salary","Food","Shopping","Rent","Bills","Others"])

with col3:
    amount = st.number_input("Amount",min_value=0.0,format="%.2f")

with col4:
    description = st.text_input("Description")

if st.button("Add Transaction"):
    if amount > 0 and description.strip()!="":
        transaction = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": t_type,
            "category": category,
            "amount": amount,
            "description": description,
        }
        st.session_state.transaction.append(transaction)

        if t_type == "Income":
            st.session_state.balance += amount

        else:
            st.session_state.balance -= amount
        st.session_state.last_action = f"{t_type}"
        st.success("Transaction Added Successfully")

    else:
        st.warning("Please enter a valid Amount and Description")
    st.write(st.session_state.last_action)


