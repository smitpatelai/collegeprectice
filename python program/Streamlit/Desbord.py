import pandas as pd
import streamlit as st
import plotly.express as px   # ✅ missing import

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Sales Dashboard")

def load_data():
    df = pd.read_csv("sales_dataset_streamlit_dashboard.csv.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()
print(df)


# sidebar
st.sidebar.header("Filter Data")

# date
start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())

# region filter
region = st.sidebar.multiselect("Select Region", df["Region"].unique())

# product filter
product = st.sidebar.multiselect("Select Product", df["Product"].unique())

# top n
top_n = st.sidebar.slider("Top N Products", 1, 10, 5)


# apply filters
filtered_df = df[
    (df["Date"] >= pd.to_datetime(start_date)) &
    (df["Date"] <= pd.to_datetime(end_date)) &
    (df["Region"].isin(region)) &
    (df["Product"].isin(product))
]


# KPI SECTION
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
avg_sales = filtered_df["Sales"].mean()

# previous period comparison
previous_df = df[df["Date"] < pd.to_datetime(start_date)]
previous_sales = previous_df["Sales"].sum()

growth = 0
if previous_sales > 0:
    growth = ((total_sales - previous_sales) / previous_sales) * 100

col1, col2, col3 = st.columns(3)   # ✅ fixed variable name
col1.metric("Total Sales", f"{total_sales}", f"{round(growth, 2)}%")
col2.metric("Total Profit", f"{total_profit}")
col3.metric("Average Sales", f"{round(avg_sales, 2)}")  # ✅ fixed bracket


# chart section
col4, col5 = st.columns(2)

# region sales
sales_region = filtered_df.groupby("Region")["Sales"].sum().reset_index()
fig_bar = px.bar(
    sales_region,
    x="Region",   # ✅ fixed X -> x
    y="Sales",
    title="Sales by Region",
    color="Region"
)

col4.plotly_chart(fig_bar, use_container_width=True)


# TOP N PRODUCT
sales_product = filtered_df.groupby("Product")["Sales"].sum().reset_index()
sales_product = sales_product.sort_values(by="Sales", ascending=False).head(top_n)

fig_top = px.bar(
    sales_product,
    x="Product",
    y="Sales",
    title="Sales of Various Product",
    color="Product"
)

col5.plotly_chart(fig_top)


# trendline display -- > sales

fig_line = px. line(filtered_df,
                            x="Date", y="Sales", markers=True, title="Sales Trend Over Dataset")
st.plotly_chart(fig_line)


profit_product = filtered_df.groupby("Product") ["Profit"].sum().reset_index()
fig_pie = px.pie(profit_product,
                            values="Profit",
                            names="Product",
                            title="Profit By Product",
                            hole=0.4)
st.plotly_chart(fig_pie)

st.markdown("### Download Filtered Dataset")
csv = filtered_df.to_csv(index=False). encode('UTF-8')
st. download_button ( "Download CSV", csv,"Filtered_Dashboard_data. csv", "text/csv")

