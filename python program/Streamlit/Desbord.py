import pandas as pd
import streamlit as st
import plotly.express as px
import time

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# --------------------------------
# MATRIX BACKGROUND + TERMINAL + UI
# --------------------------------
st.markdown("""
<style>

/* MATRIX BACKGROUND */
#matrix-bg {
    position: fixed;
    top: 0;
    left: 0;
    z-index: -1;
}

/* MAIN TRANSPARENT */
.main {
    background: transparent !important;
}

/* CONTAINER GLASS */
.block-container {
    background: rgba(0,0,0,0.75);
    border-radius: 15px;
    padding: 20px;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #05070d !important;
}

/* TERMINAL */
.terminal {
    background-color: #000;
    color: #00ffcc;
    font-family: monospace;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #00ffcc;
    box-shadow: 0 0 20px rgba(0,255,204,0.4);
    margin-bottom: 20px;
}

/* METRIC HACK STYLE */
.metric-hack {
    font-size: 28px;
    color: #00ffcc;
    text-shadow: 0 0 15px #00ffcc;
    font-family: monospace;
}

/* GLOW BOX */
.glow-box {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #00ffcc;
    box-shadow: 0 0 15px rgba(0,255,204,0.3);
    background: rgba(0,0,0,0.6);
    text-align: center;
}

</style>

<canvas id="matrix-bg"></canvas>

<script>
const canvas = document.getElementById('matrix-bg');
const ctx = canvas.getContext('2d');

canvas.height = window.innerHeight;
canvas.width = window.innerWidth;

const letters = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const matrix = letters.split("");

const fontSize = 14;
const columns = canvas.width / fontSize;
const drops = [];

for (let x = 0; x < columns; x++) drops[x] = 1;

function draw() {
    ctx.fillStyle = "rgba(0, 0, 0, 0.08)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#00ffcc";
    ctx.font = fontSize + "px monospace";

    for (let i = 0; i < drops.length; i++) {
        const text = matrix[Math.floor(Math.random() * matrix.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975)
            drops[i] = 0;

        drops[i]++;
    }
}

setInterval(draw, 35);
</script>
""", unsafe_allow_html=True)

# --------------------------------
# SIDEBAR NAVIGATION
# --------------------------------
st.sidebar.title("⚡ Navigation")
page = st.sidebar.radio("Go to", ["Home", "Dashboard", "About"])

# --------------------------------
# LOAD DATA (UNCHANGED)
# --------------------------------
def load_data():
    df = pd.read_csv("sales_dataset_streamlit_dashboard.csv.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()
print(df)

# --------------------------------
# HOME PAGE
# --------------------------------
if page == "Home":

    st.markdown("""
    <div class="terminal">
> Booting AI Sales System...
> Loading Modules...
> Connecting Database...
> Access Granted ✅
> Welcome Smit Patel 🚀
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;color:#00ffcc;'>⚡ AI COMMAND CENTER</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.markdown('<div class="glow-box">📊 Live Monitoring</div>', unsafe_allow_html=True)
    col2.markdown('<div class="glow-box">💰 Profit Engine</div>', unsafe_allow_html=True)
    col3.markdown('<div class="glow-box">🌍 Market Control</div>', unsafe_allow_html=True)

# --------------------------------
# DASHBOARD
# --------------------------------
elif page == "Dashboard":

    st.markdown("<h1 style='text-align:center;color:#00ffcc;'>⚡ SALES CONTROL PANEL</h1>", unsafe_allow_html=True)

    # sidebar filters
    st.sidebar.header("Filter Data")

    start_date = st.sidebar.date_input("Start Date", df["Date"].min())
    end_date = st.sidebar.date_input("End Date", df["Date"].max())

    region = st.sidebar.multiselect("Select Region", df["Region"].unique())
    product = st.sidebar.multiselect("Select Product", df["Product"].unique())
    top_n = st.sidebar.slider("Top N Products", 1, 10, 5)

    filtered_df = df[
        (df["Date"] >= pd.to_datetime(start_date)) &
        (df["Date"] <= pd.to_datetime(end_date)) &
        (df["Region"].isin(region) if region else True) &
        (df["Product"].isin(product) if product else True)
    ]

    # KPI VALUES
    total_sales = int(filtered_df["Sales"].sum())
    total_profit = int(filtered_df["Profit"].sum())
    avg_sales = int(filtered_df["Sales"].mean())

    # 🔥 HACKING NUMBER EFFECT
    def hack_number(target):
        placeholder = st.empty()
        for i in range(0, target, max(1, target // 50)):
            placeholder.markdown(f"<div class='metric-hack'>${i}</div>", unsafe_allow_html=True)
            time.sleep(0.01)
        placeholder.markdown(f"<div class='metric-hack'>${target}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Total Sales")
        hack_number(total_sales)

    with col2:
        st.markdown("### Total Profit")
        hack_number(total_profit)

    with col3:
        st.markdown("### Average Sales")
        hack_number(avg_sales)

    # charts (UNCHANGED)
    col4, col5 = st.columns(2)

    sales_region = filtered_df.groupby("Region")["Sales"].sum().reset_index()
    fig_bar = px.bar(sales_region, x="Region", y="Sales", color="Region")
    col4.plotly_chart(fig_bar, use_container_width=True)

    sales_product = filtered_df.groupby("Product")["Sales"].sum().reset_index()
    sales_product = sales_product.sort_values(by="Sales", ascending=False).head(top_n)
    fig_top = px.bar(sales_product, x="Product", y="Sales", color="Product")
    col5.plotly_chart(fig_top, use_container_width=True)

    fig_line = px.line(filtered_df, x="Date", y="Sales")
    st.plotly_chart(fig_line, use_container_width=True)

    profit_product = filtered_df.groupby("Product")["Profit"].sum().reset_index()
    fig_pie = px.pie(profit_product, values="Profit", names="Product", hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode('UTF-8')
    st.download_button("Download CSV", csv, "Filtered_Dashboard_data.csv", "text/csv")

# --------------------------------
# ABOUT PAGE
# --------------------------------
elif page == "About":

    st.markdown("""
    <div class="glow-box">
    ⚡ SYSTEM INFO <br><br>
    Developer: Smit Patel <br>
    Tech: Python | Streamlit | Plotly <br>
    Mode: Hacker UI Enabled 💻 <br>
    Status: ACTIVE ✅
    </div>
    """, unsafe_allow_html=True)