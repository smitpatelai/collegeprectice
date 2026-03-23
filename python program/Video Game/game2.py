import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(page_title="Video Game Dashboard", layout="wide")

# --------------------------------
# LOAD CSS
# --------------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------
# MATRIX BACKGROUND
# --------------------------------
def matrix_bg():
    matrix_js = """
    <canvas id="matrix"></canvas>
    <script>
    var canvas = document.getElementById("matrix");
    var ctx = canvas.getContext("2d");

    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;

    var letters = "01";
    letters = letters.split("");

    var font_size = 14;
    var columns = canvas.width/font_size;

    var drops = [];
    for(var x = 0; x < columns; x++)
        drops[x] = 1;

    function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = "#00ff9f";
        ctx.font = font_size + "px monospace";

        for(var i = 0; i < drops.length; i++) {
            var text = letters[Math.floor(Math.random()*letters.length)];
            ctx.fillText(text, i*font_size, drops[i]*font_size);

            if(drops[i]*font_size > canvas.height && Math.random() > 0.975)
                drops[i] = 0;

            drops[i]++;
        }
    }

    setInterval(draw, 35);
    </script>
    """
    st.components.v1.html(matrix_js, height=0)

# APPLY UI
load_css()
matrix_bg()

# --------------------------------
# LOAD DATA
# --------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("vgsales.csv")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df.dropna(inplace=True)
    return df

# --------------------------------
# DASHBOARD
# --------------------------------
def dashboard():
    st.markdown('<div class="typing">🎮 Video Game Sales Dashboard</div>', unsafe_allow_html=True)

    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filters")
    platform = st.sidebar.multiselect("Platform", df["Platform"].unique())
    genre = st.sidebar.multiselect("Genre", df["Genre"].unique())

    filtered_df = df.copy()

    if platform:
        filtered_df = filtered_df[filtered_df["Platform"].isin(platform)]

    if genre:
        filtered_df = filtered_df[filtered_df["Genre"].isin(genre)]

    # KPIs
    total_sales = filtered_df["Global_Sales"].sum()
    avg_sales = filtered_df["Global_Sales"].mean()
    top_game = filtered_df.loc[filtered_df["Global_Sales"].idxmax()]["Name"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"{total_sales:.2f}M")
    col2.metric("Average Sales", f"{avg_sales:.2f}M")
    col3.metric("Top Game", top_game)

    # -----------------------------
    # CHARTS
    # -----------------------------

    # Year-wise
    year_sales = filtered_df.groupby("Year")["Global_Sales"].sum().reset_index()
    fig1 = px.line(year_sales, x="Year", y="Global_Sales", title="Year-wise Sales")
    st.plotly_chart(fig1, use_container_width=True)

    # Genre
    genre_sales = filtered_df.groupby("Genre")["Global_Sales"].sum().reset_index()
    fig2 = px.bar(genre_sales, x="Genre", y="Global_Sales", title="Genre-wise Sales")
    st.plotly_chart(fig2, use_container_width=True)

    # Platform
    platform_sales = filtered_df.groupby("Platform")["Global_Sales"].sum().reset_index()
    fig3 = px.pie(platform_sales, names="Platform", values="Global_Sales", title="Platform Distribution")
    st.plotly_chart(fig3, use_container_width=True)

    # ============================================================
    # ADDED CHARTS (structure above is unchanged)
    # ============================================================

    st.markdown("---")
    st.subheader("📊 Extended Analytics")

    # ── ROW 1: Top 10 Publishers + Regional Sales ──
    col4, col5 = st.columns(2)

    with col4:
        # Top 10 Publishers by Global Sales
        pub_sales = (filtered_df.groupby("Publisher")["Global_Sales"]
                     .sum().reset_index()
                     .sort_values("Global_Sales", ascending=True)
                     .tail(10))
        fig4 = px.bar(pub_sales, x="Global_Sales", y="Publisher",
                      orientation="h",
                      title="🏢 Top 10 Publishers",
                      color="Global_Sales",
                      color_continuous_scale="Greens")
        fig4.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig4, use_container_width=True, key="pub_chart")

    with col5:
        # Regional Sales Donut
        region_data = pd.DataFrame({
            "Region": ["NA Sales", "EU Sales", "JP Sales", "Other"],
            "Sales": [
                filtered_df["NA_Sales"].sum(),
                filtered_df["EU_Sales"].sum(),
                filtered_df["JP_Sales"].sum(),
                filtered_df["Other_Sales"].sum()
            ]
        })
        fig5 = px.pie(region_data, names="Region", values="Sales",
                      title="🌍 Regional Sales Breakdown",
                      hole=0.45,
                      color_discrete_sequence=["#00ff9f", "#7c5cfc", "#ff6b6b", "#ffb830"])
        st.plotly_chart(fig5, use_container_width=True, key="region_chart")

    # ── ROW 2: Stacked Bar + Scatter ──
    col6, col7 = st.columns([3, 2])

    with col6:
        # Stacked Regional Sales by Year
        yr = filtered_df.groupby("Year")[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum().reset_index()
        fig6 = go.Figure()
        for col_name, color in [("NA_Sales", "#00ff9f"), ("EU_Sales", "#7c5cfc"),
                                ("JP_Sales", "#ff6b6b"), ("Other_Sales", "#ffb830")]:
            fig6.add_trace(go.Bar(
                name=col_name.replace("_Sales", ""),
                x=yr["Year"], y=yr[col_name],
                marker_color=color
            ))
        fig6.update_layout(barmode="stack", title="🗓 Regional Sales by Year")
        st.plotly_chart(fig6, use_container_width=True, key="stacked_chart")

    with col7:
        # NA vs EU Scatter by Genre
        scatter_df = (filtered_df.groupby("Genre")[["NA_Sales", "EU_Sales", "Global_Sales"]]
                      .sum().reset_index())
        fig7 = px.scatter(scatter_df, x="NA_Sales", y="EU_Sales",
                          size="Global_Sales", text="Genre",
                          color="Genre", size_max=50,
                          title="🔵 NA vs EU Sales by Genre")
        fig7.update_traces(textposition="top center")
        st.plotly_chart(fig7, use_container_width=True, key="scatter_chart")

    # ── ROW 3: Top 15 Games Table ──
    st.markdown("**🏅 Top 15 Best-Selling Games**")
    top15 = (filtered_df.sort_values("Global_Sales", ascending=False)
             .head(15)
             [["Name", "Platform", "Year", "Genre", "Publisher",
               "NA_Sales", "EU_Sales", "JP_Sales", "Global_Sales"]]
             .reset_index(drop=True))
    top15.index += 1
    top15.columns = ["Name", "Platform", "Year", "Genre", "Publisher",
                     "NA (M)", "EU (M)", "JP (M)", "Global (M)"]
    st.dataframe(
        top15.style
        .background_gradient(subset=["Global (M)"], cmap="Greens")
        .format({"NA (M)": "{:.2f}", "EU (M)": "{:.2f}",
                 "JP (M)": "{:.2f}", "Global (M)": "{:.2f}"}),
        use_container_width=True,
        height=480
    )

dashboard()