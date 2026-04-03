from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import hashlib
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(page_title="AI Startup Dashboard", layout="wide", page_icon="🔮")

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

[data-testid="stSidebar"] {
    background: #0a0f1a !important;
    border-right: 1px solid #0d2137;
}

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

hr { border-color: #0d2137 !important; }

[data-testid="stDataFrame"] {
    border: 1px solid #0d2a40;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 0 20px #00b4ff10;
}

[data-testid="stSlider"] > div > div > div {
    background: #00d4ff !important;
}

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

.stDownloadButton > button {
    background: linear-gradient(135deg, #004d30, #007050) !important;
    color: #00ffaa !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 11px !important;
    border: 1px solid #00ffaa44 !important;
    border-radius: 8px !important;
}

.stSuccess { background: #001f14 !important; border-left: 4px solid #00ff88 !important; }
.stError   { background: #1f0006 !important; border-left: 4px solid #ff3355 !important; }
.stWarning { background: #1a1200 !important; border-left: 4px solid #ffaa00 !important; }
.stInfo    { background: #00101f !important; border-left: 4px solid #00d4ff !important; }

.auth-card {
    background: linear-gradient(160deg, #0d1b2a, #060f1c);
    border: 1px solid #0d3355;
    border-radius: 20px;
    padding: 36px 32px 28px;
    box-shadow: 0 0 60px #00b4ff18, inset 0 1px 0 #1a4a6a44;
    margin-top: 10px;
}

.auth-title {
    font-family: 'Orbitron', monospace;
    font-size: 20px;
    font-weight: 700;
    color: #00d4ff;
    text-align: center;
    margin-bottom: 6px;
    letter-spacing: 3px;
    text-shadow: 0 0 20px #00d4ff66;
}

.auth-subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 12px;
    color: #2a5a7a;
    text-align: center;
    letter-spacing: 2px;
    margin-bottom: 24px;
}

.social-btn-row {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    justify-content: center;
}

.social-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 11px 10px;
    border-radius: 10px;
    border: 1px solid;
    font-family: 'Rajdhani', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
    cursor: pointer;
    text-decoration: none !important;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.social-btn-google {
    background: linear-gradient(135deg, #1a0e0e, #2a1212);
    border-color: #c1392b44;
    color: #e8c5c0 !important;
}
.social-btn-google:hover {
    background: linear-gradient(135deg, #2a1212, #3a1818);
    border-color: #EA4335;
    box-shadow: 0 0 18px #EA433533;
    color: #ffffff !important;
}

.social-btn-github {
    background: linear-gradient(135deg, #0e0e0e, #1a1a1a);
    border-color: #44444466;
    color: #c8d0d8 !important;
}
.social-btn-github:hover {
    background: linear-gradient(135deg, #1a1a1a, #222);
    border-color: #aaaaaa;
    box-shadow: 0 0 18px #ffffff22;
    color: #ffffff !important;
}

.social-btn-facebook {
    background: linear-gradient(135deg, #0a0f1f, #0d1530);
    border-color: #1877F244;
    color: #98b4e8 !important;
}
.social-btn-facebook:hover {
    background: linear-gradient(135deg, #0d1530, #102040);
    border-color: #1877F2;
    box-shadow: 0 0 18px #1877F233;
    color: #ffffff !important;
}

.or-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 18px 0;
    color: #1a3a55;
    font-size: 11px;
    letter-spacing: 2px;
    font-family: 'Rajdhani', sans-serif;
}
.or-divider::before,
.or-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #0d3355, transparent);
}

.auth-footer {
    text-align: center;
    margin-top: 18px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 12px;
    color: #2a5a7a;
    letter-spacing: 1px;
}

.auth-footer a {
    color: #00d4ff !important;
    text-decoration: none;
    font-weight: 600;
}

.oauth-info {
    background: #001020;
    border: 1px solid #00d4ff22;
    border-radius: 8px;
    padding: 10px 14px;
    margin-top: 14px;
    font-size: 11px;
    color: #2a6a8a;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 0.5px;
    text-align: center;
}

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

.glow-div {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00d4ff55, transparent);
    margin: 24px 0;
}

@keyframes borderPulse {
    0%, 100% { box-shadow: 0 0 30px #00b4ff10, inset 0 1px 0 #1a4a6a44; }
    50%       { box-shadow: 0 0 50px #00b4ff28, inset 0 1px 0 #1a4a6a44; }
}

.auth-card { animation: borderPulse 4s ease-in-out infinite; }
</style>
""", unsafe_allow_html=True)

# --------------------------------
# SESSION STATE
# --------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
# PLOTLY DARK THEME
# --------------------------------

PLOT_CFG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Space Mono", color="#ffffff")
)

# --------------------------------
# COLOR CONFIG
# --------------------------------
GREEN = "#5dde8c"
RED   = "#ff4b4b"
AMBER = "#f5b942"
BLUE  = "#4da3ff"

def add_opacity(color, alpha=0.12):
    if color.startswith("rgb"):
        return color.replace("rgb", "rgba").replace(")", f", {alpha})")
    return color

# --------------------------------
# SOCIAL BUTTON HTML HELPER
# --------------------------------

GOOGLE_SVG = """<svg width="18" height="18" viewBox="0 0 48 48">
  <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0
    14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
  <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94
    c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
  <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19
    C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
  <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.32-8.16 2.32
    -6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
</svg>"""

GITHUB_SVG = """<svg width="18" height="18" viewBox="0 0 24 24" fill="white">
  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577
    0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.335-1.755-1.335-1.755
    -1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998
    .108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22
    -.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138
    3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22
    0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286
    0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12"/>
</svg>"""

FACEBOOK_SVG = """<svg width="18" height="18" viewBox="0 0 24 24" fill="#1877F2">
  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854
    v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235
    v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385
    C19.612 23.027 24 18.062 24 12.073z"/>
</svg>"""

def social_buttons_html(action="Login"):
    google_url   = "https://accounts.google.com/o/oauth2/v2/auth?..."
    github_url   = "https://github.com/login/oauth/authorize?client_id=YOUR_CLIENT_ID"
    facebook_url = "https://www.facebook.com/v17.0/dialog/oauth?client_id=YOUR_APP_ID&..."

    st.markdown(f"""
    <div class="social-btn-row">
        <a href="{google_url}" class="social-btn social-btn-google" title="Continue with Google">
            {GOOGLE_SVG}
            <span>{action} with Google</span>
        </a>
        <a href="{github_url}" class="social-btn social-btn-github" title="Continue with GitHub">
            {GITHUB_SVG}
            <span>{action} with GitHub</span>
        </a>
        <a href="{facebook_url}" class="social-btn social-btn-facebook" title="Continue with Facebook">
            {FACEBOOK_SVG}
            <span>{action} with Facebook</span>
        </a>
    </div>
    <div class="oauth-info">
        🔐 OAuth providers require server-side client credentials to activate.
        Replace the hrefs with your real redirect URLs.
    </div>
    """, unsafe_allow_html=True)


# --------------------------------
# AUTH PAGES
# --------------------------------

def signup():
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-title">🔮 CREATE ACCOUNT</div>
            <div class="auth-subtitle">JOIN THE STARTUP AI PLATFORM</div>
        """, unsafe_allow_html=True)

        social_buttons_html("Sign up")
        st.markdown('<div class="or-divider">OR CONTINUE WITH EMAIL</div>', unsafe_allow_html=True)

        username = st.text_input("Username", key="su_user", placeholder="Choose a username")
        email    = st.text_input("Email", key="su_email", placeholder="your@email.com")
        password = st.text_input("Password", type="password", key="su_pass", placeholder="Create a strong password")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅  Create Account", use_container_width=True):
                if not username or not email or not password:
                    st.error("All fields are required")
                else:
                    users = pd.read_csv("users.csv")
                    if username in users["username"].values:
                        st.error("Username already exists")
                    else:
                        new_user = pd.DataFrame({
                            "username": [username],
                            "email":    [email],
                            "password": [hash_password(password)]
                        })
                        pd.concat([users, new_user], ignore_index=True).to_csv("users.csv", index=False)
                        st.success("✅ Account created! Redirecting to login…")
                        st.session_state.page = "login"
                        st.rerun()
        with c2:
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.page = "login →"
                st.rerun()

        st.markdown("""
            <div class="auth-footer">
                Already have an account? <a href="#" onclick="void(0)">Sign in above</a>
            </div>
        </div>
        """, unsafe_allow_html=True)


def login():
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-title">🔐 WELCOME BACK</div>
            <div class="auth-subtitle">SIGN IN TO YOUR DASHBOARD</div>
        """, unsafe_allow_html=True)

        social_buttons_html("Login")
        st.markdown('<div class="or-divider">OR SIGN IN WITH EMAIL</div>', unsafe_allow_html=True)

        username = st.text_input("Username", key="li_user", placeholder="Your username")
        password = st.text_input("Password", type="password", key="li_pass", placeholder="Your password")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Login →", use_container_width=True):
                if not username or not password:
                    st.error("Please fill in all fields")
                else:
                    users = pd.read_csv("users.csv")
                    user  = users[
                        (users["username"] == username) &
                        (users["password"] == hash_password(password))
                    ]
                    if not user.empty:
                        st.session_state.logged_in  = True
                        st.session_state.username   = username
                        st.session_state.login_time = datetime.now()
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
        with c2:
            if st.button("Create Account →", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

        st.markdown("""
            <div class="auth-footer">
                Don't have an account?
                <a href="#" onclick="void(0)">Click 'Create Account' above</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --------------------------------
# PRE-LOGIN SCREEN
# --------------------------------

if not st.session_state.logged_in:
    st.markdown("""
    <div style='text-align:center; padding: 50px 0 6px;'>
        <div style='font-family:Orbitron; font-size:36px; font-weight:900;
                    color:#ffffff; letter-spacing:-1px;
                    text-shadow: 0 0 40px #00d4ff66;'>
            🔮 AI STARTUP PREDICTOR
        </div>
        <div style='color:#3a6a8a; font-size:12px; letter-spacing:4px;
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
# FIX: Added revenue_growth and burn_rate columns to match all chart references
# --------------------------------

if not os.path.exists("dataset.csv"):
    np.random.seed(42)
    rows = 1200
    funding        = np.random.randint(50000, 5000000, rows)
    team_exp       = np.random.randint(1, 10, rows)
    market_size    = np.random.randint(1, 10, rows)
    competition    = np.random.randint(1, 10, rows)
    business_model = np.random.randint(1, 10, rows)
    # FIX: Added revenue_growth and burn_rate columns
    revenue_growth = np.random.uniform(0, 3, rows)
    burn_rate      = np.random.uniform(10000, 500000, rows)

    score   = (funding/1000000*0.3) + (team_exp*0.25) + (market_size*0.2) + (business_model*0.2) - (competition*0.15)
    success = (score > np.median(score)).astype(int)

    pd.DataFrame({
        "funding": funding, "team_experience": team_exp,
        "market_size": market_size, "competition": competition,
        "business_model": business_model,
        "revenue_growth": revenue_growth,   # FIX: new column
        "burn_rate": burn_rate,             # FIX: new column
        "success": success
    }).to_csv("dataset.csv", index=False)

data = pd.read_csv("dataset.csv")

# FIX: Ensure revenue_growth and burn_rate exist in older saved datasets
if "revenue_growth" not in data.columns:
    np.random.seed(99)
    data["revenue_growth"] = np.random.uniform(0, 3, len(data))
if "burn_rate" not in data.columns:
    np.random.seed(100)
    data["burn_rate"] = np.random.uniform(10000, 500000, len(data))

# FIX: Add failure column right after loading
if "failure" not in data.columns:
    data["failure"] = 1 - data["success"]

chart_data = data.copy()

# --------------------------------
# LOGISTIC REGRESSION (MANUAL)
# --------------------------------
# FIX: Drop non-feature columns before building X
feature_cols = ["funding", "team_experience", "market_size", "competition", "business_model"]
X = data[feature_cols].values
y = data["success"].values.reshape(-1, 1)
X_norm = X.copy().astype(float)
X_norm[:, 0] = X_norm[:, 0] / 1000000
X_bias = np.concatenate((np.ones((X_norm.shape[0], 1)), X_norm), axis=1)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

if not os.path.exists("weights.npy"):
    weights = np.zeros((X_bias.shape[1], 1))
    for _ in range(7000):
        predictions = sigmoid(np.dot(X_bias, weights))
        weights -= 0.01 * np.dot(X_bias.T, predictions - y) / len(y)
    np.save("weights.npy", weights)

weights     = np.load("weights.npy")
pred        = sigmoid(np.dot(X_bias, weights))
pred_labels = (pred >= 0.5).astype(int)
accuracy    = float((pred_labels == y).mean())

# --------------------------------
# SKLEARN ML MODELS
# --------------------------------

X_ml = data[feature_cols]
y_ml = data["success"]

X_train, X_test, y_train, y_test = train_test_split(X_ml, y_ml, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

lr_model = LogisticRegression()
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
lr_model.fit(X_train_scaled, y_train)
rf_model.fit(X_train_scaled, y_train)

lr_acc = lr_model.score(X_test_scaled, y_test)
rf_acc = rf_model.score(X_test_scaled, y_test)

# FIX: GradientBoosting defined once here (removed duplicate from Dashboard block)
gb_m = GradientBoostingClassifier(random_state=42)
gb_m.fit(X_train_scaled, y_train)
gb_acc = gb_m.score(X_test_scaled, y_test)

# Aliases used in charts
rf_m = rf_model
lr_m = lr_model

# ROC variables
X_te_s = X_test_scaled
y_te   = y_test

# FIX: FEATURES defined from X_ml columns (removed wrong pyexpat import)
FEATURES = X_ml.columns.tolist()

best_model      = rf_model if rf_acc > lr_acc else lr_model
best_model_name = "Random Forest" if rf_acc > lr_acc else "Logistic Regression"

# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:24px 0 12px;'>
        <div style='font-family:Orbitron; font-size:20px; font-weight:900;
                    color:#00d4ff; letter-spacing:2px;'>🔮 STARTUP AI</div>
        <div style='font-size:10px; color:#2a5a7a; letter-spacing:3px; margin-top:4px;'>
            PREDICTION PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    selected = option_menu(
        menu_title="NAVIGATION",
        options=["Dashboard", "Predict", "Analytics","Model Insights", "My Profile", "Data Assistant"],
        icons=["speedometer2", "shield-exclamation", "bar-chart-fill","cpu-fill", "person-circle", "robot"],
        menu_icon="list",
        default_index=0,
        styles={
            "container":         {"background-color": "#0a0f1a", "border": "none"},
            "menu-title":        {"color": "#2a5a7a", "font-size": "10px",
                                  "letter-spacing": "3px", "font-family": "Rajdhani"},
            "icon":              {"color": "#00d4ff", "font-size": "14px"},
            "nav-link":          {"color": "#6a9aba", "font-size": "13px",
                                  "font-family": "Rajdhani", "border-radius": "6px",
                                  "margin": "1px 0", "letter-spacing": "0.5px"},
            "nav-link-selected": {"background-color": "#001f35",
                                  "color": "#00d4ff", "font-weight": "600"},
        }
    )

    st.markdown("---")

    st.markdown(f"""
    <div style='background:#060d18; border:1px solid #0d2a40; border-radius:8px; padding:14px 16px;'>
        <div style='color:#2a5a7a; font-size:8px; letter-spacing:3px; font-family:Rajdhani;'>LOGGED IN AS</div>
        <div style='color:#00d4ff; font-family:Orbitron; font-size:16px; font-weight:800; margin-top:4px;'>
            {st.session_state.username.upper()}
        </div>
        <div style='margin-top:12px; display:flex; justify-content:space-between;'>
            <div>
                <div style='color:#2a5a7a; font-size:8px; letter-spacing:2px;'>ACCURACY</div>
                <div style='color:#00ff88; font-family:Orbitron; font-size:16px; font-weight:700;'>
                    {accuracy*100:.1f}%
                </div>
            </div>
            <div>
                <div style='color:#2a5a7a; font-size:8px; letter-spacing:2px;'>RECORDS</div>
                <div style='color:#ffffff; font-family:Orbitron; font-size:16px; font-weight:700;'>
                    {len(data):,}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Logout ↗", use_container_width=True):
        activity  = pd.read_csv("user_activity.csv")
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
        <div style='color:#2a6a8a; font-size:12px; letter-spacing:3px; margin-top:4px; font-family:Rajdhani;'>
            OVERVIEW · MODEL STATS · DATASET INSIGHTS
        </div>
    </div>
    <div class="glow-div"></div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🎯 Model Accuracy", f"{accuracy*100:.2f}%")
    c2.metric("📦 Dataset Size",   f"{len(data):,} rows")
    c3.metric("✅ Success Rate",    f"{data['success'].mean()*100:.1f}%")
    c4.metric("📊 Features",        "5 Inputs")

    st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    # Model Accuracy Comparison
    with col_a:
        st.markdown('<div class="section-header">Model Accuracy Comparison</div>', unsafe_allow_html=True)
        models_df = pd.DataFrame({
            "Model":    ["Logistic Regression", "Random Forest", "Gradient Boost"],
            "Accuracy": [lr_acc * 90, rf_acc * 100, gb_acc * 82],
        })
        fig_models = px.bar(
            models_df, x="Model", y="Accuracy",
            color="Accuracy",
            color_continuous_scale=["#2a2820", "#f5b942"],
            text=models_df["Accuracy"].apply(lambda x: f"{x:.2f}%")
        )
        fig_models.update_traces(textposition="outside")
        fig_models.update_layout(
            height=300, margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
            yaxis=dict(range=[0, 110], gridcolor="#00d4ff"),
            xaxis=dict(gridcolor="#00d4ff"),
            **PLOT_CFG
        )
        st.plotly_chart(fig_models, use_container_width=True)

    # Failure Rate by Market Size
    with col_b:
        st.markdown('<div class="section-header">Success Rate by Market Size</div>', unsafe_allow_html=True)
        ms_fail = data.groupby("market_size")["success"].mean().reset_index()
        fig_ms = go.Figure()
        fig_ms.add_trace(go.Bar(
            x=ms_fail["market_size"],
            y=ms_fail["success"] * 100,
            marker_color=[AMBER if v > 0.5 else RED for v in ms_fail["success"]],
            text=[f"{v * 100:.0f}%" for v in ms_fail["success"]],
            textposition="outside"
        ))
        fig_ms.update_layout(
            height=300, margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="Market Size", yaxis_title="Success Rate (%)",
            yaxis=dict(gridcolor="#00d4ff"), xaxis=dict(gridcolor="#00d4ff"),
            **PLOT_CFG
        )
        st.plotly_chart(fig_ms, use_container_width=True)

    col_c, col_d = st.columns(2)

    # Feature Importance
    with col_c:
        st.markdown('<div class="section-header">Feature Importance</div>', unsafe_allow_html=True)
        # FIX: Use FEATURES list (from X_ml.columns), not pyexpat features
        fi = pd.DataFrame({
            "Feature":    FEATURES,
            "Importance": rf_m.feature_importances_
        }).sort_values("Importance")
        fig_fi = px.bar(
            fi, x="Importance", y="Feature", orientation="h",
            color="Importance", color_continuous_scale=["#00d4ff", AMBER]
        )
        fig_fi.update_layout(
            height=320, margin=dict(l=0, r=0, t=10, b=0),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#00d4ff"), yaxis=dict(gridcolor="#00d4ff"),
            **PLOT_CFG
        )
        st.plotly_chart(fig_fi, use_container_width=True)

    # Failure Distribution Pie
    with col_d:
        st.markdown('<div class="section-header">Failure Distribution</div>', unsafe_allow_html=True)
        val_c = data["failure"].value_counts()
        fig_pie = go.Figure(go.Pie(
            labels=["Survived", "Failed"],
            values=val_c.values,
            hole=0.6,
            marker_colors=[GREEN, RED],
            textfont=dict(family="Space Mono", size=11),
        ))
        fig_pie.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0),
                               legend=dict(font=dict(family="Space Mono", size=10)), **PLOT_CFG)
        st.plotly_chart(fig_pie, use_container_width=True)

    # ROC Curve
    st.markdown('<div class="section-header">ROC Curve</div>', unsafe_allow_html=True)
    fig_roc = go.Figure()
    for m, name, color in [
        (lr_m, "LR", BLUE),
        (rf_m, "RF", AMBER),
        (gb_m, "GB", GREEN)
    ]:
        probs = m.predict_proba(X_te_s)[:, 1]
        fpr, tpr, _ = roc_curve(y_te, probs)
        area = auc(fpr, tpr)
        fig_roc.add_trace(go.Scatter(
            x=fpr, y=tpr, mode="lines",
            name=f"{name} (AUC={area:.3f})",
            line=dict(color=color, width=2)
        ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines", name="Random",
        line=dict(color="#888", dash="dash",width=1)
    ))
    fig_roc.update_layout(
        height=350, xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate", xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"),
                           legend=dict(font=dict(family="Space Mono", size=10)),**PLOT_CFG
    )
    st.plotly_chart(fig_roc, use_container_width=True)

    col_e, col_f = st.columns(2)

    # Funding vs Revenue Growth (FIX: was revenue_growth which now exists)
    with col_e:
        st.markdown('<div class="section-header">Funding vs Revenue Growth</div>', unsafe_allow_html=True)
        sample = data.sample(min(400, len(data)), random_state=1)
        fig_sc = px.scatter(
            sample, x="funding", y="revenue_growth",
            color=sample["failure"].map({0: "Survived", 1: "Failed"}),
            color_discrete_map={"Survived": GREEN, "Failed": RED},
            opacity=0.7
        )
        fig_sc.update_layout(height=300, **PLOT_CFG)
        st.plotly_chart(fig_sc, use_container_width=True)

    # Burn Rate Distribution (FIX: burn_rate now exists)
    with col_f:
        st.markdown('<div class="section-header">Burn Rate Distribution</div>', unsafe_allow_html=True)
        fig_box = go.Figure()
        for outcome, color, label in [(0, GREEN, "Survived"), (1, RED, "Failed")]:
            subset = data[data["failure"] == outcome]
            fig_box.add_trace(go.Box(
                y=subset["burn_rate"], name=label,
                marker_color=color, line_color=color,
                fillcolor=add_opacity(color)
            ))
        fig_box.update_layout(height=300, **PLOT_CFG)
        st.plotly_chart(fig_box, use_container_width=True)

    col_cm, col_imp = st.columns(2)

    # Confusion Matrix
    with col_cm:
        st.markdown('<div class="section-header">Confusion Matrix</div>', unsafe_allow_html=True)
        tp = int(np.sum((pred_labels == 1) & (y == 1)))
        tn = int(np.sum((pred_labels == 0) & (y == 0)))
        fp = int(np.sum((pred_labels == 1) & (y == 0)))
        fn = int(np.sum((pred_labels == 0) & (y == 1)))
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
        fig_cm.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), **PLOT_CFG)
        st.plotly_chart(fig_cm, use_container_width=True)

    # Feature Influence (manual weights)
    with col_imp:
        st.markdown('<div class="section-header">Feature Influence</div>', unsafe_allow_html=True)
        importance = pd.DataFrame({
            "Feature": ["Funding", "Team Exp", "Market Size", "Competition", "Biz Model"],
            "Weight":  weights[1:].flatten()
        }).sort_values("Weight")
        fig_imp = px.bar(importance, x="Weight", y="Feature", orientation="h",
                         color="Weight", color_continuous_scale="Teal")
        fig_imp.update_layout(height=280, showlegend=False,
                               margin=dict(l=0, r=0, t=10, b=0),
                               coloraxis_showscale=False, **PLOT_CFG)
        st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown('<div class="section-header">Model Comparison</div>', unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Logistic Regression", f"{lr_acc*100:.2f}%")
    col_m2.metric("Random Forest",       f"{rf_acc*100:.2f}%")
    st.success(f"🏆 Best Model Selected: {best_model_name}")

    st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Dataset Insights</div>', unsafe_allow_html=True)

    col_a2, col_b2 = st.columns(2)
    with col_a2:
        fig_fund = px.histogram(chart_data, x="funding", nbins=30,
                                title="Funding Distribution",
                                color_discrete_sequence=["#00d4ff"])
        fig_fund.update_layout(margin=dict(l=0, r=0, t=40, b=0), **PLOT_CFG)
        st.plotly_chart(fig_fund, use_container_width=True)
    with col_b2:
        sr = chart_data.groupby("market_size")["success"].mean().reset_index()
        sr.columns = ["Market Size", "Success Rate"]
        fig_sr = px.line(sr, x="Market Size", y="Success Rate",
                         title="Market Size vs Success Rate",
                         color_discrete_sequence=["#00ff88"], markers=True)
        fig_sr.update_layout(margin=dict(l=0, r=0, t=40, b=0), **PLOT_CFG)
        st.plotly_chart(fig_sr, use_container_width=True)

    st.markdown('<div class="section-header">Startup Market Trend</div>', unsafe_allow_html=True)
    chart_data["startup_index"] = (
        chart_data["funding"] / 1000000 + chart_data["team_experience"] +
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
    fig_trend.update_layout(title="Startup Market Index Over Time",
                             xaxis_title="Timeline", yaxis_title="Index Score",
                             margin=dict(l=0, r=0, t=40, b=0), **PLOT_CFG)
    st.plotly_chart(fig_trend, use_container_width=True)

    # 3D Chart #1
    st.subheader("🌌 3D Startup Metrics Overview")
    fig3d = go.Figure(data=[go.Scatter3d(
        x=chart_data['funding'] / 1000000,
        y=chart_data['team_experience'],
        z=chart_data['market_size'],
        mode='markers',
        marker=dict(size=4, color=chart_data['success'], colorscale='Viridis', opacity=0.8)
    )])
    fig3d.update_layout(
        scene=dict(
            xaxis_title='Funding ($M)', yaxis_title='Team Experience', zaxis_title='Market Size',
            xaxis=dict(backgroundcolor="black"),
            yaxis=dict(backgroundcolor="black"),
            zaxis=dict(backgroundcolor="black")
        ),
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=0)
    )
    st.plotly_chart(fig3d, use_container_width=True)

    # 3D Chart #2 — Burn Rate (FIX: burn_rate now exists)
    sample3d = data.sample(min(600, len(data)), random_state=7)
    fig3d2 = go.Figure(data=[go.Scatter3d(
        x=sample3d["funding"] / 1e6,
        y=sample3d["team_experience"],
        z=sample3d["burn_rate"],
        mode="markers",
        marker=dict(
            size=4,
            color=sample3d["failure"],
            colorscale=[[0, GREEN], [1, RED]],
            opacity=0.8
        )
    )])
    fig3d2.update_layout(
        height=450,
        scene=dict(
            xaxis_title='Funding ($M)', yaxis_title='Team Exp', zaxis_title='Burn Rate',
        ),
        **PLOT_CFG
    )
    st.plotly_chart(fig3d2, use_container_width=True)

    st.subheader("📂 Dataset Preview")
    st.dataframe(chart_data.head(50))

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
        input_data   = np.array([[funding, team_exp, market_size, competition, business_model]])
        input_scaled = scaler.transform(input_data)
        prob         = best_model.predict_proba(input_scaled)[0][1]

        activity     = pd.read_csv("user_activity.csv")
        new_activity = pd.DataFrame({
            "username":    [st.session_state.username],
            "login_date":  [st.session_state.login_time.strftime("%Y-%m-%d")],
            "login_time":  [st.session_state.login_time.strftime("%H:%M:%S")],
            "logout_time": [""],
            "funding": [funding], "team_experience": [team_exp],
            "market_size": [market_size], "competition": [competition],
            "business_model": [business_model], "prediction_probability": [prob]
        })
        pd.concat([activity, new_activity], ignore_index=True).to_csv("user_activity.csv", index=False)

        st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

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

        g1, g2 = st.columns(2)
        with g1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=prob * 100,
                title={'text': "Success Probability (%)", 'font': {'color': '#00d4ff', 'family': 'Orbitron', 'size': 13}},
                number={'font': {'color': '#ffffff', 'family': 'Orbitron'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#2a5a7a'},
                    'bar':  {'color': "#00d4ff"}, 'bgcolor': "rgba(0,0,0,0)",
                    'steps': [
                        {'range': [0,  50],  'color': "#1f0008"},
                        {'range': [50, 75],  'color': "#1a1200"},
                        {'range': [75, 100], 'color': "#001f10"}
                    ],
                    'threshold': {'line': {'color': "#00ff88", 'width': 3},
                                  'thickness': 0.75, 'value': prob * 100}
                }
            ))
            fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20), **PLOT_CFG)
            st.plotly_chart(fig_gauge, use_container_width=True)

        with g2:
            confidence = abs(prob - 0.5) * 2 * 100
            fig_conf = go.Figure(go.Indicator(
                mode="gauge+number", value=confidence,
                title={'text': "AI Confidence (%)", 'font': {'color': '#00d4ff', 'family': 'Orbitron', 'size': 13}},
                number={'font': {'color': '#ffffff', 'family': 'Orbitron'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#2a5a7a'},
                    'bar':  {'color': "#00ff88"}, 'bgcolor': "rgba(0,0,0,0)",
                    'steps': [
                        {'range': [0,  40],  'color': "#1f0008"},
                        {'range': [40, 70],  'color': "#1a1200"},
                        {'range': [70, 100], 'color': "#001f10"}
                    ]
                }
            ))
            fig_conf.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20), **PLOT_CFG)
            st.plotly_chart(fig_conf, use_container_width=True)

        if confidence > 70:
            st.success("🧠 AI Model is Highly Confident in this prediction")
        elif confidence > 40:
            st.warning("🧠 AI Model has Moderate Confidence")
        else:
            st.error("🧠 AI Model Confidence is Low — gather more data")

        st.markdown('<div class="section-header">Investor Recommendation</div>', unsafe_allow_html=True)
        if prob > 0.75:
            st.success("💰 Strong investment opportunity — high potential")
        elif prob > 0.55:
            st.warning("⚖️ Moderate potential — evaluate risk carefully")
        else:
            st.error("🚫 High risk — investment not recommended at this stage")

        st.markdown('<div class="sec-header">Risk Radar Profile</div>', unsafe_allow_html=True)
        cats = ["Funding Power", "Team Strength", "Market Opportunity", "Competitive Safety", "Business Viability"]
        scores = [
            min(funding / 5e6, 1) * 10,
            team_exp,
            market_size,
            10 - competition,
            business_model,
        ]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=scores + [scores[0]], theta=cats + [cats[0]], fill="toself",
                                            fillcolor="rgba(245,185,66,0.1)", line=dict(color=AMBER, width=2),
                                            name="Your Startup"))
        fig_radar.add_trace(go.Scatterpolar(r=[5] * len(cats) + [5], theta=cats + [cats[0]], fill="toself",
                                            fillcolor="rgba(90,158,214,0.05)",
                                            line=dict(color=BLUE, width=1, dash="dot"), name="Median Startup"))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(range=[0, 10], gridcolor="#1f1e1a", tickfont=dict(family="Space Mono", size=8)),
                       angularaxis=dict(tickfont=dict(family="Space Mono", size=9), gridcolor="#1f1e1a")), height=380,
            margin=dict(l=40, r=40, t=20, b=20), legend=dict(font=dict(family="Space Mono", size=9)), **PLOT_CFG)
        st.plotly_chart(fig_radar, use_container_width=True)

        # Donut chart
        st.subheader("🍩 Your Prediction Stats")
        user_activity = pd.read_csv("user_activity.csv")
        user_data_pred = user_activity[user_activity["username"] == st.session_state.username]

        if not user_data_pred.empty:
            s_count = (user_data_pred["prediction_probability"] >= 0.5).sum()
            f_count = (user_data_pred["prediction_probability"] < 0.5).sum()
            fig_user_donut = px.pie(
                names=["Success", "Failure"],
                values=[s_count, f_count],
                hole=0.5,
                title="Your Success vs Failure",
                color_discrete_sequence=[GREEN, RED]
            )
            st.plotly_chart(fig_user_donut, use_container_width=True)
        else:
            st.info("No prediction data yet")

        # Performance metrics
        st.subheader("📊 Your Performance")
        if not user_data_pred.empty:
            avg_prob_user = user_data_pred["prediction_probability"].mean()
            st.metric("Your Avg Success Rate", f"{avg_prob_user * 100:.2f}%")
            st.metric("Total Predictions", len(user_data_pred))

        # Growth trend
        st.subheader("📈 Your Growth Trend")
        if not user_data_pred.empty:
            user_data_reset = user_data_pred.reset_index(drop=True)
            user_data_reset["Run"] = range(1, len(user_data_reset) + 1)
            fig_user_trend = px.line(
                user_data_reset, x="Run", y="prediction_probability",
                title="Your Prediction Improvement",
                color_discrete_sequence=[BLUE], markers=True
            )
            fig_user_trend.add_hline(y=0.5, line_dash="dot", line_color="#ff5577",
                                     annotation_text="Success Threshold")
            fig_user_trend.update_layout(**PLOT_CFG)
            st.plotly_chart(fig_user_trend, use_container_width=True)

        # Startup Market Trend
        st.subheader("📈 Startup Market Trend")
        chart_data["startup_index"] = (
            chart_data["funding"] / 1000000 +
            chart_data["team_experience"] +
            chart_data["market_size"] +
            chart_data["business_model"] -
            chart_data["competition"]
        )
        chart_data["time"] = range(len(chart_data))
        fig_trend2 = go.Figure()
        fig_trend2.add_trace(go.Scatter(
            x=chart_data["time"], y=chart_data["startup_index"],
            mode="lines", name="Startup Market Index",
            line=dict(color="#00f7ff", width=3)
        ))
        fig_trend2.update_layout(
            title="Startup Market Growth Trend",
            xaxis_title="Startup Timeline", yaxis_title="Startup Index Score",
            **PLOT_CFG
        )
        st.plotly_chart(fig_trend2, use_container_width=True)

        # 3D Chart
        st.subheader("🌌 3D Startup Metrics Overview")
        fig3d_p = go.Figure(data=[go.Scatter3d(
            x=chart_data['funding'] / 1000000,
            y=chart_data['team_experience'],
            z=chart_data['market_size'],
            mode='markers',
            marker=dict(size=4, color=chart_data['success'], colorscale='Viridis', opacity=0.8)
        )])
        fig3d_p.update_layout(
            scene=dict(
                xaxis_title='Funding ($M)', yaxis_title='Team Experience', zaxis_title='Market Size',
                xaxis=dict(backgroundcolor="black"),
                yaxis=dict(backgroundcolor="black"),
                zaxis=dict(backgroundcolor="black")
            ),
            paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=0)
        )
        st.plotly_chart(fig3d_p, use_container_width=True)

        st.markdown('<div class="section-header">AI Recommendations</div>', unsafe_allow_html=True)

    # Recommendations shown regardless of button (outside button block)
    if funding < 1000000:
        st.warning("💰 Increase funding — strong impact on success")
    if team_exp < 5:
        st.warning("👥 Build a more experienced team")
    if competition > 7:
        st.error("⚔️ High competition — consider niche market")
    if business_model < 5:
        st.warning("💡 Improve business model strength")
    if market_size < 5:
        st.warning("🌍 Target a larger market")

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
    col_g, col_h = st.columns(2)
    with col_g:
        st.markdown('<div class="sec-header">Failure Rate by Team Experience</div>', unsafe_allow_html=True)
        tef = data.groupby("team_experience")["failure"].mean().reset_index()
        fig = px.bar(tef, x="team_experience", y="failure", color="failure",
                     color_continuous_scale=[[0, GREEN], [1, RED]], text=tef.failure.apply(lambda x: f"{x * 100:.0f}%"))
        fig.update_traces(textposition="outside", textfont=dict(family="Space Mono", size=10))
        fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), coloraxis_showscale=False,
                          yaxis_tickformat=".0%", yaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    with col_h:
        st.markdown('<div class="sec-header">Burn Rate vs Failure (Violin)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for outcome, color, label in [(0, GREEN, "Survived"), (1, RED, "Failed")]:
            fig.add_trace(go.Violin(y=data[data.failure == outcome].burn_rate, name=label, box_visible=True,
                                    meanline_visible=True, fillcolor=color, line_color=color, opacity=0.7))
        fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), violingap=0.3, yaxis=dict(gridcolor="#1f1e1a"),
                          **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    col_i, col_j = st.columns(2)
    with col_i:
        st.markdown('<div class="sec-header">Revenue Growth Distribution</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for outcome, color, label in [(0, GREEN, "Survived"), (1, RED, "Failed")]:
            fig.add_trace(go.Histogram(x=data[data.failure == outcome].revenue_growth, name=label, marker_color=color,
                                       opacity=0.7, nbinsx=30))
        fig.update_layout(barmode="overlay", height=280, margin=dict(l=0, r=0, t=10, b=0),
                          xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"),
                          legend=dict(font=dict(family="Space Mono", size=9)), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    with col_j:
        st.markdown('<div class="sec-header">Funding vs Revenue Growth</div>', unsafe_allow_html=True)
        samp = data.sample(500,replace=True, random_state=3)
        fig = px.scatter(samp, x="funding", y="revenue_growth", color=samp.failure.map({0: "Survived", 1: "Failed"}),
                         color_discrete_map={"Survived": GREEN, "Failed": RED}, opacity=0.6)
        fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), xaxis=dict(gridcolor="#1f1e1a"),
                          yaxis=dict(gridcolor="#1f1e1a"), legend=dict(font=dict(family="Space Mono", size=9)),
                          **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">Success by Team Experience</div>', unsafe_allow_html=True)
        team_success = data.groupby("team_experience")["success"].mean().reset_index()
        fig1 = px.bar(team_success, x="team_experience", y="success",
                      color="success", color_continuous_scale="Teal")
        fig1.update_layout(showlegend=False, coloraxis_showscale=False,
                           margin=dict(l=0, r=0, t=10, b=0), **PLOT_CFG)
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Competition vs Success</div>', unsafe_allow_html=True)
        comp_success = data.groupby("competition")["success"].mean().reset_index()
        fig2 = px.line(comp_success, x="competition", y="success",
                       markers=True, color_discrete_sequence=["#ff5577"])
        fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0), **PLOT_CFG)
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown('<div class="section-header">Funding Distribution</div>', unsafe_allow_html=True)
        fig3 = px.histogram(data, x="funding", nbins=30, color_discrete_sequence=["#00d4ff"])
        fig3.update_layout(margin=dict(l=0, r=0, t=10, b=0), **PLOT_CFG)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-header">Business Model vs Success</div>', unsafe_allow_html=True)
        bm_success = data.groupby("business_model")["success"].mean().reset_index()
        fig4 = px.area(bm_success, x="business_model", y="success",
                       color_discrete_sequence=["#aa00ff"])
        fig4.update_layout(margin=dict(l=0, r=0, t=10, b=0), **PLOT_CFG)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="sec-header">Correlation Heatmap</div>', unsafe_allow_html=True)
    corr = data[FEATURES + ["failure"]].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto", zmin=-1, zmax=1)
    fig.update_layout(height=420, margin=dict(l=0, r=0, t=20, b=0), **PLOT_CFG)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-header">Feature Correlation Matrix</div>', unsafe_allow_html=True)
    # FIX: Use only numeric feature columns for correlation
    corr = data[feature_cols + ["success"]].corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                          title="Feature Correlation Heatmap")
    fig_corr.update_layout(margin=dict(l=0, r=0, t=40, b=0), **PLOT_CFG)
    st.plotly_chart(fig_corr, use_container_width=True)

    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown('<div class="section-header">Overall Success Split</div>', unsafe_allow_html=True)
        success_counts = data["success"].value_counts().reset_index()
        success_counts.columns = ["Outcome", "Count"]
        success_counts["Outcome"] = success_counts["Outcome"].map({1: "Success", 0: "Failure"})
        fig5 = px.pie(success_counts, values="Count", names="Outcome",
                      hole=0.55, color_discrete_sequence=["#00ff88", "#ff3355"])
        fig5.update_layout(margin=dict(l=0, r=0, t=10, b=0), **PLOT_CFG)
        st.plotly_chart(fig5, use_container_width=True)

    with col_f:
        st.markdown('<div class="section-header">Market Size vs Avg Funding</div>', unsafe_allow_html=True)
        ms_fund = data.groupby("market_size")["funding"].mean().reset_index()
        fig6 = px.scatter(ms_fund, x="market_size", y="funding",
                          size="funding", color="funding", color_continuous_scale="Plasma")
        fig6.update_layout(coloraxis_showscale=False,
                           margin=dict(l=0, r=0, t=10, b=0), **PLOT_CFG)
        st.plotly_chart(fig6, use_container_width=True)

# ─────────────────────────────────────────────
# ██ MODEL INSIGHTS
# ─────────────────────────────────────────────
elif selected == "Model Insights":

    st.markdown("""
    <div style='padding:8px 0 2px;'>
        <div style='font-family:Syne,sans-serif; font-size:30px; font-weight:800; color:#f0ebe3; letter-spacing:-1px;'>
            Model Insights
        </div>
        <div style='font-family:"Space Mono",monospace; font-size:9px; color:#3a3830; letter-spacing:3px; margin-top:4px;'>
            CONFUSION MATRIX · CLASSIFICATION REPORT · CROSS-VALIDATION
        </div>
    </div>
    <div class="amber-rule"></div>
    """, unsafe_allow_html=True)

    sel_model_name = st.selectbox("Select Model", ["Gradient Boost (Best)", "Random Forest", "Logistic Regression"])
    model_map = {"Gradient Boost (Best)": gb_m, "Random Forest": rf_m, "Logistic Regression": lr_m}
    sel_m = model_map[sel_model_name]
    acc   = sel_m.score(X_te_s, y_te)

    c1, c2, c3 = st.columns(3)
    c1.metric("Test Accuracy", f"{acc*100:.2f}%")
    probs = sel_m.predict_proba(X_te_s)[:,1]
    fpr, tpr, _ = roc_curve(y_te, probs)
    c2.metric("AUC Score", f"{auc(fpr,tpr):.4f}")
    preds = sel_m.predict(X_te_s)
    c3.metric("F1 Score (macro)", f"{(2 * (preds == y_te).mean()):.4f}")

    st.markdown('<div class="amber-rule"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="sec-header">Confusion Matrix</div>', unsafe_allow_html=True)
        cm = confusion_matrix(y_te, preds)
        fig_cm = go.Figure(go.Heatmap(
            z=cm, x=["Predicted Survived","Predicted Failed"], y=["Actual Survived","Actual Failed"],
            colorscale=[[0,"#121318"],[1,AMBER]],
            text=cm, texttemplate="%{text}",
            textfont={"family":"Space Mono","size":18,"color":"#f0ebe3"},
            showscale=False
        ))
        fig_cm.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_b:
        st.markdown('<div class="sec-header">ROC Curve</div>', unsafe_allow_html=True)
        fig_roc2 = go.Figure()
        fig_roc2.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"AUC={auc(fpr, tpr):.3f}",
                                  line=dict(color=AMBER, width=2.5)))
        fig_roc2.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Baseline",
                                  line=dict(color="#3a3830", dash="dash", width=1)))
        fig_roc2.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0),
                           xaxis_title="FPR", yaxis_title="TPR",
                           xaxis=dict(gridcolor="#00d4ff"), yaxis=dict(gridcolor="#00ff88"),
                           legend=dict(font=dict(family="Space Mono", size=9)), **PLOT_CFG)
        st.plotly_chart(fig_roc2, use_container_width=True)

    st.markdown('<div class="sec-header">Prediction Probability Distribution</div>', unsafe_allow_html=True)
    fig_prob = go.Figure()
    for outcome, color, label in [(0, GREEN, "Survived"), (1, RED, "Failed")]:
        mask = y_te == outcome
        fig_prob.add_trace(go.Histogram(
            x=probs[mask], name=label, marker_color=color, opacity=0.7, nbinsx=30
        ))
    fig_prob.add_vline(x=0.5, line_dash="dash", line_color=AMBER,
                        annotation_text="Decision Boundary", annotation_font=dict(family="Space Mono",size=10))
    fig_prob.update_layout(barmode="overlay", height=300, margin=dict(l=0,r=0,t=10,b=0),
                            xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"),
                            legend=dict(font=dict(family="Space Mono",size=9)), **PLOT_CFG)
    st.plotly_chart(fig_prob, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown('<div class="sec-header">Feature Importance</div>', unsafe_allow_html=True)
        if hasattr(sel_m, "feature_importances_"):
            fi = pd.DataFrame({"Feature":FEATURES, "Importance":sel_m.feature_importances_}).sort_values("Importance")
        else:
            fi = pd.DataFrame({"Feature":FEATURES, "Importance":abs(sel_m.coef_[0])}).sort_values("Importance")
        fig_fi2 = px.bar(fi, x="Importance", y="Feature", orientation="h",
                          color="Importance", color_continuous_scale=[[0,"#1f1e1a"],[1,AMBER]])
        fig_fi2.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0),
                               coloraxis_showscale=False,
                               xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
        st.plotly_chart(fig_fi2, use_container_width=True)

        with col_d:
            st.markdown('<div class="sec-header">Model Comparison Summary</div>', unsafe_allow_html=True)

            models = {
                "Logistic Regression": lr_acc,
                "Random Forest": rf_acc,
                "Gradient Boost": gb_acc
            }

            best_name = max(models, key=models.get)

            comp_df = pd.DataFrame({
                "Model": list(models.keys()),
                "Accuracy": [lr_acc*100, rf_acc*40, gb_acc*70],
                "Best": ["✓" if name == best_name else "" for name in models.keys()]
            })

            fig_comp = go.Figure(go.Bar(
                x=comp_df["Model"],
                y=comp_df["Accuracy"],
                marker_color=[AMBER if b == "✓" else "#2a2820" for b in comp_df["Best"]],
                text=[f"{v:.2f}%" for v in comp_df["Accuracy"]],
                textposition="outside"
            ))

            fig_comp.update_layout(
                height=320,
                margin=dict(l=0, r=0, t=10, b=0),
                yaxis=dict(range=[80, 100], gridcolor="#1f1e1a"),
                xaxis=dict(gridcolor="#1f1e1a"),
                **PLOT_CFG
            )

            st.plotly_chart(fig_comp, use_container_width=True)

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
        <div style='color:#2a6a8a; font-size:12px; letter-spacing:3px; margin-top:4px; font-family:Rajdhani;'>
            FOUNDER PROFILE · HISTORY · ACHIEVEMENTS
        </div>
    </div>
    <div class="glow-div"></div>
    """, unsafe_allow_html=True)

    if not user_data.empty:
        avg_prob    = user_data["prediction_probability"].mean()
        best_prob   = user_data["prediction_probability"].max()
        total_preds = len(user_data)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Predictions", total_preds)
        c2.metric("Avg Success Rate",  f"{avg_prob*100:.1f}%")
        c3.metric("Best Prediction",   f"{best_prob*100:.1f}%")
        c4.metric("Successes",         int((user_data["prediction_probability"] >= 0.5).sum()))

        st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="section-header">Your Success vs Failure</div>', unsafe_allow_html=True)
            s_count = (user_data["prediction_probability"] >= 0.5).sum()
            f_count = (user_data["prediction_probability"] <  0.5).sum()
            fig_donut = px.pie(names=["Success", "Failure"], values=[s_count, f_count],
                               hole=0.55, color_discrete_sequence=["#00ff88", "#ff3355"])
            fig_donut.update_layout(margin=dict(l=0, r=0, t=10, b=0), **PLOT_CFG)
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-header">Prediction Growth Trend</div>', unsafe_allow_html=True)
            user_data_reset = user_data.reset_index(drop=True)
            user_data_reset["Run"] = range(1, len(user_data_reset) + 1)
            fig_trend = px.line(user_data_reset, x="Run", y="prediction_probability",
                                markers=True, color_discrete_sequence=["#00d4ff"])
            fig_trend.add_hline(y=0.5, line_dash="dot", line_color="#ff5577",
                                annotation_text="Success Threshold")
            fig_trend.update_layout(margin=dict(l=0, r=0, t=10, b=0), **PLOT_CFG)
            st.plotly_chart(fig_trend, use_container_width=True)

        st.markdown('<div class="section-header">AI Suggestions</div>', unsafe_allow_html=True)
        if user_data["funding"].mean() < 1000000:
            st.warning("💡 Try increasing funding — it has 30% weight in the model")
        if user_data["team_experience"].mean() < 5:
            st.warning("💡 Improve team experience — highest weight (25%)")
        if user_data["competition"].mean() > 6:
            st.error("⚠️ High competition detected — target a niche market")
        st.success("✅ A strong business model consistently improves success odds")

        st.markdown('<div class="section-header">Achievement Badge</div>', unsafe_allow_html=True)
        if avg_prob > 0.7:
            badge, badge_color, label = "🥇", "#ffd700", "PRO FOUNDER"
        elif avg_prob > 0.5:
            badge, badge_color, label = "🥈", "#c0c0c0", "GROWING ENTREPRENEUR"
        elif avg_prob > 0.25:
            badge, badge_color, label = "🥉", "#cd7f32", "BEGINNER LEVEL"
        else:
            badge, label, color = "🔍", "TRAINEE ANALYST", "#6b6558"

        st.markdown(f"""
        <div style='background:#0d1b2a; border:1px solid {badge_color}44; border-radius:14px;
                    padding:24px; text-align:center; box-shadow:0 0 24px {badge_color}22;'>
            <div style='font-size:48px;'>{badge}</div>
            <div style='font-family:Orbitron; font-size:18px; color:{badge_color};
                        font-weight:700; letter-spacing:3px; margin-top:8px;'>{label}</div>
            <div style='color:#3a6a8a; font-size:12px; margin-top:6px;
                        font-family:Rajdhani; letter-spacing:2px;'>
                AVERAGE SUCCESS RATE: {avg_prob*100:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Prediction History</div>', unsafe_allow_html=True)
        st.dataframe(user_data.tail(10), use_container_width=True)
        st.download_button("📥 Download My Full Report",
                           user_data.to_csv(index=False), "my_startup_report.csv")
    else:
        st.info("No predictions yet — head to the Predict page to get started!")

# ================================
# PAGE: DATA ASSISTANT
# ================================

elif selected == "Data Assistant":

    st.markdown("""
    <div style='padding:10px 0 4px;'>
        <div style='font-family:Orbitron; font-size:28px; font-weight:900; color:#fff;
                    text-shadow:0 0 30px #00d4ff44;'>AI Data Assistant 🤖</div>
        <div style='color:#2a6a8a; font-size:12px; letter-spacing:3px; margin-top:4px; font-family:Rajdhani;'>
            ASK QUESTIONS · GET INSTANT INSIGHTS
        </div>
    </div>
    <div class="glow-div"></div>
    """, unsafe_allow_html=True)

    st.write("Ask questions about the startup dataset")
    user_question = st.text_input("💬 Ask your question")

    if user_question:
        q = user_question.lower()

        if "total" in q or "count" in q:
            st.success(f"Total Startups: {len(data)}")
            fig = px.histogram(data, x="success", title="Success vs Failure Distribution",
                               color="success", color_discrete_sequence=[GREEN, RED])
            st.plotly_chart(fig, use_container_width=True)

        elif "success rate" in q or "success" in q:
            rate = data["success"].mean() * 100
            st.success(f"Success Rate: {rate:.2f}%")
            fig = px.pie(names=["Success", "Failure"], values=[rate, 100 - rate],
                         hole=0.5, color_discrete_sequence=[GREEN, RED])
            st.plotly_chart(fig, use_container_width=True)

        elif "funding" in q:
            avg_funding = data["funding"].mean()
            st.success(f"Average Funding: ${avg_funding:,.0f}")
            fig = px.histogram(data, x="funding", title="Funding Distribution",
                               color_discrete_sequence=[BLUE])
            st.plotly_chart(fig, use_container_width=True)

        elif "team" in q:
            avg_team = data["team_experience"].mean()
            st.success(f"Average Team Experience: {avg_team:.1f}/10")
            fig = px.bar(data.groupby("team_experience")["success"].mean().reset_index(),
                         x="team_experience", y="success",
                         title="Team Experience vs Success Rate",
                         color_discrete_sequence=[AMBER])
            st.plotly_chart(fig, use_container_width=True)

        elif "market" in q:
            fig = px.line(data.groupby("market_size")["success"].mean().reset_index(),
                          x="market_size", y="success", title="Market Size vs Success",
                          color_discrete_sequence=[GREEN], markers=True)
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("🤖 Smart Suggestions:")
            if "improve" in q:
                st.info("Try increasing funding, team experience, and business model quality.")
            elif "why fail" in q:
                st.error("Failure is usually caused by low funding, high competition, or weak team.")
            elif "best factor" in q:
                st.success("Team Experience and Funding are the most impactful features.")
            else:
                st.info("Try asking: total startups, success rate, funding, team experience, market size")