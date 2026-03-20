import streamlit as st
import pandas as pd
import plotly.express as px

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        load_css()

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
        matrix_bg()
# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("vgsales.csv")   # <-- your dataset file
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df.dropna(inplace=True)
    return df

# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Username or Password ❌")

# -----------------------------
# SIGNUP PAGE
# -----------------------------
def signup_page():
    st.title("📝 Signup")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Signup"):
        if new_user in st.session_state.users:
            st.warning("User already exists ⚠️")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("Account created! Please login ✅")

# -----------------------------
# DASHBOARD
# -----------------------------
def dashboard():
    # st.title("🎮 Video Game Sales Dashboard")
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

    # 1. Year-wise Sales
    year_sales = filtered_df.groupby("Year")["Global_Sales"].sum().reset_index()
    fig1 = px.line(year_sales, x="Year", y="Global_Sales", title="Year-wise Sales")
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Genre Sales
    genre_sales = filtered_df.groupby("Genre")["Global_Sales"].sum().reset_index()
    fig2 = px.bar(genre_sales, x="Genre", y="Global_Sales", title="Genre-wise Sales")
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Platform Sales
    platform_sales = filtered_df.groupby("Platform")["Global_Sales"].sum().reset_index()
    fig3 = px.pie(platform_sales, names="Platform", values="Global_Sales", title="Platform Distribution")
    st.plotly_chart(fig3, use_container_width=True)

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# -----------------------------
# MAIN APP FLOW
# -----------------------------
menu = ["Login", "Signup"]

if not st.session_state.logged_in:
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login_page()
    else:
        signup_page()
else:
    dashboard()

