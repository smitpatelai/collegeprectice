import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

st.set_page_config("Uber Analytics", layout="wide")

df = pd.read_csv("Uber_data .csv")

# sidebar menu

with st.sidebar:
    selected = option_menu("Main Menu", ["Dataset", "Overview", "Ride Analytics"],
                           icons=["table", "bar-chart", "graph-up"], menu_icon="car-front",
                           default_index=0)

if selected == "Dataset":
    st.title("Data Explorer")
    st.divider()

    # dataset overview

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Value", df.isna().sum().sum())

    st.divider()

    # column selection

    st.subheader("Select Column")
    selected_column = st.multiselect("Select Columns to Display",
                                     df.columns, default=df.columns)
    filtered_df = df[selected_column]

    # search

    st.subheader("Search in Dataset")
    search_value = st.text_input("Enter Value to Search:")
    if search_value:
        filtered_df = filtered_df[filtered_df.astype(str).apply(
            lambda row: row.str.contains(search_value, case=False).any(), axis=1
        )]

    st.dataframe(filtered_df)
