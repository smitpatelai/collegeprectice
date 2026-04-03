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
from sklearn.ensemble import RandomForestClassifier
import hashlib

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(page_title="AI Startup Dashboard", layout="wide", page_icon="🧊")

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

/* ============================================================
   SOCIAL AUTH BUTTONS — MAIN STYLED BUTTONS
   ============================================================ */

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

/* Social buttons row */
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

/* Google */
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

/* GitHub */
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

/* Facebook */
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

/* Or divider */
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

/* Login footer */
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

/* OAuth info banner */
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

/* Animated glow pulse on auth card */
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
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(6,9,16,0.6)"
)

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
    """Render Google / GitHub / Facebook social buttons as styled HTML anchors."""
    # In production, replace these hrefs with your real OAuth redirect URLs:
    #   Google  → https://accounts.google.com/o/oauth2/v2/auth?...
    #   GitHub  → https://github.com/login/oauth/authorize?client_id=YOUR_CLIENT_ID
    #   Facebook→ https://www.facebook.com/v17.0/dialog/oauth?client_id=YOUR_APP_ID&...
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
        Replace the hrefs in with your real redirect URLs.
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
            <div class="auth-title">🧊 CREATE ACCOUNT</div>
            <div class="auth-subtitle">JOIN THE STARTUP AI PLATFORM</div>
        """, unsafe_allow_html=True)

        # ── Social buttons
        social_buttons_html("Sign up")

        # ── Divider
        st.markdown('<div class="or-divider">OR CONTINUE WITH EMAIL</div>', unsafe_allow_html=True)

        # ── Form fields
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
                st.session_state.page = "login"
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

        # ── Social buttons
        social_buttons_html("Login")

        # ── Divider
        st.markdown('<div class="or-divider">OR SIGN IN WITH EMAIL</div>', unsafe_allow_html=True)

        # ── Form fields
        username = st.text_input("Username", key="li_user", placeholder="Your username")
        password = st.text_input("Password", type="password", key="li_pass", placeholder="Your password")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀  Login", use_container_width=True):
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
            🧊 AI STARTUP PREDICTOR
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
# --------------------------------

if not os.path.exists("dataset.csv"):
    np.random.seed(42)
    rows = 1200
    funding        = np.random.randint(50000, 5000000, rows)
    team_exp       = np.random.randint(1, 10, rows)
    market_size    = np.random.randint(1, 10, rows)
    competition    = np.random.randint(1, 10, rows)
    business_model = np.random.randint(1, 10, rows)
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

weights     = np.load("weights.npy")
pred        = sigmoid(np.dot(X, weights))
pred_labels = (pred >= 0.5).astype(int)
accuracy    = (pred_labels == y).mean()

# --------------------------------
# ADVANCED ML MODEL
# --------------------------------

X_ml = data.drop("success", axis=1)
y_ml = data["success"]
X_train, X_test, y_train, y_test = train_test_split(X_ml, y_ml, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

lr_model = LogisticRegression()
rf_model = RandomForestClassifier()
lr_model.fit(X_train_scaled, y_train)
rf_model.fit(X_train_scaled, y_train)

lr_acc = lr_model.score(X_test_scaled, y_test)
rf_acc = rf_model.score(X_test_scaled, y_test)

best_model      = rf_model if rf_acc > lr_acc else lr_model
best_model_name = "Random Forest" if rf_acc > lr_acc else "Logistic Regression"

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
        options=["Dashboard", "Predict", "Analytics", "My Profile", "Data Assistant"],
        icons=["speedometer2", "cpu", "bar-chart-fill", "person-circle", "robot"],
        menu_icon="grid-fill",
        default_index=0,
        styles={
            "container":         {"background-color": "#0a0f1a", "border": "none"},
            "menu-title":        {"color": "#2a5a7a", "font-size": "10px",
                                  "letter-spacing": "3px", "font-family": "Rajdhani"},
            "icon":              {"color": "#00d4ff", "font-size": "15px"},
            "nav-link":          {"color": "#6a9aba", "font-size": "13px",
                                  "font-family": "Rajdhani", "border-radius": "8px",
                                  "margin": "2px 0", "letter-spacing": "1px"},
            "nav-link-selected": {"background-color": "#001f35",
                                  "color": "#00d4ff", "font-weight": "600"},
        }
    )

    st.markdown("---")

    st.markdown(f"""
    <div style='background:#060d18; border:1px solid #0d2a40; border-radius:12px; padding:14px;'>
        <div style='color:#2a5a7a; font-size:10px; letter-spacing:3px; font-family:Rajdhani;'>LOGGED IN AS</div>
        <div style='color:#00d4ff; font-family:Orbitron; font-size:15px; font-weight:700; margin-top:4px;'>
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
        fig_imp = px.bar(importance, x="Weight", y="Feature", orientation="h",
                         color="Weight", color_continuous_scale="Teal")
        fig_imp.update_layout(height=280, showlegend=False,
                               margin=dict(l=0,r=0,t=10,b=0),
                               coloraxis_showscale=False, **PLOT_CFG)
        st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown('<div class="section-header">Model Comparison</div>', unsafe_allow_html=True)
    col_m1, col_m2 = st.columns(2)
    col_m1.metric("Logistic Regression", f"{lr_acc*100:.2f}%")
    col_m2.metric("Random Forest",       f"{rf_acc*100:.2f}%")
    st.success(f"🏆 Best Model Selected: {best_model_name}")

    st.markdown('<div class="glow-div"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Dataset Insights</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        fig_fund = px.histogram(chart_data, x="funding", nbins=30,
                                title="Funding Distribution",
                                color_discrete_sequence=["#00d4ff"])
        fig_fund.update_layout(margin=dict(l=0,r=0,t=40,b=0), **PLOT_CFG)
        st.plotly_chart(fig_fund, use_container_width=True)
    with col_b:
        sr = chart_data.groupby("market_size")["success"].mean().reset_index()
        sr.columns = ["Market Size", "Success Rate"]
        fig_sr = px.line(sr, x="Market Size", y="Success Rate",
                         title="Market Size vs Success Rate",
                         color_discrete_sequence=["#00ff88"], markers=True)
        fig_sr.update_layout(margin=dict(l=0,r=0,t=40,b=0), **PLOT_CFG)
        st.plotly_chart(fig_sr, use_container_width=True)

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
    fig_trend.update_layout(title="Startup Market Index Over Time",
                             xaxis_title="Timeline", yaxis_title="Index Score",
                             margin=dict(l=0,r=0,t=40,b=0), **PLOT_CFG)
    st.plotly_chart(fig_trend, use_container_width=True)

    st.subheader("🌌 3D Startup Metrics Overview")
    fig3d = go.Figure(data=[go.Scatter3d(
        x=chart_data['funding']/1000000,
        y=chart_data['team_experience'],
        z=chart_data['market_size'],
        mode='markers',
        marker=dict(size=7, color=chart_data['success'], colorscale='Viridis', opacity=0.9)
    )])
    fig3d.update_layout(
        scene=dict(xaxis_title='Funding ($M)', yaxis_title='Team Experience', zaxis_title='Market Size',
                   xaxis=dict(backgroundcolor="black"), yaxis=dict(backgroundcolor="black"),
                   zaxis=dict(backgroundcolor="black")),
        paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, b=0, t=0)
    )
    st.plotly_chart(fig3d, use_container_width=True)

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

        if prob >= 0.5:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#001f14,#002a1c);
                        border:1px solid #00ff88; border-radius:14px;
                        padding:24px; text-align:center; margin:12px 0;
                        box-shadow:0 0 30px #00ff8833;'>
                <div style='font-family:Orbitron; font-size:22px; color:#00ff88; font-weight:700; letter-spacing:2px;'>
                    ✅ STARTUP WILL SUCCEED
                </div>
                <div style='color:#00cc66; font-size:14px; margin-top:8px; font-family:Rajdhani; letter-spacing:2px;'>
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
                <div style='font-family:Orbitron; font-size:22px; color:#ff3355; font-weight:700; letter-spacing:2px;'>
                    ⚠️ HIGH RISK OF FAILURE
                </div>
                <div style='color:#cc2244; font-size:14px; margin-top:8px; font-family:Rajdhani; letter-spacing:2px;'>
                    SUCCESS PROBABILITY: {prob*100:.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        g1, g2 = st.columns(2)
        with g1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=prob*100,
                title={'text': "Success Probability (%)", 'font': {'color': '#00d4ff', 'family': 'Orbitron', 'size': 13}},
                number={'font': {'color': '#ffffff', 'family': 'Orbitron'}},
                gauge={
                    'axis': {'range': [0,100], 'tickcolor': '#2a5a7a'},
                    'bar':  {'color': "#00d4ff"}, 'bgcolor': "rgba(0,0,0,0)",
                    'steps': [{'range': [0,50], 'color': "#1f0008"},
                               {'range': [50,75], 'color': "#1a1200"},
                               {'range': [75,100], 'color': "#001f10"}],
                    'threshold': {'line': {'color': "#00ff88", 'width': 3}, 'thickness': 0.75, 'value': prob*100}
                }
            ))
            fig_gauge.update_layout(height=260, margin=dict(l=20,r=20,t=40,b=20), **PLOT_CFG)
            st.plotly_chart(fig_gauge, use_container_width=True)

        with g2:
            confidence = abs(prob - 0.5) * 2 * 100
            fig_conf = go.Figure(go.Indicator(
                mode="gauge+number", value=confidence,
                title={'text': "AI Confidence (%)", 'font': {'color': '#00d4ff', 'family': 'Orbitron', 'size': 13}},
                number={'font': {'color': '#ffffff', 'family': 'Orbitron'}},
                gauge={
                    'axis': {'range': [0,100], 'tickcolor': '#2a5a7a'},
                    'bar':  {'color': "#00ff88"}, 'bgcolor': "rgba(0,0,0,0)",
                    'steps': [{'range': [0,40],  'color': "#1f0008"},
                               {'range': [40,70], 'color': "#1a1200"},
                               {'range': [70,100],'color': "#001f10"}]
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

        st.markdown('<div class="section-header">Investor Recommendation</div>', unsafe_allow_html=True)
        if prob > 0.75:
            st.success("💰 Strong investment opportunity — high potential")
        elif prob > 0.55:
            st.warning("⚖️ Moderate potential — evaluate risk carefully")
        else:
            st.error("🚫 High risk — investment not recommended at this stage")

        # ------------------------------
        # Donat chart
        # -----------------------------

        st.subheader("🍩 Your Prediction Stats")

        user_activity = pd.read_csv("user_activity.csv")
        user_data = user_activity[user_activity["username"] == st.session_state.username]

        if not user_data.empty:

                success = (user_data["prediction_probability"] >= 0.5).sum()
                failure = (user_data["prediction_probability"] < 0.5).sum()

                fig_user_donut = px.pie(
                    names=["Success", "Failure"],
                    values=[success, failure],
                    hole=0.5,
                    title="Your Success vs Failure"
                )

                st.plotly_chart(fig_user_donut, use_container_width=True)

        else:
                st.info("No prediction data yet")
        # ----------------
        # parformance
        # ----------------
        st.subheader("📊 Your Performance")

        if not user_data.empty:
                avg_prob = user_data["prediction_probability"].mean()

                st.metric("Your Avg Success Rate", f"{avg_prob * 100:.2f}%")

                st.metric("Total Predictions", len(user_data))
        # --------------
        # growth trend
        # --------------
        st.subheader("📈 Your Growth Trend")

        if not user_data.empty:
                user_data = user_data.reset_index()

                fig_user_trend = px.line(
                    user_data,
                    x=user_data.index,
                    y="prediction_probability",
                    title="Your Prediction Improvement"
                )

                st.plotly_chart(fig_user_trend, use_container_width=True)

        # --------------------------------
        # STARTUP MARKET TREND (STOCK STYLE)
        # --------------------------------

        st.subheader("📈 Startup Market Trend")

        chart_data["startup_index"] = (
                    chart_data["funding"] / 1000000 +
                    chart_data["team_experience"] +
                    chart_data["market_size"] +
                    chart_data["business_model"] -
                    chart_data["competition"]
        )

        chart_data["time"] = range(len(chart_data))

        fig_trend = go.Figure()

        fig_trend.add_trace(go.Scatter(
                x=chart_data["time"],
                y=chart_data["startup_index"],
                mode="lines",
                name="Startup Market Index",
                line=dict(color="#00f7ff", width=3)
        ))

        fig_trend.update_layout(
                title="Startup Market Growth Trend",
                xaxis_title="Startup Timeline",
                yaxis_title="Startup Index Score",
                template="plotly_dark"
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

        st.markdown('<div class="section-header">AI Recommendations</div>', unsafe_allow_html=True)
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
    # prob = None  # initialize
    #
    # if st.button("Predict"):
    #     input_data = np.array([[funding, team_exp, market_size, competition, business_model]])
    #     input_scaled = scaler.transform(input_data)
    #
    #     prob = best_model.predict_proba(input_scaled)[0][1]
    #
    #     st.success(f"Success Probability: {prob * 100:.2f}%")
    #
    # # ✅ SAFE CHECK
    # if prob is not None and prob > 0.75:
    #     st.success("🚀 Excellent startup potential!")

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

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-header">Success by Team Experience</div>', unsafe_allow_html=True)
        team_success = data.groupby("team_experience")["success"].mean().reset_index()
        fig1 = px.bar(team_success, x="team_experience", y="success",
                      color="success", color_continuous_scale="Teal")
        fig1.update_layout(showlegend=False, coloraxis_showscale=False,
                           margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Competition vs Success</div>', unsafe_allow_html=True)
        comp_success = data.groupby("competition")["success"].mean().reset_index()
        fig2 = px.line(comp_success, x="competition", y="success",
                       markers=True, color_discrete_sequence=["#ff5577"])
        fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown('<div class="section-header">Funding Distribution</div>', unsafe_allow_html=True)
        fig3 = px.histogram(data, x="funding", nbins=30, color_discrete_sequence=["#00d4ff"])
        fig3.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig3, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-header">Business Model vs Success</div>', unsafe_allow_html=True)
        bm_success = data.groupby("business_model")["success"].mean().reset_index()
        fig4 = px.area(bm_success, x="business_model", y="success",
                       color_discrete_sequence=["#aa00ff"])
        fig4.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown('<div class="section-header">Feature Correlation Matrix</div>', unsafe_allow_html=True)
    corr = data.corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                          title="Feature Correlation Heatmap")
    fig_corr.update_layout(margin=dict(l=0,r=0,t=40,b=0), **PLOT_CFG)
    st.plotly_chart(fig_corr, use_container_width=True)

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
                          size="funding", color="funding", color_continuous_scale="Plasma")
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
        <div style='color:#2a6a8a; font-size:12px; letter-spacing:3px; margin-top:4px; font-family:Rajdhani;'>
            FOUNDER PROFILE · HISTORY · ACHIEVEMENTS
        </div>
    </div>
    <div class="glow-div"></div>
    """, unsafe_allow_html=True)

    if not user_data.empty:
        avg_prob  = user_data["prediction_probability"].mean()
        best_prob = user_data["prediction_probability"].max()
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
            fig_donut = px.pie(names=["Success","Failure"], values=[s_count, f_count],
                               hole=0.55, color_discrete_sequence=["#00ff88","#ff3355"])
            fig_donut.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-header">Prediction Growth Trend</div>', unsafe_allow_html=True)
            user_data_reset = user_data.reset_index(drop=True)
            user_data_reset["Run"] = range(1, len(user_data_reset)+1)
            fig_trend = px.line(user_data_reset, x="Run", y="prediction_probability",
                                markers=True, color_discrete_sequence=["#00d4ff"])
            fig_trend.add_hline(y=0.5, line_dash="dot", line_color="#ff5577",
                                annotation_text="Success Threshold")
            fig_trend.update_layout(margin=dict(l=0,r=0,t=10,b=0), **PLOT_CFG)
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
        else:
            badge, badge_color, label = "🥉", "#cd7f32", "BEGINNER LEVEL"

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
        st.download_button("📥 Download My Full Report", user_data.to_csv(index=False), "my_startup_report.csv")

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
            fig = px.histogram(data, x="success", title="Success vs Failure Distribution", color="success")
            st.plotly_chart(fig, use_container_width=True)

        elif "success rate" in q or "success" in q:
            rate = data["success"].mean() * 100
            st.success(f"Success Rate: {rate:.2f}%")
            fig = px.pie(names=["Success","Failure"], values=[rate, 100-rate], hole=0.5)
            st.plotly_chart(fig, use_container_width=True)

        elif "funding" in q:
            avg_funding = data["funding"].mean()
            st.success(f"Average Funding: ${avg_funding:,.0f}")
            fig = px.histogram(data, x="funding", title="Funding Distribution")
            st.plotly_chart(fig, use_container_width=True)

        elif "team" in q:
            avg_team = data["team_experience"].mean()
            st.success(f"Average Team Experience: {avg_team:.1f}/10")
            fig = px.bar(data.groupby("team_experience")["success"].mean().reset_index(),
                         x="team_experience", y="success", title="Team Experience vs Success Rate")
            st.plotly_chart(fig, use_container_width=True)

        elif "market" in q:
            fig = px.line(data.groupby("market_size")["success"].mean().reset_index(),
                          x="market_size", y="success", title="Market Size vs Success")
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


#ML MODEL AND ALGORIDHAM
#1. Logistic Regression
#2. Random Forest Classifier
#3. (Optional Advanced) Pipeline Model