import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd

st.set_page_config("Uber Analytics", layout="wide")

# FIX 1: remove extra space in file name
df = pd.read_csv("Uber_data .csv")

# FIX 2: clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

# sidebar menu
with st.sidebar:
    selected = option_menu("🛸Main Menu",
                           ["Dataset", "Overview", "Ride Analytics"],
                            icons=["table", "bar-chart", "graph-up"],
                            menu_icon="car-front",
                            default_index=0)

if selected == "Dataset":
    st.title("Data Explorer")
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Value", df.isna().sum().sum())

    st.divider()

    st.subheader("📊Select Column")
    selected_column = st.multiselect("Select Columns to Display",
                                     df.columns, default=df.columns)
    filtered_df = df[selected_column]

    st.subheader("🔍Search in Dataset")
    search_value = st.text_input("Enter Value to Search:")
    if search_value:
        filtered_df = filtered_df[filtered_df.astype(str).apply(
            lambda row: row.str.contains(search_value, case=False).any(), axis=1
        )]
    st.dataframe(filtered_df)

    st.subheader("🛡️Column Filter")
    col_a, col_b = st.columns(2)

    with col_a:
        filter_column = st.selectbox(
            "Select Column to Filter",
            options=["None"] + list(filtered_df.columns)
        )

    with col_b:
        if filter_column != "None":
            unique_values = filtered_df[filter_column].dropna().astype(str).unique()
            filter_value = st.selectbox(
                "Enter Filter Value:",
                options=["None"] + sorted(unique_values)
            )
        else:
            filter_value = "None"

    if filter_column != "None" and filter_value != "None":
        filtered_df = filtered_df[
            filtered_df[filter_column].astype(str) == filter_value
        ]

    st.divider()

    st.write("📌 Filtered Rows:", len(filtered_df))

    st.subheader("📜Row Display")
    num_rows = st.slider("Select Number of Rows to Display",
                         min_value=5,
                         max_value=max(5, len(filtered_df)),
                         value=min(10, len(filtered_df)),
                         step=5)

    display_df = filtered_df.head(num_rows)

    st.divider()

    st.subheader("🧾Dataset Table")
    st.dataframe(display_df, use_container_width=True)

    st.divider()

    st.subheader("🕹️Download")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_uber_data.csv",
        mime="text/csv"
    )

elif selected == "Overview":
    st.title("📊 Overview")
    st.info("Add charts here (Trips, Revenue, etc.)")

    col1, col2 = st.columns(2)
    col1.metric("Total Rides", len(df))
    col2.metric("Revenue", df["Booking Value"].sum())

    total_revenue = df["Booking Value"].sum()

    st.divider()

    st.header("💵Business Unit Performance Metrix")

    # FIX 3: handle missing Ride Rating safely
    if "Ride Rating" not in df.columns:
        df["Ride Rating"] = 0   # fallback to avoid crash

    bu_matrix = df.groupby("Vehicle Type").agg(
        Total_booking=("Booking ID", "count"),
        Revenue_Generated=("Booking Value", "sum"),
        Avg_Distance=("Ride Distance", "mean"),
        Avg_Rating=("Ride Rating", "mean")
    )

    # FIX 4: correct column name
    bu_matrix["Revenue Share%"] = (
        bu_matrix["Revenue_Generated"] / total_revenue * 100
        if total_revenue > 0 else 0
    )

    st.dataframe(bu_matrix.style.format({
        "Revenue_Generated": "${:,.2f}",
        "Avg_Distance": "{:,.2f} km",
        "Avg_Rating": "{:,.1f}",
        "Revenue Share%": "{:,.1f}%"
    }).background_gradient(subset=["Revenue_Generated"], cmap="YlOrRd"))

    #Operation Efficiency

    col_eff , col_can = st.columns(2)
    with col_eff:
        st.header("⚙️Operational Efficiency")
        eff_df = df.groupby("Vehicle Type")[["Avg VTAT","Avg CTAT"]].mean()
        st.write("Average Turn Around Time {%in Minutes%}")
        st.dataframe(eff_df.style.highlight_max(axis=0,color="#438f55").highlight_min(axis=0,color="#368569"),
                     use_container_width=True)
    total_rides = len(df)
    with col_can:
        st.subheader("✖️Cancellation Audit")
        status_count = df["Booking Status"].value_counts().to_frame(name="Count")
        status_count["Share %"]= (status_count["Count"] / total_rides*100)
        st.dataframe(status_count,use_container_width=True)
    st.divider()
    with col_can:
        st.header("🏁Completed Rides by Payment Method")
        completed_rides = df.groupby("Payment Method")["Booking ID"].count().reset_index()
        completed_rides.columns = ["Payment Method", "Total Rides"]
        st.dataframe(completed_rides, use_container_width=True)
    st.divider()

    #Financial Analysis
    st.header("🎯Financial Deep Dive")
    pay_col , reason_col = st.columns([4,6])
    with pay_col:
        st.markdown(" ** Payment Method Distribution")
        pay_summary = (df["Payment Method"].value_counts(normalize=True) * 100)
        st.dataframe(pay_summary)





elif selected == "Ride Analytics":
    st.title("🚕 Ride Analytics")
    st.info("Add advanced analytics here (Peak hours, Heatmaps, etc.)")