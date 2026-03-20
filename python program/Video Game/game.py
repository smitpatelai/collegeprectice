import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="🎮 VG Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    <canvas id="matrix" style="position:fixed;top:0;left:0;z-index:-1;opacity:0.18;pointer-events:none;"></canvas>
    <script>
    var canvas = document.getElementById("matrix");
    var ctx = canvas.getContext("2d");
    canvas.height = window.innerHeight;
    canvas.width  = window.innerWidth;
    window.addEventListener('resize', function(){
        canvas.height = window.innerHeight;
        canvas.width  = window.innerWidth;
    });
    var letters = "01アイウエオカキクケコ";
    letters = letters.split("");
    var font_size = 13;
    var columns = Math.floor(canvas.width / font_size);
    var drops = Array(columns).fill(1);
    function draw() {
        ctx.fillStyle = "rgba(5,5,16,0.07)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#00ff9f";
        ctx.font = font_size + "px monospace";
        for (var i = 0; i < drops.length; i++) {
            var text = letters[Math.floor(Math.random() * letters.length)];
            ctx.fillText(text, i * font_size, drops[i] * font_size);
            if (drops[i] * font_size > canvas.height && Math.random() > 0.975)
                drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 38);
    </script>
    """
    st.components.v1.html(matrix_js, height=0)

# --------------------------------
# PLOTLY THEME
# --------------------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Orbitron, monospace", color="#c8ffd4", size=11),
    title_font=dict(family="Orbitron, monospace", color="#00ff9f", size=14),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c8ffd4")),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="rgba(0,255,159,0.08)", color="#6bffb8", tickfont=dict(size=10)),
    yaxis=dict(gridcolor="rgba(0,255,159,0.08)", color="#6bffb8", tickfont=dict(size=10)),
)

COLORS = ["#00ff9f", "#7c5cfc", "#ff6b6b", "#ffb830", "#00c8ff",
          "#ff4dff", "#b8ff47", "#ff8c42", "#4dffdb", "#ff4d94"]

# --------------------------------
# LOAD DATA
# --------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("vgsales.csv")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df.dropna(subset=["Year", "Global_Sales", "Name", "Platform", "Genre", "Publisher"], inplace=True)
    df["Year"] = df["Year"].astype(int)
    return df

# --------------------------------
# DASHBOARD
# --------------------------------
def dashboard():
    load_css()
    matrix_bg()

    # Title
    st.markdown("""
        <div class="title-wrap">
            <div class="title-glow">🎮 Video Game Sales Dashboard</div>
            <div class="title-sub">Global Analytics · Dataset: vgsalesGlobale</div>
        </div>
    """, unsafe_allow_html=True)

    df = load_data()

    # ── SIDEBAR ──────────────────────────────────
    st.sidebar.markdown('<div class="sidebar-title">⚙ FILTERS</div>', unsafe_allow_html=True)

    platforms  = sorted(df["Platform"].unique().tolist())
    genres     = sorted(df["Genre"].unique().tolist())
    publishers = sorted(df["Publisher"].unique().tolist())
    year_min, year_max = int(df["Year"].min()), int(df["Year"].max())

    sel_platform  = st.sidebar.multiselect("🕹 Platform",  platforms,  placeholder="All platforms")
    sel_genre     = st.sidebar.multiselect("🎯 Genre",     genres,     placeholder="All genres")
    sel_publisher = st.sidebar.multiselect("🏢 Publisher", publishers, placeholder="All publishers")
    year_range    = st.sidebar.slider("📅 Year range", year_min, year_max, (2000, year_max))

    st.sidebar.markdown("---")
    st.sidebar.markdown(f'<div class="sidebar-stat">📦 Total records: <b>{len(df):,}</b></div>', unsafe_allow_html=True)

    # ── FILTER ───────────────────────────────────
    fdf = df.copy()
    if sel_platform:  fdf = fdf[fdf["Platform"].isin(sel_platform)]
    if sel_genre:     fdf = fdf[fdf["Genre"].isin(sel_genre)]
    if sel_publisher: fdf = fdf[fdf["Publisher"].isin(sel_publisher)]
    fdf = fdf[(fdf["Year"] >= year_range[0]) & (fdf["Year"] <= year_range[1])]

    if fdf.empty:
        st.warning("⚠️ No data matches your filters. Please adjust them.")
        return

    # ── KPIs ─────────────────────────────────────
    total_sales  = fdf["Global_Sales"].sum()
    avg_sales    = fdf["Global_Sales"].mean()
    top_game     = fdf.loc[fdf["Global_Sales"].idxmax(), "Name"]
    top_game_sal = fdf["Global_Sales"].max()
    top_platform = fdf.groupby("Platform")["Global_Sales"].sum().idxmax()
    top_genre    = fdf.groupby("Genre")["Global_Sales"].sum().idxmax()
    na_pct       = (fdf["NA_Sales"].sum() / fdf["Global_Sales"].sum() * 100)
    total_titles = len(fdf)

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f"""<div class="kpi-card" style="--kc:#00ff9f">
        <div class="kpi-icon">💰</div>
        <div class="kpi-label">Total Global Sales</div>
        <div class="kpi-value">{total_sales:,.1f}M</div>
        <div class="kpi-sub">{total_titles:,} titles</div>
    </div>""", unsafe_allow_html=True)

    k2.markdown(f"""<div class="kpi-card" style="--kc:#7c5cfc">
        <div class="kpi-icon">🏆</div>
        <div class="kpi-label">Top-Selling Game</div>
        <div class="kpi-value kpi-value--sm">{top_game}</div>
        <div class="kpi-sub">{top_game_sal:.2f}M units</div>
    </div>""", unsafe_allow_html=True)

    k3.markdown(f"""<div class="kpi-card" style="--kc:#ff6b6b">
        <div class="kpi-icon">📊</div>
        <div class="kpi-label">Average Sales/Game</div>
        <div class="kpi-value">{avg_sales:.3f}M</div>
        <div class="kpi-sub">Best genre: {top_genre}</div>
    </div>""", unsafe_allow_html=True)

    k4.markdown(f"""<div class="kpi-card" style="--kc:#ffb830">
        <div class="kpi-icon">🌎</div>
        <div class="kpi-label">Top Platform</div>
        <div class="kpi-value kpi-value--sm">{top_platform}</div>
        <div class="kpi-sub">NA share: {na_pct:.1f}%</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── ROW 1: Line + Pie ─────────────────────────
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown('<div class="chart-label">📈 Year-wise Global Sales Trend</div>', unsafe_allow_html=True)
        year_sales = fdf.groupby("Year")["Global_Sales"].sum().reset_index()
        fig1 = px.line(year_sales, x="Year", y="Global_Sales",
                       markers=True, color_discrete_sequence=["#00ff9f"])
        fig1.update_traces(line=dict(width=2.5), marker=dict(size=6,
                           line=dict(color="#00ff9f", width=1.5)))
        fig1.update_layout(**PLOTLY_LAYOUT, height=300,
                           yaxis_title="Sales (M)", xaxis_title="Year")
        st.plotly_chart(fig1, use_container_width=True, key="year_chart")

    with c2:
        st.markdown('<div class="chart-label">🌍 Regional Distribution</div>', unsafe_allow_html=True)
        region_data = pd.DataFrame({
            "Region": ["NA Sales", "EU Sales", "JP Sales", "Other"],
            "Sales":  [fdf["NA_Sales"].sum(), fdf["EU_Sales"].sum(),
                       fdf["JP_Sales"].sum(), fdf["Other_Sales"].sum()]
        })
        fig2 = px.pie(region_data, names="Region", values="Sales",
                      color_discrete_sequence=COLORS, hole=0.45)
        fig2.update_layout(**{**PLOTLY_LAYOUT, "xaxis": {}, "yaxis": {}}, height=300)
        fig2.update_traces(textfont_color="#0a0d14",
                           marker=dict(line=dict(color="#0a0d14", width=2)))
        st.plotly_chart(fig2, use_container_width=True, key="region_chart")

    # ── ROW 2: Bar + Horizontal bar ───────────────
    c3, c4 = st.columns(2)

    with c3:
        st.markdown('<div class="chart-label">🎯 Genre-wise Performance</div>', unsafe_allow_html=True)
        genre_sales = (fdf.groupby("Genre")["Global_Sales"]
                          .sum().reset_index()
                          .sort_values("Global_Sales", ascending=False))
        fig3 = px.bar(genre_sales, x="Genre", y="Global_Sales",
                      color="Global_Sales",
                      color_continuous_scale=["#0a2e1a", "#00ff9f"],
                      text_auto=".1f")
        fig3.update_layout(**PLOTLY_LAYOUT, height=320,
                           coloraxis_showscale=False,
                           yaxis_title="Sales (M)", xaxis_title="")
        fig3.update_traces(textfont_color="#000", textposition="outside",
                           marker_line_color="rgba(0,0,0,0)")
        st.plotly_chart(fig3, use_container_width=True, key="genre_chart")

    with c4:
        st.markdown('<div class="chart-label">🏢 Top 10 Publishers</div>', unsafe_allow_html=True)
        pub_sales = (fdf.groupby("Publisher")["Global_Sales"]
                       .sum().reset_index()
                       .sort_values("Global_Sales", ascending=True)
                       .tail(10))
        fig4 = px.bar(pub_sales, x="Global_Sales", y="Publisher",
                      orientation="h",
                      color="Global_Sales",
                      color_continuous_scale=["#1a0a2e", "#7c5cfc"],
                      text_auto=".1f")
        fig4.update_layout(**PLOTLY_LAYOUT, height=320,
                           coloraxis_showscale=False,
                           xaxis_title="Sales (M)", yaxis_title="")
        fig4.update_traces(textfont_color="#fff", textposition="inside",
                           marker_line_color="rgba(0,0,0,0)")
        st.plotly_chart(fig4, use_container_width=True, key="publisher_chart")

    # ── ROW 3: Stacked bar + Scatter ──────────────
    c5, c6 = st.columns([3, 2])

    with c5:
        st.markdown('<div class="chart-label">🗓 Regional Sales by Year (stacked)</div>', unsafe_allow_html=True)
        yr = fdf.groupby("Year")[["NA_Sales","EU_Sales","JP_Sales","Other_Sales"]].sum().reset_index()
        fig5 = go.Figure()
        pairs = [("NA_Sales","#00ff9f"),("EU_Sales","#7c5cfc"),
                 ("JP_Sales","#ff6b6b"),("Other_Sales","#ffb830")]
        for col, color in pairs:
            fig5.add_trace(go.Bar(name=col.replace("_Sales",""),
                                  x=yr["Year"], y=yr[col],
                                  marker_color=color, marker_line_width=0))
        fig5.update_layout(**PLOTLY_LAYOUT, barmode="stack", height=300,
                           yaxis_title="Sales (M)")
        st.plotly_chart(fig5, use_container_width=True, key="stacked_chart")

    with c6:
        st.markdown('<div class="chart-label">🔵 NA vs EU Sales by Genre</div>', unsafe_allow_html=True)
        scatter_df = (fdf.groupby("Genre")[["NA_Sales","EU_Sales","Global_Sales"]]
                        .sum().reset_index())
        fig6 = px.scatter(scatter_df, x="NA_Sales", y="EU_Sales",
                          size="Global_Sales", text="Genre",
                          color="Genre", color_discrete_sequence=COLORS,
                          size_max=50)
        fig6.update_traces(textposition="top center",
                           textfont=dict(size=9, color="#c8ffd4"))
        fig6.update_layout(**PLOTLY_LAYOUT, height=300,
                           showlegend=False,
                           xaxis_title="NA Sales (M)",
                           yaxis_title="EU Sales (M)")
        st.plotly_chart(fig6, use_container_width=True, key="scatter_chart")

    # ── TABLE ────────────────────────────────────
    st.markdown('<div class="chart-label">🏅 Top 15 Best-Selling Games</div>', unsafe_allow_html=True)
    top15 = (fdf.sort_values("Global_Sales", ascending=False)
               .head(15)
               [["Name","Platform","Year","Genre","Publisher",
                 "NA_Sales","EU_Sales","JP_Sales","Global_Sales"]]
               .reset_index(drop=True))
    top15.index += 1
    top15.columns = ["Name","Platform","Year","Genre","Publisher",
                     "NA (M)","EU (M)","JP (M)","Global (M)"]
    st.dataframe(
        top15.style
             .background_gradient(subset=["Global (M)"], cmap="Greens")
             .format({"NA (M)": "{:.2f}", "EU (M)": "{:.2f}",
                      "JP (M)": "{:.2f}", "Global (M)": "{:.2f}"}),
        use_container_width=True, height=480
    )

    st.markdown('<div class="footer">🎮 VG Sales Dashboard · Built with Streamlit + Plotly · vgsalesGlobale dataset</div>',
                unsafe_allow_html=True)

# RUN
dashboard()