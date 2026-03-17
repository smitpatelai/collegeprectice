import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go


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

# st.header("Chart Using Plotly")
#
# df = px.data.stocks()
#
# fig = px.line(df, x='date',
#               y=['GOOG','AAPL','AMZN','FB','NFLX','MSFT'],
#               title="Stock Market Chart")
#
# st.plotly_chart(fig)

# df = px.data.gapminder().query("country in ['Canada', 'Botswana']")
#
# fig = px.line(df, x="lifeExp", y="gdpPercap", color="country", text="year")
# fig.update_traces(textposition="bottom right")
# fig.show()

# np.random.seed(1)
#
# N = 100
# random_x = np.linspace(0, 1, N)
# random_y0 = np.random.randn(N) + 5
# random_y1 = np.random.randn(N)
# random_y2 = np.random.randn(N) - 5
#
# fig = go.Figure()
#
# # Add traces
# fig.add_trace(go.Scatter(x=random_x, y=random_y0,
#                     mode='markers',
#                     name='markers'))
# fig.add_trace(go.Scatter(x=random_x, y=random_y1,
#                     mode='lines+markers',
#                     name='lines+markers'))
# fig.add_trace(go.Scatter(x=random_x, y=random_y2,
#                     mode='lines',
#                     name='lines'))
#
# fig.show()
# data = {
#     "funding":[5000000, 2000000, 8000000],
#     "team_experience":[5,3,8],
#     "market_size":[100,60,150],
#     "success":[1,0,1]
# }
#
# df = pd.DataFrame(data)
# fig3d = go.Figure(data=[go.Scatter3d(
#     x = df['funding'] / 1000000,
#     y = df['team_experience'],
#     z = df['market_size'],
#     mode = 'markers',
#     marker = dict(
#         size = 7,
#         color = df['success'],
#         colorscale = 'Viridis',
#         opacity = 0.9
#     )
# )])

# Read data from a csv
# z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
#
# fig = go.Figure(data=[go.Surface(z=z_data.values)])
#
# fig.update_layout(title=dict(text='Mt Bruno Elevation'), autosize=False,
#                   width=500, height=500,
#                   margin=dict(l=65, r=50, b=65, t=90))
#
# fig.show()
# us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
# us_cities = us_cities.query("State in ['New York', 'Ohio']")
#
# fig = px.line_map(us_cities, lat="lat", lon="lon", color="State", zoom=3, height=300)
#
# fig.update_layout(map_style="open-street-map", map_zoom=4, map_center_lat = 41,
#     margin={"r":0,"t":0,"l":0,"b":0},
#     width =1400,
#     height =900)
# fig.show()


# Page title
st.title("3D Surface Plot - Mt Bruno Elevation")

# Read data from CSV
z_data = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv"
)

# Create surface plot
fig = go.Figure(data=[go.Surface(z=z_data.values)])

# Layout
fig.update_layout(
    title="Mt Bruno Elevation",
    autosize=False,
    width=500,
    height=500,
    margin=dict(l=65, r=50, b=65, t=90)
)

# Show chart in Streamlit
st.plotly_chart(fig)