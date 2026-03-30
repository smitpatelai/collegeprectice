import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Enterprise Analytics Dashboard", layout="wide")

df = pd.read_csv("annual-enterprise.csv")

# =========================
# DATA CLEANING (IMPORTANT)
# =========================
df.columns = df.columns.str.strip()

# Convert Value column safely
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

# Remove invalid rows
df = df.dropna(subset=["Value"])

# =========================
# SIDEBAR MENU
# =========================
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Dataset", "Overview", "Industry Analytics", "Data Assistant"],
        icons=["table", "bar-chart", "graph-up", "robot"],
        menu_icon="building",
        default_index=0
    )

# =========================
# DATASET PAGE
# =========================
if selected == "Dataset":
    st.title("📊 Data Explorer")
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isna().sum().sum())

    st.divider()

    selected_cols = st.multiselect("Select Columns", df.columns, default=df.columns)
    filtered_df = df[selected_cols]

    search = st.text_input("Search in Data")
    if search:
        filtered_df = filtered_df[
            filtered_df.astype(str).apply(
                lambda row: row.str.contains(search, case=False).any(), axis=1
            )
        ]

    st.dataframe(filtered_df, use_container_width=True)

    # download
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", csv, "filtered_data.csv", "text/csv")

# =========================
# OVERVIEW PAGE
# =========================
elif selected == "Overview":
    st.title("📈 Enterprise Overview")

    total_value = df["Value"].sum()
    avg_value = df["Value"].mean()
    total_years = df["Year"].nunique()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Value", f"{total_value:,.0f}")
    c2.metric("Average Value", f"{avg_value:,.2f}")
    c3.metric("Years Covered", total_years)

    st.divider()

    # Trend
    st.subheader("📊 Value Trend Over Years")
    trend = df.groupby("Year")["Value"].sum().reset_index()

    fig1 = px.line(trend, x="Year", y="Value", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

    # Top industries
    st.subheader("🏭 Top Industries")
    top_ind = df.groupby("Industry_name_NZSIOC")["Value"].sum().nlargest(10).reset_index()

    fig2 = px.bar(top_ind, x="Value", y="Industry_name_NZSIOC", orientation="h")
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# INDUSTRY ANALYTICS
# =========================
elif selected == "Industry Analytics":
    st.title("🏭 Industry Analytics")

    # =========================
    # CLEAN DATA FOR CHARTS
    # =========================
    clean_df = df.copy()

    # Drop nulls in required columns
    clean_df = clean_df.dropna(subset=[
        "Industry_name_NZSIOC",
        "Variable_name",
        "Value"
    ])

    # Limit data (VERY IMPORTANT for Sunburst)
    clean_df = clean_df.groupby(
        ["Industry_name_NZSIOC", "Variable_name"],
        as_index=False
    )["Value"].sum()

    # Take top 50 rows to avoid overload
    clean_df = clean_df.nlargest(50, "Value")

    # =========================
    # SUNBURST
    # =========================
    st.subheader("🌐 Sunburst Chart")

    try:
        fig1 = px.sunburst(
            clean_df,
            path=["Industry_name_NZSIOC", "Variable_name"],
            values="Value",
            color="Value"
        )
        st.plotly_chart(fig1, use_container_width=True)

    except Exception as e:
        st.error(f"Sunburst Error: {e}")

    # =========================
    # TREEMAP
    # =========================
    st.subheader("📦 Treemap")

    try:
        fig2 = px.treemap(
            clean_df,
            path=["Industry_name_NZSIOC", "Variable_name"],
            values="Value",
            color="Value"
        )
        st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Treemap Error: {e}")

    st.subheader("📈 Value Growth Over Time")

    trend = df.groupby("Year")["Value"].sum().reset_index()

    fig = px.area(
        trend,
        x="Year",
        y="Value",
        color_discrete_sequence=["#00f5d4"]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔥 Industry Heatmap")

    heatmap_data = df.pivot_table(
        index="Industry_name_NZSIOC",
        columns="Year",
        values="Value",
        aggfunc="sum"
    ).fillna(0)

    fig = px.imshow(
        heatmap_data,
        aspect="auto",
        color_continuous_scale="Turbo"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🫧 Bubble Analysis")

    sample = df.groupby(["Industry_name_NZSIOC", "Year"], as_index=False)["Value"].sum()

    fig = px.scatter(
        sample,
        x="Year",
        y="Value",
        size="Value",
        color="Industry_name_NZSIOC",
        hover_name="Industry_name_NZSIOC"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🏆 Top 10 Industries")

    top = df.groupby("Industry_name_NZSIOC")["Value"].sum().nlargest(10).reset_index()

    fig = px.bar(
        top,
        x="Value",
        y="Industry_name_NZSIOC",
        orientation="h",
        color="Value",
        color_continuous_scale="Viridis"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🍩 Industry Share")

    share = df.groupby("Industry_name_NZSIOC")["Value"].sum().nlargest(5).reset_index()

    fig = px.pie(
        share,
        names="Industry_name_NZSIOC",
        values="Value",
        hole=0.5
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🎬 Animated Industry Growth")

    fig = px.bar(
        df,
        x="Industry_name_NZSIOC",
        y="Value",
        color="Industry_name_NZSIOC",
        animation_frame="Year"
    )

    st.plotly_chart(fig, use_container_width=True)

    import plotly.graph_objects as go

    st.subheader("💰 Value Contribution")

    top = df.groupby("Industry_name_NZSIOC")["Value"].sum().nlargest(5)

    fig = go.Figure(go.Waterfall(
        x=top.index,
        y=top.values,
        textposition="outside"
    ))

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <style>
    [data-testid="stPlotlyChart"] {
        background-color: #111;
        border-radius: 12px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    

# =========================
# DATA ASSISTANT
# =========================
elif selected == "Data Assistant":
    st.title("🤖 Data Assistant")

    question = st.text_input("Ask a question")

    if question:
        q = question.lower()

        if "total" in q:
            st.success(f"Total Value: {df['Value'].sum():,.0f}")

        elif "average" in q:
            st.success(f"Average Value: {df['Value'].mean():,.2f}")

        elif "top industry" in q:
            top = df.groupby("Industry_name_NZSIOC")["Value"].sum().idxmax()
            st.success(f"Top Industry: {top}")

        elif "trend" in q:
            trend = df.groupby("Year")["Value"].sum().reset_index()
            fig = px.line(trend, x="Year", y="Value")
            st.plotly_chart(fig)

        else:
            st.warning("Try: total, average, top industry, trend")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🚀 Enterprise Analytics Dashboard | Streamlit Project")