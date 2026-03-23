import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config("Uber Analytics", layout="wide")

# --------------------------------
# LOAD DATA (FIXED FILE NAME)
# --------------------------------
df = pd.read_csv("Uber_data .csv")

# --------------------------------
# SIDEBAR MENU
# --------------------------------
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Dataset", "Overview", "Ride Analytics"],
        icons=["table", "bar-chart", "graph-up"],
        menu_icon="car-front",
        default_index=0
    )

# --------------------------------
# DATASET PAGE
# --------------------------------
if selected == "Dataset":
    st.title("🚗 Data Explorer")
    st.divider()

    # -----------------------------
    # DATASET OVERVIEW
    # -----------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isna().sum().sum())

    st.divider()

    # -----------------------------
    # COLUMN SELECTION
    # -----------------------------
    st.subheader("📊 Select Column")
    selected_column = st.multiselect(
        "Select Columns to Display",
        df.columns,
        default=df.columns
    )

    filtered_df = df[selected_column]

    # -----------------------------
    # SEARCH
    # -----------------------------
    st.subheader("🔍 Search in Dataset")
    search_value = st.text_input("Enter Value to Search:")

    if search_value:
        filtered_df = filtered_df[
            filtered_df.astype(str).apply(
                lambda row: row.str.contains(search_value, case=False).any(),
                axis=1
            )
        ]

    # -----------------------------
    # COLUMN FILTER
    # -----------------------------
    st.subheader("🎯 Column Filter")
    col_a, col_b = st.columns(2)

    with col_a:
        filter_column = st.selectbox(
            "Select Column to Filter",
            options=["None"] + list(filtered_df.columns)
        )

    with col_b:
        filter_value = st.text_input("Enter Filter Value:")

    if filter_column != "None" and filter_value:
        filtered_df = filtered_df[
            filtered_df[filter_column]
            .astype(str)
            .str.contains(filter_value, case=False)
        ]

    st.divider()

    # -----------------------------
    # DEBUG INFO (OPTIONAL)
    # -----------------------------
    st.write("📌 Filtered Rows:", len(filtered_df))

    # -----------------------------
    # ROW DISPLAY (FIXED)
    # -----------------------------
    st.subheader("📅 Row Display")

    if len(filtered_df) > 0:
        num_rows = st.slider(
            "Select Number of Rows to Display",
            min_value=1,
            max_value=len(filtered_df),
            value=min(10, len(filtered_df))
        )

        display_df = filtered_df.head(num_rows)

        # -----------------------------
        # DATASET TABLE
        # -----------------------------
        st.subheader("📋 Dataset Table")
        st.dataframe(display_df, use_container_width=True)

    else:
        st.warning("⚠️ No data available after filtering")

    st.divider()

    # -----------------------------
    # DOWNLOAD BUTTON
    # -----------------------------
    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="⬇️ Download Filtered Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

# --------------------------------
# OVERVIEW PAGE
# --------------------------------
elif selected == "Overview":
    st.title("📊 Overview")
    st.info("Add charts here (Trips, Revenue, etc.)")

# --------------------------------
# RIDE ANALYTICS PAGE
# --------------------------------
elif selected == "Ride Analytics":
    st.title("🚕 Ride Analytics")
    st.info("Add advanced analytics here (Peak hours, Heatmaps, etc.)")