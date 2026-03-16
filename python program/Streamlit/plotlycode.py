import streamlit as st
import plotly.express as px
import pandas as pd

st.header("Chart Using Plotly")

# expenses = {
#     "Category": ["Rent", "EMI", "Food", "Shopping", "Others"],
#     "debit": [15000, 5500, 6000, 18900, 15780]
# }
#
# df = pd.DataFrame(expenses)
#
# fig = px.bar(df, x="Category", y="debit", title="Expense Track")
#
# st.plotly_chart(fig)


# data = {"Hours": [3,4, 5, 6, 7, 8],
#         "Marks":[75,80,85,90,95,100]}
# df = pd.DataFrame (data)
# fig = px. scatter(df, x="Hours", y="Marks", title="Hours V/S Marks")
# st.plotly_chart(fig)

st.header("Chart Using Plotly")

df = px.data.stocks()

fig = px.line(df, x='date',
              y=['GOOG','AAPL','AMZN','FB','NFLX','MSFT'],
              title="Stock Market Chart")

st.plotly_chart(fig)