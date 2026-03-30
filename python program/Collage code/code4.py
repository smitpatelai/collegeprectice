from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(page_title="AI Startup Dashboard", layout="wide", page_icon="🚀")

# --------------------------------
# GLOBAL CSS
# --------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
}

.stApp {
    background: #060910;
    color: #e0e8f0;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #0a0f1a !important;
    border-right: 1px solid #0d2137;
}

/* ---- METRICS ---- */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0d1b2a 60%, #0a2540);
    border: 1px solid #0d3355;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 0 18px #00b4ff18;
}

[data-testid="metric-container"] label {
    color: #4a8aaa !important;
    font-size: 11px !important;
    font-family: 'Rajdhani', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 2px;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #00d4ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

/* ---- HEADINGS ---- */
h1 {
    font-family: 'Orbitron', monospace !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    letter-spacing: -1px;
    text-shadow: 0 0 30px #00d4ff55;
}

h2, h3 {
    font-family: 'Orbitron', monospace !important;
    font-weight: 600 !important;
    color: #c0d8ee !important;
    letter-spacing: 0.5px;
}

/* ---- DIVIDER ---- */
hr { border-color: #0d2137 !important; }

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {
    border: 1px solid #0d2a40;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 20px #00b4ff10;
}

/* ---- SLIDERS ---- */
[data-testid="stSlider"] > div > div > div {
    background: #00d4ff !important;
}

/* ---- INPUTS ---- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #0d1b2a !important;
    border: 1px solid #0d3355 !important;
    color: #e0e8f0 !important;
    border-radius: 8px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.stSelectbox > div > div,
.stMultiSelect > div {
    background: #0d1b2a !important;
    border: 1px solid #0d3355 !important;
    color: #e0e8f0 !important;
    border-radius: 8px !important;
}

/* ---- BUTTONS ---- */
.stButton > button {
    background: linear-gradient(135deg, #004d80, #006faa) !important;
    color: #ffffff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border: 1px solid #00d4ff55 !important;
    border-radius: 8px !important;
    letter-spacing: 1px;
    transition: all 0.2s ease;
    box-shadow: 0 0 14px #00b4ff22;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #006faa, #00a0d4) !important;
    box-shadow: 0 0 22px #00d4ff44 !important;
}

/* ---- DOWNLOAD BUTTON ---- */
.stDownloadButton > button {
    background: linear-gradient(135deg, #004d30, #007050) !important;
    color: #00ffaa !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 11px !important;
    border: 1px solid #00ffaa44 !important;
    border-radius: 8px !important;
}

/* ---- ALERTS ---- */
.stSuccess { background: #001f14 !important; border-left: 4px solid #00ff88 !important; }
.stError   { background: #1f0006 !important; border-left: 4px solid #ff3355 !important; }
.stWarning { background: #1a1200 !important; border-left: 4px solid #ffaa00 !important; }
.stInfo    { background: #00101f !important; border-left: 4px solid #00d4ff !important; }

/* ---- LOGIN CARD ---- */
.login-card {
    background: linear-gradient(160deg, #0d1b2a, #060f1c);
    border: 1px solid #0d3355;
    border-radius: 20px;
    padding: 36px 32px 28px;
    box-shadow: 0 0 60px #00b4ff18, inset 0 1px 0 #1a4a6a44;
    margin-top: 20px;
}

.login-title {
    font-family: 'Orbitron', monospace;
    font-size: 22px;
    font-weight: 700;
    color: #00d4ff;
    text-align: center;
    margin-bottom: 24px;
    letter-spacing: 2px;
    text-shadow: 0 0 20px #00d4ff66;
}

/* ---- TAG PILLS ---- */
.tag-pill {
    display: inline-block;
    background: #001f35;
    color: #00d4ff;
    border: 1px solid #00d4ff33;
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 11px;
    font-weight: 600;
    margin-right: 6px;
    letter-spacing: 1px;
    font-family: 'Rajdhani', sans-serif;
}

/* ---- SECTION HEADER ---- */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #00d4ff;
    letter-spacing: 3px;
    text-transform: uppercase;
    border-bottom: 1px solid #0d3355;
    padding-bottom: 8px;
    margin-bottom: 16px;
}

/* ---- GLOW DIVIDER ---- */
.glow-div {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00d4ff55, transparent);
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# SESSION STATE
# --------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# --------------------------------
# FILES
# --------------------------------

if not os.path.exists("users.csv"):
    pd.DataFrame(columns=["username", "email", "password"]).to_csv("users.csv", index=False)

if not os.path.exists("user_activity.csv"):
    pd.DataFrame(columns=[
        "username", "login_date", "login_time", "logout_time",
        "funding", "team_experience", "market_size",
        "competition", "business_model", "prediction_probability"
    ]).to_csv("user_activity.csv", index=False)

# --------------------------------
# PLOTLY DARK THEME DEFAULTS
# --------------------------------

PLOT_CFG = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(6,9,16,0.6)"
)

# --------------------------------
# AUTH PAGES
# --------------------------------

def signup():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        # st.markdown('<div class="login-card">🚀 CREATE ACCOUNT</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">🚀 CREATE ACCOUNT</div>', unsafe_allow_html=True)
        username = st.text_input("Username", key="su_user")
        email    = st.text_input("Email", key="su_email")
        password = st.text_input("Password", type="password", key="su_pass")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Sign Up", use_container_width=True):
                users = pd.read_csv("users.csv")
                if username in users["username"].values:
                    st.error("Username already exists")
                else:
                    new_user = pd.DataFrame({"username": [username], "email": [email], "password": [password]})
                    pd.concat([users, new_user], ignore_index=True).to_csv("users.csv", index=False)
                    st.success("Account created!")
                    st.session_state.page = "login"
                    st.rerun()
        with c2:
            if st.button("← Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def login():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        # st.markdown('<div class="login-card">🔐 LOGIN</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">🔐 LOGIN</div>', unsafe_allow_html=True)
        username = st.text_input("Username", key="li_user")
        password = st.text_input("Password", type="password", key="li_pass")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Login", use_container_width=True):
                users = pd.read_csv("users.csv")
                user = users[(users["username"] == username) & (users["password"] == password)]
                if not user.empty:
                    st.session_state.logged_in   = True
                    st.session_state.username    = username
                    st.session_state.login_time  = datetime.now()
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        with c2:
            if st.button("Sign Up →", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------
# PRE-LOGIN SCREEN
# --------------------------------

if not st.session_state.logged_in:
    st.markdown("""
    <div style='text-align:center; padding: 60px 0 10px;'>
        <div style='font-family:Orbitron; font-size:38px; font-weight:900;
                    color:#ffffff; letter-spacing:-1px;
                    text-shadow: 0 0 40px #00d4ff66;'>
            🚀 AI STARTUP PREDICTOR
        </div>
        <div style='color:#3a6a8a; font-size:13px; letter-spacing:4px;
                    margin-top:8px; font-family:Rajdhani;'>
            MACHINE LEARNING · LOGISTIC REGRESSION · REAL-TIME ANALYSIS
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.page == "login":
        login()
    else:
        signup()
    st.stop()

# --------------------------------
# CREATE / LOAD DATASET
# --------------------------------

if not os.path.exists("dataset.csv"):
    np.random.seed(42)
    rows = 1200
    funding       = np.random.randint(50000, 5000000, rows)
    team_exp      = np.random.randint(1, 10, rows)
    market_size   = np.random.randint(1, 10, rows)
    competition   = np.random.randint(1, 10, rows)
    business_model= np.random.randint(1, 10, rows)
    score = (funding/1000000*0.3) + (team_exp*0.25) + (market_size*0.2) + (business_model*0.2) - (competition*0.15)
    success = (score > np.median(score)).astype(int)
    pd.DataFrame({
        "funding": funding, "team_experience": team_exp,
        "market_size": market_size, "competition": competition,
        "business_model": business_model, "success": success
    }).to_csv("dataset.csv", index=False)

data       = pd.read_csv("dataset.csv")
chart_data = data.copy()
X = data.drop("success", axis=1).values
y = data["success"].values.reshape(-1, 1)
X[:, 0] = X[:, 0] / 1000000
X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

if not os.path.exists("weights.npy"):
    weights = np.zeros((X.shape[1], 1))
    for _ in range(7000):
        predictions = sigmoid(np.dot(X, weights))
        weights -= 0.01 * np.dot(X.T, predictions - y) / len(y)
    np.save("weights.npy", weights)

weights    = np.load("weights.npy")
pred       = sigmoid(np.dot(X, weights))
pred_labels= (pred >= 0.5).astype(int)
accuracy   = (pred_labels == y).mean()

# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:24px 0 12px;'>
        <div style='font-family:Orbitron; font-size:20px; font-weight:900;
                    color:#00d4ff; letter-spacing:2px;'>🚀 STARTUP AI</div>
        <div style='font-size:10px; color:#2a5a7a; letter-spacing:3px; margin-top:4px;'>
            PREDICTION PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    selected = option_menu(
        menu_title="NAVIGATION",
        options=["Dashboard", "Predict", "Analytics", "My Profile","Data Assistant"],
        icons=["speedometer2", "cpu", "bar-chart-fill", "person-circle","robot"],
        menu_icon="grid-fill",
        default_index=0,
        styles={
            "container":        {"background-color": "#0a0f1a", "border": "none"},
            "menu-title":       {"color": "#2a5a7a", "font-size": "10px",
                                 "letter-spacing": "3px", "font-family": "Rajdhani"},
            "icon":             {"color": "#00d4ff", "font-size": "15px"},
            "nav-link":         {"color": "#6a9aba", "font-size": "13px",
                                 "font-family": "Rajdhani", "border-radius": "8px",
                                 "margin": "2px 0", "letter-spacing": "1px"},
            "nav-link-selected":{"background-color": "#001f35",
                                 "color": "#00d4ff", "font-weight": "600"},
        }
    )

    st.markdown("---")

    # Sidebar user card
    st.markdown(f"""
    <div style='background:#060d18; border:1px solid #0d2a40; border-radius:12px; padding:14px;'>
        <div style='color:#2a5a7a; font-size:10px; letter-spacing:3px; font-family:Rajdhani;'>LOGGED IN AS</div>
        <div style='color:#00d4ff; font-family:Orbitron; font-size:15px;
                    font-weight:700; margin-top:4px;'>
            {st.session_state.username.upper()}
        </div>
        <div style='margin-top:12px; display:flex; justify-content:space-between;'>
            <div>
                <div style='color:#2a5a7a; font-size:10px; letter-spacing:2px;'>ACCURACY</div>
                <div style='color:#00ff88; font-family:Orbitron; font-size:16px; font-weight:700;'>
                    {accuracy*100:.1f}%
                </div>
            </div>
            <div>
                <div style='color:#2a5a7a; font-size:10px; letter-spacing:2px;'>RECORDS</div>
                <div style='color:#ffffff; font-family:Orbitron; font-size:16px; font-weight:700;'>
                    {len(data):,}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⏻  Logout", use_container_width=True):
        activity = pd.read_csv("user_activity.csv")
        user_rows = activity[activity["username"] == st.session_state.username]
        if not user_rows.empty:
            activity.loc[user_rows.index[-1], "logout_time"] = datetime.now().strftime("%H:%M:%S")
        activity.to_csv("user_activity.csv", index=False)
        st.session_state.logged_in = False
        st.session_state.page      = "login"
        st.session_state.username  = ""
        st.rerun()

# ================================
# PAGE: DASHBOARD
# ================================

if selected == "Dashboard":

    st.markdown(f"""
    <div style='padding:10px 0 4px;'>
        <div style='font-family:Orbitron; font-size:28px; font-weight:900; color:#fff;
                    text-shadow:0 0 30px #00d4ff44; letter-spacing:-0.5px;'>
            Mission Control
        </div>
        <div style='color:#2a6a8a; font-size:12px; letter-spacing:3px; margin-top:4px;
                    font-family:Rajdhani;'>
            OVERVIEW · MODEL STATS · DATASET INSIGHTS
        </div>
    </div>
    <div class="glow-div"></div>
    """, unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🎯 Model Accuracy",     f"{accuracy*100:.2f}%")
    c2.metric("📦 Dataset Size",       f"{len(data):,} rows")
    c3.metric("✅ Success Rate",        f"{data['success'].mean()*100:.1f}%")
    c4.metric("📊 Features",           "5 Inputs")

    st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

    # Confusion Matrix
    col_cm, col_imp = st.columns(2)

    with col_cm:
        st.markdown('<div class="section-header">Confusion Matrix</div>', unsafe_allow_html=True)
        tp = int(np.sum((pred_labels==1)&(y==1)))
        tn = int(np.sum((pred_labels==0)&(y==0)))
        fp = int(np.sum((pred_labels==1)&(y==0)))
        fn = int(np.sum((pred_labels==0)&(y==1)))

        fig_cm = go.Figure(data=go.Heatmap(
            z=[[tn, fp], [fn, tp]],
            x=["Predicted Fail", "Predicted Success"],
            y=["Actual Fail",    "Actual Success"],
            colorscale="Blues",
            text=[[tn, fp], [fn, tp]],
            texttemplate="%{text}",
            textfont={"size": 18, "family": "Orbitron"},
            showscale=False
        ))
        fig_cm.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_imp:
        st.markdown('<div class="section-header">Feature Influence</div>', unsafe_allow_html=True)
        importance = pd.DataFrame({
            "Feature": ["Funding","Team Exp","Market Size","Competition","Biz Model"],
            "Weight":  weights[1:].flatten()
        }).sort_values("Weight")

        fig_imp = px.bar(
            importance, x="Weight", y="Feature", orientation="h",
            color="Weight", color_continuous_scale="Teal"
        )
        fig_imp.update_layout(height=280, showlegend=False,
                               margin=dict(l=0,r=0,t=10,b=0),
                               coloraxis_showscale=False, **PLOT_CFG)
        st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

    # Dataset insights
    st.markdown('<div class="section-header">Dataset Insights</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        fig_fund = px.histogram(
            chart_data, x="funding", nbins=30,
            title="Funding Distribution",
            color_discrete_sequence=["#00d4ff"]
        )
        fig_fund.update_layout(margin=dict(l=0,r=0,t=40,b=0), **PLOT_CFG)
        st.plotly_chart(fig_fund, use_container_width=True)

    with col_b:
        sr = chart_data.groupby("market_size")["success"].mean().reset_index()
        sr.columns = ["Market Size", "Success Rate"]
        fig_sr = px.line(
            sr, x="Market Size", y="Success Rate",
            title="Market Size vs Success Rate",
            color_discrete_sequence=["#00ff88"], markers=True
        )
        fig_sr.update_layout(margin=dict(l=0,r=0,t=40,b=0), **PLOT_CFG)
        st.plotly_chart(fig_sr, use_container_width=True)

    # Market trend
    st.markdown('<div class="section-header">Startup Market Trend</div>', unsafe_allow_html=True)

    chart_data["startup_index"] = (
        chart_data["funding"]/1000000 + chart_data["team_experience"] +
        chart_data["market_size"] + chart_data["business_model"] - chart_data["competition"]
    )
    chart_data["time"] = range(len(chart_data))

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=chart_data["time"], y=chart_data["startup_index"],
        mode="lines", fill="tozeroy",
        line=dict(color="#00d4ff", width=2),
        fillcolor="rgba(0,212,255,0.06)"
    ))
    fig_trend.update_layout(
        title="Startup Market Index Over Time",
        xaxis_title="Timeline", yaxis_title="Index Score",
        margin=dict(l=0,r=0,t=40,b=0), **PLOT_CFG
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # --------------------------------
    # 3D CHART
    # --------------------------------

    st.subheader("🌌 3D Startup Metrics Overview")

    fig3d = go.Figure(data=[go.Scatter3d(
        x=chart_data['funding'] / 1000000,
        y=chart_data['team_experience'],
        z=chart_data['market_size'],
        mode='markers',
        marker=dict(
            size=7,
            color=chart_data['success'],
            colorscale='Viridis',
            opacity=0.9

        )
    )])
    fig3d.update_layout(
        scene=dict(
            xaxis_title='Funding ($M)',
            yaxis_title='Team Experience',
            zaxis_title='Market Size',
            xaxis=dict(backgroundcolor="black"),
            yaxis=dict(backgroundcolor="black"),
            zaxis=dict(backgroundcolor="black")
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=0, t=0)
    )
    st.plotly_chart(fig3d, use_container_width=True)

    # --------------------------------
    # DATASET PREVIEW
    # --------------------------------

    st.subheader("📂 Dataset Preview")

    st.dataframe(chart_data.head(50))

    if st.button("Logout"):

        activity = pd.read_csv("user_activity.csv")

        logout_time = datetime.now().strftime("%H:%M:%S")

        # Find last record of this user
        user_rows = activity[activity["username"] == st.session_state.username]

        if not user_rows.empty:
            last_index = user_rows.index[-1]

            activity.loc[last_index, "logout_time"] = logout_time

        activity.to_csv("user_activity.csv", index=False)

# ================================
# PAGE: PREDICT
# ================================

elif selected == "Predict":

    st.markdown("""
    <div style='padding:10px 0 4px;'>
        <div style='font-family:Orbitron; font-size:28px; font-weight:900; color:#fff;
                    text-shadow:0 0 30px #00d4ff44;'>Prediction Engine</div>
        <div style='color:#2a6a8a; font-size:12px; letter-spacing:3px; margin-top:4px;
                    font-family:Rajdhani;'>ENTER STARTUP PARAMETERS · GET AI VERDICT</div>
    </div>
    <div class="glow-div"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Startup Parameters</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        funding = st.number_input("💰 Funding Amount ($)", min_value=0, step=10000)
    with col2:
        team_exp = st.slider("👥 Team Experience", 1, 10, 0)
    with col3:
        market_size = st.slider("🌍 Market Size", 1, 10, 0)

    col4, col5 = st.columns(2)
    with col4:
        competition = st.slider("⚔️ Competition Level", 1, 10, 0)
    with col5:
        business_model = st.slider("💡 Business Model Strength", 1, 10, 0)

    st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

    if st.button("⚡  LAUNCH PREDICTION", use_container_width=True):

        funding_norm = funding / 1000000
        features = np.array([1, funding_norm, team_exp, market_size, competition, business_model]).reshape(1, -1)
        prob = sigmoid(np.dot(features, weights)).item()

        # Save activity
        activity = pd.read_csv("user_activity.csv")
        new_activity = pd.DataFrame({
            "username": [st.session_state.username],
            "login_date":  [st.session_state.login_time.strftime("%Y-%m-%d")],
            "login_time":  [st.session_state.login_time.strftime("%H:%M:%S")],
            "logout_time": [""],
            "funding": [funding], "team_experience": [team_exp],
            "market_size": [market_size], "competition": [competition],
            "business_model": [business_model], "prediction_probability": [prob]
        })
        pd.concat([activity, new_activity], ignore_index=True).to_csv("user_activity.csv", index=False)

        st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

        # Result banner
        if prob >= 0.5:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#001f14,#002a1c);
                        border:1px solid #00ff88; border-radius:14px;
                        padding:24px; text-align:center; margin:12px 0;
                        box-shadow:0 0 30px #00ff8833;'>
                <div style='font-family:Orbitron; font-size:22px; color:#00ff88;
                            font-weight:700; letter-spacing:2px;'>
                    ✅ STARTUP WILL SUCCEED
                </div>
                <div style='color:#00cc66; font-size:14px; margin-top:8px;
                            font-family:Rajdhani; letter-spacing:2px;'>
                    SUCCESS PROBABILITY: {prob*100:.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#1f0006,#2a0008);
                        border:1px solid #ff3355; border-radius:14px;
                        padding:24px; text-align:center; margin:12px 0;
                        box-shadow:0 0 30px #ff335533;'>
                <div style='font-family:Orbitron; font-size:22px; color:#ff3355;
                            font-weight:700; letter-spacing:2px;'>
                    ⚠️ HIGH RISK OF FAILURE
                </div>
                <div style='color:#cc2244; font-size:14px; margin-top:8px;
                            font-family:Rajdhani; letter-spacing:2px;'>
                    SUCCESS PROBABILITY: {prob*100:.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Gauges side by side
        g1, g2 = st.columns(2)

        with g1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob * 100,
                title={'text': "Success Probability (%)", 'font': {'color': '#00d4ff', 'family': 'Orbitron', 'size': 13}},
                number={'font': {'color': '#ffffff', 'family': 'Orbitron'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#2a5a7a'},
                    'bar': {'color': "#00d4ff"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [
                        {'range': [0,  50], 'color': "#1f0008"},
                        {'range': [50, 75], 'color': "#1a1200"},
                        {'range': [75,100], 'color': "#001f10"}
                    ],
                    'threshold': {'line': {'color': "#00ff88", 'width': 3}, 'thickness': 0.75, 'value': prob*100}
                }
            ))
            fig_gauge.update_layout(height=260, margin=dict(l=20,r=20,t=40,b=20), **PLOT_CFG)
            st.plotly_chart(fig_gauge, use_container_width=True)

        with g2:
            confidence = abs(prob - 0.5) * 2 * 100
            fig_conf = go.Figure(go.Indicator(
                mode="gauge+number",
                value=confidence,
                title={'text': "AI Confidence (%)", 'font': {'color': '#00d4ff', 'family': 'Orbitron', 'size': 13}},
                number={'font': {'color': '#ffffff', 'family': 'Orbitron'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#2a5a7a'},
                    'bar': {'color': "#00ff88"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'steps': [
                        {'range': [0,  40], 'color': "#1f0008"},
                        {'range': [40, 70], 'color': "#1a1200"},
                        {'range': [70,100], 'color': "#001f10"}
                    ]
                }
            ))
            fig_conf.update_layout(height=260, margin=dict(l=20,r=20,t=40,b=20), **PLOT_CFG)
            st.plotly_chart(fig_conf, use_container_width=True)

        if confidence > 70:
            st.success("🧠 AI Model is Highly Confident in this prediction")
        elif confidence > 40:
            st.warning("🧠 AI Model has Moderate Confidence")
        else:
            st.error("🧠 AI Model Confidence is Low — gather more data")

        # Investor recommendation
        st.markdown('<div class="section-header">Investor Recommendation</div>', unsafe_allow_html=True)
        if prob > 0.75:
            st.success("💰 Strong investment opportunity — high potential")
        elif prob > 0.55:
            st.warning("⚖️ Moderate potential — evaluate risk carefully")
        else:
            st.error("🚫 High risk — investment not recommended at this stage")

# ================================
# PAGE: ANALYTICS
# ================================

elif selected == "Analytics":

    st.markdown("""
    <div style='padding:10px 0 4px;'>
        <div style='font-family:Orbitron; font-size:28px; font-weight:900; color:#fff;
                    text-shadow:0 0 30px #00d4ff44;'>Analytics Lab</div>
        <div style='color:#2a6a8a; font-size:12px; letter-spacing:3px; margin-top:4px;
                    font-family:Rajdhani;'>DATA DISTRIBUTION · CORRELATIONS · SUCCESS PATTERNS</div>
    </div>
    <div class="glow-div"></div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Startups", f"{len(data):,}")
    c2.metric("Avg Funding",    f"${data['funding'].mean()/1e6:.2f}M")
    c3.metric("Avg Team Exp",   f"{data['team_experience'].mean():.1f}/10")
    c4.metric("Success Rate",   f"{data['success'].mean()*100:.1f}%")

    st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

    # Row 1
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header">Success by Team Experience</div>', unsafe_allow_html=True)
        team_success = data.groupby("team_experience")["success"].mean().reset_index()
        fig1 = px.bar(team_success, x="team_experience", y="success",
                      color="success", color_continuous_scale="Teal",
                      labels={"team_experience": "Team Experience", "success": "Success Rate"})
        fig1.update_layout(showlegend=False, coloraxis_showscale=False,
                           margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Competition vs Success</div>', unsafe_allow_html=True)
        comp_success = data.groupby("competition")["success"].mean().reset_index()
        fig2 = px.line(comp_success, x="competition", y="success",
                       markers=True, color_discrete_sequence=["#ff5577"],
                       labels={"competition": "Competition Level", "success": "Success Rate"})
        fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown('<div class="section-header">Funding Distribution</div>', unsafe_allow_html=True)
        fig3 = px.histogram(data, x="funding", nbins=30,
                            color_discrete_sequence=["#00d4ff"])
        fig3.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-header">Business Model vs Success</div>', unsafe_allow_html=True)
        bm_success = data.groupby("business_model")["success"].mean().reset_index()
        fig4 = px.area(bm_success, x="business_model", y="success",
                       color_discrete_sequence=["#aa00ff"],
                       labels={"business_model": "Business Model Score", "success": "Success Rate"})
        fig4.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig4, use_container_width=True)

    # Correlation heatmap
    st.markdown('<div class="section-header">Feature Correlation Matrix</div>', unsafe_allow_html=True)
    corr = data.corr()
    fig_corr = px.imshow(
        corr, text_auto=True, color_continuous_scale="RdBu_r",
        title="Feature Correlation Heatmap"
    )
    fig_corr.update_layout(margin=dict(l=0,r=0,t=40,b=0), **PLOT_CFG)
    st.plotly_chart(fig_corr, use_container_width=True)

    # Success donut
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown('<div class="section-header">Overall Success Split</div>', unsafe_allow_html=True)
        success_counts = data["success"].value_counts().reset_index()
        success_counts.columns = ["Outcome", "Count"]
        success_counts["Outcome"] = success_counts["Outcome"].map({1: "Success", 0: "Failure"})
        fig5 = px.pie(success_counts, values="Count", names="Outcome",
                      hole=0.55, color_discrete_sequence=["#00ff88", "#ff3355"])
        fig5.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig5, use_container_width=True)

    with col_f:
        st.markdown('<div class="section-header">Market Size vs Avg Funding</div>', unsafe_allow_html=True)
        ms_fund = data.groupby("market_size")["funding"].mean().reset_index()
        fig6 = px.scatter(ms_fund, x="market_size", y="funding",
                          size="funding", color="funding",
                          color_continuous_scale="Plasma",
                          labels={"market_size": "Market Size", "funding": "Avg Funding ($)"})
        fig6.update_layout(coloraxis_showscale=False,
                           margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig6, use_container_width=True)

# ================================
# PAGE: MY PROFILE
# ================================

elif selected == "My Profile":

    user_activity = pd.read_csv("user_activity.csv")
    user_data = user_activity[user_activity["username"] == st.session_state.username].copy()

    st.markdown(f"""
    <div style='padding:10px 0 4px;'>
        <div style='font-family:Orbitron; font-size:28px; font-weight:900; color:#fff;
                    text-shadow:0 0 30px #00d4ff44;'>
            {st.session_state.username.upper()}
        </div>
        <div style='color:#2a6a8a; font-size:12px; letter-spacing:3px; margin-top:4px;
                    font-family:Rajdhani;'>FOUNDER PROFILE · HISTORY · ACHIEVEMENTS</div>
    </div>
    <div class="glow-div"></div>
    """, unsafe_allow_html=True)

    if not user_data.empty:
        avg_prob = user_data["prediction_probability"].mean()
        best_prob = user_data["prediction_probability"].max()
        total_preds = len(user_data)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Predictions",  total_preds)
        c2.metric("Avg Success Rate",   f"{avg_prob*100:.1f}%")
        c3.metric("Best Prediction",    f"{best_prob*100:.1f}%")
        c4.metric("Successes",          int((user_data["prediction_probability"] >= 0.5).sum()))

        st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

        # Donut + Trend
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="section-header">Your Success vs Failure</div>', unsafe_allow_html=True)
            s_count = (user_data["prediction_probability"] >= 0.5).sum()
            f_count = (user_data["prediction_probability"] <  0.5).sum()
            fig_donut = px.pie(
                names=["Success", "Failure"], values=[s_count, f_count],
                hole=0.55, color_discrete_sequence=["#00ff88", "#ff3355"]
            )
            fig_donut.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-header">Prediction Growth Trend</div>', unsafe_allow_html=True)
            user_data_reset = user_data.reset_index(drop=True)
            user_data_reset["Run"] = range(1, len(user_data_reset) + 1)
            fig_trend = px.line(
                user_data_reset, x="Run", y="prediction_probability",
                markers=True, color_discrete_sequence=["#00d4ff"]
            )
            fig_trend.add_hline(y=0.5, line_dash="dot", line_color="#ff5577",
                                annotation_text="Success Threshold")
            fig_trend.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
            st.plotly_chart(fig_trend, use_container_width=True)

        # AI Suggestions
        st.markdown('<div class="section-header">AI Suggestions</div>', unsafe_allow_html=True)

        avg_funding = user_data["funding"].mean()
        avg_team    = user_data["team_experience"].mean()

        if avg_funding < 1000000:
            st.warning("💡 Try increasing funding — it has 30% weight in the model")
        if avg_team < 5:
            st.warning("💡 Improve team experience — it has the highest weight (25%)")
        if user_data["competition"].mean() > 6:
            st.error("⚠️ High competition detected — target a niche market")
        st.success("✅ A strong business model consistently improves success odds")

        # Achievement
        st.markdown('<div class="section-header">Achievement Badge</div>', unsafe_allow_html=True)

        if avg_prob > 0.7:
            badge, badge_color, label = "🥇", "#ffd700", "PRO FOUNDER"
        elif avg_prob > 0.5:
            badge, badge_color, label = "🥈", "#c0c0c0", "GROWING ENTREPRENEUR"
        else:
            badge, badge_color, label = "🥉", "#cd7f32", "BEGINNER LEVEL"

        st.markdown(f"""
        <div style='background:#0d1b2a; border:1px solid {badge_color}44;
                    border-radius:14px; padding:24px; text-align:center;
                    box-shadow: 0 0 24px {badge_color}22;'>
            <div style='font-size:48px;'>{badge}</div>
            <div style='font-family:Orbitron; font-size:18px; color:{badge_color};
                        font-weight:700; letter-spacing:3px; margin-top:8px;'>
                {label}
            </div>
            <div style='color:#3a6a8a; font-size:12px; margin-top:6px;
                        font-family:Rajdhani; letter-spacing:2px;'>
                AVERAGE SUCCESS RATE: {avg_prob*100:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

        # History table
        st.markdown('<div class="section-header">Prediction History</div>', unsafe_allow_html=True)
        st.dataframe(user_data.tail(10), use_container_width=True)

        # Download
        st.download_button(
            "📥 Download My Full Report",
            user_data.to_csv(index=False),
            "my_startup_report.csv"
        )

    else:
        st.info("No predictions yet — head to the Predict page to get started!")

    # ================================
    # PAGE: DATA ASSISTANT
    # ================================

elif selected == "Data Assistant":

    st.markdown("""
            <div style='padding:10px 0 4px;'>
                <div style='font-family:Orbitron; font-size:28px; font-weight:900; color:#fff;
                            text-shadow:0 0 30px #00d4ff44;'>
                    AI Data Assistant 🤖
                </div>
                <div style='color:#2a6a8a; font-size:12px; letter-spacing:3px; margin-top:4px;
                            font-family:Rajdhani;'>
                    ASK QUESTIONS · GET INSTANT INSIGHTS
                </div>
            </div>
            <div class="glow-div"></div>
            """, unsafe_allow_html=True)

    st.write("Ask questions about startup dataset")

    user_question = st.text_input("💬 Ask your question")

    if user_question:
        q = user_question.lower()

        # TOTAL STARTUPS
        if "total" in q or "count" in q:
            total = len(data)
            st.success(f"Total Startups: {total}")

            fig = px.histogram(
                data, x="success",
                title="Success vs Failure Distribution",
                color="success"
            )
            st.plotly_chart(fig, use_container_width=True)

        # SUCCESS RATE
        elif "success rate" in q or "success" in q:
            rate = data["success"].mean() * 100
            st.success(f"Success Rate: {rate:.2f}%")

            fig = px.pie(
                names=["Success", "Failure"],
                values=[rate, 100 - rate],
                hole=0.5
            )
            st.plotly_chart(fig, use_container_width=True)

        # FUNDING
        elif "funding" in q:
            avg_funding = data["funding"].mean()
            st.success(f"Average Funding: ${avg_funding:,.0f}")

            fig = px.histogram(
                data, x="funding",
                title="Funding Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

        # TEAM EXPERIENCE
        elif "team" in q:
            avg_team = data["team_experience"].mean()
            st.success(f"Average Team Experience: {avg_team:.1f}/10")

            fig = px.bar(
                data.groupby("team_experience")["success"].mean().reset_index(),
                x="team_experience",
                y="success",
                title="Team Experience vs Success Rate"
            )
            st.plotly_chart(fig, use_container_width=True)

        # MARKET SIZE
        elif "market" in q:
            fig = px.line(
                data.groupby("market_size")["success"].mean().reset_index(),
                x="market_size",
                y="success",
                title="Market Size vs Success"
            )
            st.plotly_chart(fig, use_container_width=True)

        # DEFAULT
        else:
            st.warning("Try asking: total startups, success rate, funding, team, market")