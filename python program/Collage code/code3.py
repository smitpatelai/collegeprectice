from datetime import datetime

import confidence
import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_curve, auc, confusion_matrix
import hashlib
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="StartupOracle — Failure Prediction Engine",
    layout="wide",
    page_icon="🔮",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Amber/Obsidian Industrial Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #0b0c0f;
    color: #d4cfc8;
}

[data-testid="stSidebar"] {
    background: #0e0f13 !important;
    border-right: 1px solid #1f1e1a !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: #121318;
    border: 1px solid #2a2820;
    border-radius: 8px;
    padding: 16px 18px;
}
[data-testid="metric-container"] label {
    color: #6b6558 !important;
    font-size: 10px !important;
    font-family: 'Space Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 2px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #f5b942 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] { font-family: 'Space Mono', monospace !important; }

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    color: #f0ebe3 !important;
    letter-spacing: -0.5px;
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #121318 !important;
    border: 1px solid #2a2820 !important;
    color: #d4cfc8 !important;
    border-radius: 6px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #f5b942 !important;
    box-shadow: 0 0 0 2px #f5b94220 !important;
}

.stSelectbox > div > div,
.stMultiSelect > div {
    background: #121318 !important;
    border: 1px solid #2a2820 !important;
    color: #d4cfc8 !important;
    border-radius: 6px !important;
}

/* Sliders */
[data-testid="stSlider"] > div > div > div {
    background: #f5b942 !important;
}
.stSlider [data-baseweb="slider"] > div:first-child {
    background: #1f1e1a !important;
}

/* Buttons */
.stButton > button {
    background: #f5b942 !important;
    color: #0b0c0f !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    transition: all 0.15s ease;
    padding: 10px 18px !important;
}
.stButton > button:hover {
    background: #f7c96a !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px #f5b94244 !important;
}

.stDownloadButton > button {
    background: #1a2e1a !important;
    color: #5dde8c !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    border: 1px solid #5dde8c44 !important;
    border-radius: 6px !important;
}

/* Alerts */
.stSuccess { background: #0e1e14 !important; border-left: 3px solid #5dde8c !important; border-radius: 0 6px 6px 0 !important; }
.stError   { background: #1e0e0e !important; border-left: 3px solid #e05c5c !important; border-radius: 0 6px 6px 0 !important; }
.stWarning { background: #1e1800 !important; border-left: 3px solid #f5b942 !important; border-radius: 0 6px 6px 0 !important; }
.stInfo    { background: #0e141e !important; border-left: 3px solid #5a9ed6 !important; border-radius: 0 6px 6px 0 !important; }

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #2a2820;
    border-radius: 8px;
    overflow: hidden;
}

/* Divider */
hr { border-color: #1f1e1a !important; }

/* ── AUTH CARD ── */
.auth-card {
    background: linear-gradient(160deg, #121318 0%, #0e0f13 100%);
    border: 1px solid #2a2820;
    border-radius: 12px;
    padding: 40px 36px 32px;
    position: relative;
    overflow: hidden;
}
.auth-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #f5b942, transparent);
}

.auth-logo {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #f5b942;
    text-align: center;
    letter-spacing: -1px;
    margin-bottom: 4px;
}
.auth-tagline {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #3a3830;
    text-align: center;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 28px;
}

/* Section headers */
.sec-header {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    color: #6b6558;
    letter-spacing: 3px;
    text-transform: uppercase;
    border-bottom: 1px solid #1f1e1a;
    padding-bottom: 8px;
    margin-bottom: 16px;
    margin-top: 8px;
}

.amber-rule {
    height: 1px;
    background: linear-gradient(90deg, transparent, #f5b94244, transparent);
    margin: 20px 0;
}

/* Risk badge */
.risk-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 4px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.risk-critical { background: #2a0808; color: #e05c5c; border: 1px solid #e05c5c44; }
.risk-high     { background: #2a1500; color: #f5945c; border: 1px solid #f5945c44; }
.risk-medium   { background: #2a1e00; color: #f5b942; border: 1px solid #f5b94244; }
.risk-low      { background: #0a2014; color: #5dde8c; border: 1px solid #5dde8c44; }

/* Sidebar brand */
.sb-brand {
    text-align: center;
    padding: 20px 0 8px;
}
.sb-brand-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: #f5b942;
    letter-spacing: -0.5px;
}
.sb-brand-sub {
    font-family: 'Space Mono', monospace;
    font-size: 8px;
    color: #3a3830;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* Result card */
.result-success {
    background: linear-gradient(135deg, #0a1e0e, #0d2412);
    border: 1px solid #5dde8c55;
    border-radius: 10px;
    padding: 28px 24px;
    text-align: center;
    margin: 16px 0;
}
.result-failure {
    background: linear-gradient(135deg, #1e0a0a, #2a0e0e);
    border: 1px solid #e05c5c55;
    border-radius: 10px;
    padding: 28px 24px;
    text-align: center;
    margin: 16px 0;
}

/* Stats strip */
.stats-strip {
    background: #121318;
    border: 1px solid #2a2820;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Timeline item */
.timeline-item {
    border-left: 2px solid #2a2820;
    padding: 8px 0 8px 16px;
    margin-bottom: 4px;
    position: relative;
}
.timeline-item::before {
    content: '';
    width: 7px; height: 7px;
    background: #f5b942;
    border-radius: 50%;
    position: absolute;
    left: -4.5px;
    top: 12px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PLOT_CFG = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(18,19,24,0.8)",
    font=dict(family="Space Mono, monospace", color="#6b6558"),
)
AMBER   = "#f5b942"
GREEN   = "#5dde8c"
RED     = "#e05c5c"
BLUE    = "#5a9ed6"
ORANGE  = "#f5945c"
PURPLE  = "#a78bde"

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
defaults = {"logged_in": False, "page": "login", "username": "", "login_time": None}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

# ─────────────────────────────────────────────
# FILE INIT
# ─────────────────────────────────────────────
if not os.path.exists("users.csv"):
    pd.DataFrame(columns=["username","email","password","joined"]).to_csv("users.csv", index=False)

if not os.path.exists("user_activity.csv"):
    pd.DataFrame(columns=[
        "username","date","time","funding","team_exp","market_size",
        "competition","biz_model","years_operating","burn_rate",
        "revenue_growth","debt_ratio","failure_prob","risk_tier"
    ]).to_csv("user_activity.csv", index=False)

# ─────────────────────────────────────────────
# DATASET GENERATION (RICHER)
# ─────────────────────────────────────────────
if not os.path.exists("startups.csv"):
    np.random.seed(99)
    n = 2000
    funding       = np.random.randint(50000, 10000000, n)
    team_exp      = np.random.randint(1, 10, n)
    market_size   = np.random.randint(1, 10, n)
    competition   = np.random.randint(1, 10, n)
    biz_model     = np.random.randint(1, 10, n)
    years_op      = np.random.randint(0, 15, n)
    burn_rate     = np.random.uniform(0.05, 0.95, n)   # monthly cash burn ratio
    rev_growth    = np.random.uniform(-0.3, 1.5, n)    # YoY revenue growth
    debt_ratio    = np.random.uniform(0, 2.0, n)       # debt / equity

    score = (
        funding/5e6 * 0.25 +
        team_exp/10 * 0.20 +
        market_size/10 * 0.15 +
        biz_model/10 * 0.15 +
        rev_growth   * 0.15 -
        competition/10 * 0.10 -
        burn_rate    * 0.10 -
        debt_ratio/2 * 0.10 +
        np.random.normal(0, 0.08, n)
    )
    failure = (score < np.median(score)).astype(int)   # 1 = failed

    pd.DataFrame({
        "funding": funding, "team_experience": team_exp, "market_size": market_size,
        "competition": competition, "business_model": biz_model,
        "years_operating": years_op, "burn_rate": burn_rate.round(3),
        "revenue_growth": rev_growth.round(3), "debt_ratio": debt_ratio.round(3),
        "failure": failure
    }).to_csv("startups.csv", index=False)

data = pd.read_csv("startups.csv")

# ─────────────────────────────────────────────
# TRAIN MODELS
# ─────────────────────────────────────────────
FEATURES = ["funding","team_experience","market_size","competition",
            "business_model","years_operating","burn_rate","revenue_growth","debt_ratio"]

X = data[FEATURES]
y = data["failure"]

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_tr_s = scaler.fit_transform(X_tr)
X_te_s  = scaler.transform(X_te)

@st.cache_resource
def train_models():
    lr  = LogisticRegression(max_iter=500, random_state=42)
    rf  = RandomForestClassifier(n_estimators=150, random_state=42)
    gb  = GradientBoostingClassifier(n_estimators=150, random_state=42)
    for m in [lr, rf, gb]:
        m.fit(X_tr_s, y_tr)
    return lr, rf, gb

lr_m, rf_m, gb_m = train_models()

lr_acc = lr_m.score(X_te_s, y_te)
rf_acc = rf_m.score(X_te_s, y_te)
gb_acc = gb_m.score(X_te_s, y_te)

best_model      = max([(lr_m, lr_acc, "Logistic Regression"), (rf_m, rf_acc, "Random Forest"), (gb_m, gb_acc, "Gradient Boost")], key=lambda x: x[1])
best_m, best_acc, best_name = best_model

def risk_tier(prob):
    if prob >= 0.75:   return "CRITICAL", "risk-critical"
    elif prob >= 0.55: return "HIGH",     "risk-high"
    elif prob >= 0.35: return "MEDIUM",   "risk-medium"
    else:              return "LOW",      "risk-low"

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

# ─────────────────────────────────────────────
# AUTH PAGES
# ─────────────────────────────────────────────
def page_login():
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-logo">🔮 StartupOracle</div>
            <div class="auth-tagline">Failure Prediction · Risk Intelligence · Decision Support</div>
        """, unsafe_allow_html=True)

        social_buttons_html("Sign up")
        st.markdown('<div class="or-divider">OR CONTINUE WITH EMAIL</div>', unsafe_allow_html=True)

        username = st.text_input("Username", key="li_u", placeholder="your_username")
        password = st.text_input("Password", type="password", key="li_p", placeholder="••••••••••")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("SIGN IN →", use_container_width=True):
                if not username or not password:
                    st.error("All fields required")
                else:
                    users = pd.read_csv("users.csv")
                    match = users[(users.username == username) & (users.password == hash_pw(password))]
                    if not match.empty:
                        st.session_state.logged_in  = True
                        st.session_state.username   = username
                        st.session_state.login_time = datetime.now()
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        with c2:
            if st.button("Create Account", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


def page_signup():
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("""
        <div class="auth-card">
            <div class="auth-logo">🔮 Create Account</div>
            <div class="auth-tagline">Join the intelligence platform</div>
        """, unsafe_allow_html=True)
        social_buttons_html("Sign up")
        st.markdown('<div class="or-divider">OR CONTINUE WITH EMAIL</div>', unsafe_allow_html=True)

        username = st.text_input("Username", key="su_u", placeholder="choose_username")
        email    = st.text_input("Email",    key="su_e", placeholder="you@company.com")
        password = st.text_input("Password", type="password", key="su_p", placeholder="strong_password")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("REGISTER →", use_container_width=True):
                if not all([username, email, password]):
                    st.error("All fields required")
                else:
                    users = pd.read_csv("users.csv")
                    if username in users.username.values:
                        st.error("Username taken")
                    else:
                        new = pd.DataFrame({"username":[username],"email":[email],
                                            "password":[hash_pw(password)],"joined":[datetime.now().date()]})
                        pd.concat([users, new], ignore_index=True).to_csv("users.csv", index=False)
                        st.success("Account created — sign in!")
                        st.session_state.page = "login"
                        st.rerun()
        with c2:
            if st.button("← Back", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PRE-LOGIN GATE
# ─────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("""
    <div style='text-align:center; padding:48px 0 4px;'>
        <div style='font-family:Syne,sans-serif; font-size:40px; font-weight:800;
                    color:#f5b942; letter-spacing:-2px;'>🔮 StartupOracle</div>
        <div style='font-family:"Space Mono",monospace; font-size:9px; color:#3a3830;
                    letter-spacing:4px; text-transform:uppercase; margin-top:8px;'>
            Intelligent Decision-Support · Startup Failure Prediction · Risk Evaluation
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.page == "signup":
        page_signup()
    else:
        page_login()
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="sb-brand">
        <div class="sb-brand-title">🔮 StartupOracle</div>
        <div class="sb-brand-sub">Risk Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    selected = option_menu(
        menu_title="NAVIGATION",
        options=["Dashboard", "Risk Evaluator", "Analytics Lab", "Model Insights", "My Profile", "AI Assistant"],
        icons=["grid-1x2-fill", "shield-exclamation", "graph-up-arrow", "cpu-fill", "person-fill", "robot"],
        menu_icon="list",
        default_index=0,
        styles={
            "container":         {"background-color": "#0e0f13", "border": "none"},
            "menu-title":        {"color":"#3a3830","font-size":"9px","letter-spacing":"3px","font-family":"Space Mono"},
            "icon":              {"color":"#6b6558","font-size":"14px"},
            "nav-link":          {"color":"#6b6558","font-size":"12px","font-family":"DM Sans","border-radius":"6px",
                                  "margin":"1px 0","letter-spacing":"0.5px"},
            "nav-link-selected": {"background-color":"#1e1c16","color":"#f5b942","font-weight":"600"},
        }
    )

    st.markdown("---")

    act = pd.read_csv("activity.csv")
    user_act = act[act.username == st.session_state.username]
    total_preds = len(user_act)
    avg_risk    = user_act["failure_prob"].mean() * 100 if total_preds > 0 else 0

    st.markdown(f"""
    <div style='background:#121318; border:1px solid #2a2820; border-radius:8px; padding:14px 16px;'>
        <div style='font-family:"Space Mono",monospace; font-size:8px; color:#3a3830;
                    letter-spacing:3px; text-transform:uppercase;'>SESSION</div>
        <div style='font-family:Syne,sans-serif; font-size:16px; font-weight:800;
                    color:#f5b942; margin-top:4px;'>{st.session_state.username}</div>
        <div style='margin-top:12px; display:flex; justify-content:space-between;'>
            <div>
                <div style='font-family:"Space Mono",monospace; font-size:8px; color:#3a3830; letter-spacing:2px;'>EVALUATIONS</div>
                <div style='font-family:"Space Mono",monospace; font-size:16px; color:#d4cfc8; font-weight:700;'>{total_preds}</div>
            </div>
            <div>
                <div style='font-family:"Space Mono",monospace; font-size:8px; color:#3a3830; letter-spacing:2px;'>AVG RISK</div>
                <div style='font-family:"Space Mono",monospace; font-size:16px; color:#f5b942; font-weight:700;'>{avg_risk:.0f}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("LOGOUT ↗", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.username = ""
        st.rerun()

# ─────────────────────────────────────────────
# ██ DASHBOARD
# ─────────────────────────────────────────────
if selected == "Dashboard":

    st.markdown("""
    <div style='padding:8px 0 2px;'>
        <div style='font-family:Syne,sans-serif; font-size:30px; font-weight:800; color:#f0ebe3; letter-spacing:-1px;'>
            Mission Control
        </div>
        <div style='font-family:"Space Mono",monospace; font-size:9px; color:#3a3830; letter-spacing:3px; margin-top:4px;'>
            PLATFORM OVERVIEW · MODEL PERFORMANCE · DATASET INTELLIGENCE
        </div>
    </div>
    <div class="amber-rule"></div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Best Model Acc",  f"{best_acc*100:.1f}%")
    c2.metric("Dataset Size",    f"{len(data):,}")
    c3.metric("Failure Rate",    f"{data.failure.mean()*100:.1f}%")
    c4.metric("Features",        f"{len(FEATURES)}")
    c5.metric("Models Trained",  "3")

    st.markdown('<div class="amber-rule"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="sec-header">Model Accuracy Comparison</div>', unsafe_allow_html=True)
        models_df = pd.DataFrame({
            "Model": ["Logistic Regression", "Random Forest", "Gradient Boost"],
            "Accuracy": [lr_acc*100, rf_acc*100, gb_acc*100],
            "Type": ["Linear", "Ensemble", "Boosted"]
        })
        fig_models = px.bar(models_df, x="Model", y="Accuracy",
                            color="Accuracy", color_continuous_scale=["#2a2820","#f5b942"],
                            text=models_df["Accuracy"].apply(lambda x: f"{x:.2f}%"))
        fig_models.update_traces(textposition="outside", textfont=dict(family="Space Mono", size=11, color="#f5b942"))
        fig_models.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                                  coloraxis_showscale=False,
                                  yaxis=dict(range=[80,100], gridcolor="#1f1e1a"),
                                  xaxis=dict(gridcolor="#1f1e1a"),
                                  **PLOT_CFG)
        st.plotly_chart(fig_models, use_container_width=True)

    with col_b:
        st.markdown('<div class="sec-header">Failure Rate by Sector Proxy (Market Size)</div>', unsafe_allow_html=True)
        ms_fail = data.groupby("market_size")["failure"].mean().reset_index()
        fig_ms = go.Figure()
        fig_ms.add_trace(go.Bar(
            x=ms_fail["market_size"], y=ms_fail["failure"]*100,
            marker_color=[AMBER if v > 0.5 else RED for v in ms_fail["failure"]],
            text=[f"{v*100:.0f}%" for v in ms_fail["failure"]], textposition="outside",
            textfont=dict(family="Space Mono", size=10)
        ))
        fig_ms.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                              xaxis_title="Market Size Score", yaxis_title="Failure Rate (%)",
                              yaxis=dict(gridcolor="#1f1e1a"), xaxis=dict(gridcolor="#1f1e1a"),
                              **PLOT_CFG)
        st.plotly_chart(fig_ms, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown('<div class="sec-header">Feature Importance (Random Forest)</div>', unsafe_allow_html=True)
        fi = pd.DataFrame({"Feature": FEATURES, "Importance": rf_m.feature_importances_}).sort_values("Importance")
        fig_fi = px.bar(fi, x="Importance", y="Feature", orientation="h",
                        color="Importance", color_continuous_scale=["#1f1e1a", AMBER])
        fig_fi.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0),
                              coloraxis_showscale=False, yaxis=dict(gridcolor="#1f1e1a"),
                              xaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
        st.plotly_chart(fig_fi, use_container_width=True)

    with col_d:
        st.markdown('<div class="sec-header">Dataset Failure Distribution</div>', unsafe_allow_html=True)
        val_c = data["failure"].value_counts()
        fig_pie = go.Figure(go.Pie(
            labels=["Failed", "Survived"], values=val_c.values,
            hole=0.6, marker_colors=[RED, GREEN],
            textfont=dict(family="Space Mono", size=11),
        ))
        fig_pie.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0),
                               legend=dict(font=dict(family="Space Mono", size=10)),
                               **PLOT_CFG)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('<div class="sec-header">ROC Curves — All Models</div>', unsafe_allow_html=True)
    fig_roc = go.Figure()
    for m, name, color in [(lr_m, "LR", BLUE), (rf_m, "RF", AMBER), (gb_m, "GB", GREEN)]:
        probs = m.predict_proba(X_te_s)[:,1]
        fpr, tpr, _ = roc_curve(y_te, probs)
        area = auc(fpr, tpr)
        fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"{name} (AUC={area:.3f})",
                                      line=dict(color=color, width=2)))
    fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Random",
                                  line=dict(color="#3a3830", dash="dash", width=1)))
    fig_roc.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0),
                           xaxis_title="False Positive Rate", yaxis_title="True Positive Rate",
                           xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"),
                           legend=dict(font=dict(family="Space Mono", size=10)), **PLOT_CFG)
    st.plotly_chart(fig_roc, use_container_width=True)

    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown('<div class="sec-header">Funding vs Failure (Scatter)</div>', unsafe_allow_html=True)
        sample = data.sample(400, random_state=1)
        fig_sc = px.scatter(sample, x="funding", y="revenue_growth",
                             color=sample["failure"].map({0:"Survived", 1:"Failed"}),
                             color_discrete_map={"Survived": GREEN, "Failed": RED},
                             opacity=0.7, size_max=8)
        fig_sc.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                              xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"),
                              legend=dict(font=dict(family="Space Mono",size=9)), **PLOT_CFG)
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_f:
        st.markdown('<div class="sec-header">Burn Rate Distribution by Outcome</div>', unsafe_allow_html=True)
        fig_box = go.Figure()
        for outcome, color, label in [(0, GREEN, "Survived"), (1, RED, "Failed")]:
            subset = data[data.failure == outcome]
            fig_box.add_trace(go.Box(y=subset.burn_rate, name=label,
                                      marker_color=color, line_color=color,
                                      fillcolor=color.replace(")", ",0.12)").replace("rgb","rgba") if color.startswith("rgb") else color))
        fig_box.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                               yaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
        st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<div class="sec-header">3D Risk Space</div>', unsafe_allow_html=True)
    sample3d = data.sample(600, random_state=7)
    fig3d = go.Figure(data=[go.Scatter3d(
        x=sample3d.funding/1e6, y=sample3d.team_experience, z=sample3d.burn_rate,
        mode="markers",
        marker=dict(size=4, color=sample3d.failure,
                    colorscale=[[0,GREEN],[1,RED]], opacity=0.8,
                    colorbar=dict(title="Failed", tickfont=dict(family="Space Mono", size=9)))
    )])
    fig3d.update_layout(
        scene=dict(xaxis_title="Funding $M", yaxis_title="Team Exp",
                   zaxis_title="Burn Rate",
                   xaxis=dict(backgroundcolor="#121318", gridcolor="#1f1e1a"),
                   yaxis=dict(backgroundcolor="#121318", gridcolor="#1f1e1a"),
                   zaxis=dict(backgroundcolor="#121318", gridcolor="#1f1e1a")),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,b=0,t=0), height=450
    )
    st.plotly_chart(fig3d, use_container_width=True)

    st.markdown('<div class="sec-header">Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(data.head(30), use_container_width=True)

# ─────────────────────────────────────────────
# ██ RISK EVALUATOR
# ─────────────────────────────────────────────
elif selected == "RISK EVALUATOR":

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

        # RESULT CARD
        if prob < 0.5:
            st.markdown(f"""
            <div class="result-success">
                <div style='font-family:Syne,sans-serif; font-size:24px; font-weight:800; color:#5dde8c; letter-spacing:-0.5px;'>
                    ✅ LOW FAILURE RISK DETECTED
                </div>
                <div style='font-family:"Space Mono",monospace; font-size:13px; color:#3a8c5c; margin-top:8px;'>
                    SUCCESS Probability: {prob*100:.2f}% 
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-failure">
                <div style='font-family:Syne,sans-serif; font-size:24px; font-weight:800; color:#e05c5c; letter-spacing:-0.5px;'>
                    ⚠️ HIGH RISK OF FAILURE
                </div>
                <div style='font-family:"Space Mono",monospace; font-size:13px; color:#8c3a3a; margin-top:8px;'>
                    Failure Probability: {prob*100:.2f}% 
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Gauges
        g1, g2, g3 = st.columns(3)
        with g1:
            fig_g1 = go.Figure(go.Indicator(
                mode="gauge+number", value=prob*100,
                title={'text':"Failure Probability (%)",'font':{'family':'Space Mono','color':'#6b6558','size':11}},
                number={'font':{'family':'Space Mono','color':'#d4cfc8'},'suffix':'%'},
                gauge={
                    'axis':{'range':[0,100],'tickcolor':'#2a2820'},
                    'bar':{'color': "#00d4ff"}, 'bgcolor': "rgba(0,0,0,0)",
                    'steps':[{'range':[0,35],'color':'#0a1e0e'},
                              {'range':[35,55],'color':'#1e1800'},
                              {'range':[55,100],'color':'#1e0a0a'}],
                    'threshold': {'line': {'color': "#00ff88", 'width': 3},
                                  'thickness': 0.75, 'value': prob * 100}
                }
            ))
            fig_g1.update_layout(height=240, margin=dict(l=10,r=10,t=40,b=10), **PLOT_CFG)
            st.plotly_chart(fig_g1, use_container_width=True)

        with g2:
            fig_g2 = go.Figure(go.Indicator(
                mode="gauge+number", value=confidence,
                title={'text':"AI Confidence (%)",'font':{'family':'Space Mono','color':'#6b6558','size':11}},
                number={'font':{'family':'Space Mono','color':'#d4cfc8'},'suffix':'%'},
                gauge={
                    'axis':{'range':[0,100],'tickcolor':'#2a2820'},
                    'bar':{'color': AMBER},
                    'bgcolor':"rgba(0,0,0,0)",
                    'steps':[{'range':[0,40],'color':'#1e1800'},{'range':[40,100],'color':'#121318'}]
                }
            ))
            fig_g2.update_layout(height=240, margin=dict(l=10,r=10,t=40,b=10), **PLOT_CFG)
            st.plotly_chart(fig_g2, use_container_width=True)

        with g3:
            # Survival probability
            surv_prob = (1 - prob) * 100
            fig_g3 = go.Figure(go.Indicator(
                mode="gauge+number", value=surv_prob,
                title={'text':"Survival Probability (%)",'font':{'family':'Space Mono','color':'#6b6558','size':11}},
                number={'font':{'family':'Space Mono','color':'#d4cfc8'},'suffix':'%'},
                gauge={
                    'axis':{'range':[0,100],'tickcolor':'#2a2820'},
                    'bar':{'color': GREEN},
                    'bgcolor':"rgba(0,0,0,0)",
                    'steps':[{'range':[0,50],'color':'#1e0a0a'},{'range':[50,100],'color':'#0a1e0e'}]
                }
            ))
            fig_g3.update_layout(height=240, margin=dict(l=10,r=10,t=40,b=10), **PLOT_CFG)
            st.plotly_chart(fig_g3, use_container_width=True)

        # Radar chart
        st.markdown('<div class="sec-header">Risk Radar Profile</div>', unsafe_allow_html=True)
        cats = ["Funding Power","Team Strength","Market Opportunity","Competitive Pressure","Business Viability","Operational Maturity"]
        scores = [
            min(funding/5e6, 1)*10,

        ]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=scores + [scores[0]], theta=cats + [cats[0]],
            fill="toself", fillcolor=f"rgba(245,185,66,0.1)",
            line=dict(color=AMBER, width=2), name="Your Startup"
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[5]*len(cats) + [5], theta=cats + [cats[0]],
            fill="toself", fillcolor="rgba(90,158,214,0.05)",
            line=dict(color=BLUE, width=1, dash="dot"), name="Median Startup"
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(range=[0,10], gridcolor="#1f1e1a", tickfont=dict(family="Space Mono",size=8)),
                       angularaxis=dict(tickfont=dict(family="Space Mono", size=9), gridcolor="#1f1e1a")),
            height=380, margin=dict(l=40,r=40,t=20,b=20),
            legend=dict(font=dict(family="Space Mono",size=9)),
            **PLOT_CFG
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Recommendations
        st.markdown('<div class="sec-header">Strategic Recommendations</div>', unsafe_allow_html=True)

        rec_cols = st.columns(2)
        recs = []
        if funding < 500000:
            recs.append(("CRITICAL", "🏦 Raise more capital — funding below survival threshold for most markets."))
        # if burn_rate_in > 0.7:
        #     recs.append(("HIGH", "🔥 Burn rate is dangerously high — extend your runway immediately."))
        # if debt_ratio_in > 1.2:
        #     recs.append(("HIGH", "📉 Debt ratio exceeds healthy bounds — restructure liabilities."))
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
        if not recs:
            recs.append(("LOW", "✅ Strong startup profile across evaluated dimensions. Focus on execution."))

        for i, (tier_r, msg) in enumerate(recs):
            col = rec_cols[i % 2]
            color_map = {"CRITICAL": RED, "HIGH": ORANGE, "MEDIUM": AMBER, "LOW": GREEN}
            with col:
                st.markdown(f"""
                <div style='background:#121318; border:1px solid {color_map[tier_r]}33;
                            border-left:3px solid {color_map[tier_r]}; border-radius:0 6px 6px 0;
                            padding:12px 14px; margin-bottom:8px;'>
                    <div style='font-family:"Space Mono",monospace; font-size:9px; color:{color_map[tier_r]};
                                letter-spacing:2px; margin-bottom:4px;'>{tier_r}</div>
                    <div style='font-family:"DM Sans",sans-serif; font-size:13px; color:#d4cfc8;'>{msg}</div>
                </div>
                """, unsafe_allow_html=True)

        # Investor Decision
        st.markdown('<div class="sec-header">Investor Decision Framework</div>', unsafe_allow_html=True)
        if prob < 0.35:
            st.success("💼 STRONG BUY — Risk profile is well within acceptable investment parameters. High conviction opportunity.")
        elif prob < 0.55:
            st.warning("🤝 CONDITIONAL INVESTMENT — Moderate risk. Recommended: staged funding with milestone triggers.")
        elif prob < 0.75:
            st.error("⚠️ PASS — Risk-adjusted returns are unfavorable. Material issues need resolution before investment.")
        else:
            st.error("🚫 STRONG PASS — Critical failure indicators present. Investment not advisable at current trajectory.")

# ─────────────────────────────────────────────
# ██ ANALYTICS LAB
# ─────────────────────────────────────────────
elif selected == "Analytics Lab":

    st.markdown("""
    <div style='padding:8px 0 2px;'>
        <div style='font-family:Syne,sans-serif; font-size:30px; font-weight:800; color:#f0ebe3; letter-spacing:-1px;'>
            Analytics Lab
        </div>
        <div style='font-family:"Space Mono",monospace; font-size:9px; color:#3a3830; letter-spacing:3px; margin-top:4px;'>
            DEEP DATA EXPLORATION · PATTERN DISCOVERY · FAILURE DRIVERS
        </div>
    </div>
    <div class="amber-rule"></div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records",   f"{len(data):,}")
    c2.metric("Avg Funding",     f"${data.funding.mean()/1e6:.2f}M")
    c3.metric("Avg Burn Rate",   f"{data.burn_rate.mean():.2f}")
    c4.metric("Avg Rev Growth",  f"{data.revenue_growth.mean()*100:.1f}%")

    st.markdown('<div class="amber-rule"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="sec-header">Failure Rate by Team Experience</div>', unsafe_allow_html=True)
        te_f = data.groupby("team_experience")["failure"].mean().reset_index()
        fig_te = px.bar(te_f, x="team_experience", y="failure",
                        color="failure", color_continuous_scale=[[0,GREEN],[1,RED]],
                        text=te_f["failure"].apply(lambda x: f"{x*100:.0f}%"))
        fig_te.update_traces(textposition="outside", textfont=dict(family="Space Mono", size=10))
        fig_te.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=0),
                              coloraxis_showscale=False, yaxis_tickformat=".0%",
                              yaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
        st.plotly_chart(fig_te, use_container_width=True)

    with col_b:
        st.markdown('<div class="sec-header">Burn Rate vs Failure (Violin)</div>', unsafe_allow_html=True)
        fig_vio = go.Figure()
        for outcome, color, label in [(0, GREEN, "Survived"), (1, RED, "Failed")]:
            fig_vio.add_trace(go.Violin(
                y=data[data.failure==outcome].burn_rate, name=label,
                box_visible=True, meanline_visible=True,
                fillcolor=color, line_color=color,
                opacity=0.7
            ))
        fig_vio.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=0),
                               violingap=0.3, yaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
        st.plotly_chart(fig_vio, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown('<div class="sec-header">Revenue Growth Distribution</div>', unsafe_allow_html=True)
        fig_rg = go.Figure()
        for outcome, color, label in [(0, GREEN, "Survived"), (1, RED, "Failed")]:
            fig_rg.add_trace(go.Histogram(
                x=data[data.failure==outcome].revenue_growth, name=label,
                marker_color=color, opacity=0.7, nbinsx=30
            ))
        fig_rg.update_layout(barmode="overlay", height=280, margin=dict(l=0,r=0,t=10,b=0),
                              xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"),
                              legend=dict(font=dict(family="Space Mono",size=9)), **PLOT_CFG)
        st.plotly_chart(fig_rg, use_container_width=True)

    with col_d:
        st.markdown('<div class="sec-header">Debt Ratio vs Revenue Growth</div>', unsafe_allow_html=True)
        samp = data.sample(500, random_state=3)
        fig_dr = px.scatter(samp, x="debt_ratio", y="revenue_growth",
                             color=samp.failure.map({0:"Survived",1:"Failed"}),
                             color_discrete_map={"Survived":GREEN,"Failed":RED}, opacity=0.6)
        fig_dr.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=0),
                              xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"),
                              legend=dict(font=dict(family="Space Mono",size=9)), **PLOT_CFG)
        st.plotly_chart(fig_dr, use_container_width=True)

    st.markdown('<div class="sec-header">Correlation Heatmap</div>', unsafe_allow_html=True)
    corr = data.corr()
    fig_h = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                       aspect="auto", zmin=-1, zmax=1)
    fig_h.update_layout(height=420, margin=dict(l=0,r=0,t=20,b=0), **PLOT_CFG)
    st.plotly_chart(fig_h, use_container_width=True)

    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown('<div class="sec-header">Failure by Years Operating</div>', unsafe_allow_html=True)
        yo_f = data.groupby("years_operating")["failure"].mean().reset_index()
        fig_yo = px.area(yo_f, x="years_operating", y="failure",
                          color_discrete_sequence=[AMBER])
        fig_yo.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=0),
                              yaxis_tickformat=".0%",
                              xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
        st.plotly_chart(fig_yo, use_container_width=True)

    with col_f:
        st.markdown('<div class="sec-header">Business Model Strength vs Failure</div>', unsafe_allow_html=True)
        bm_f = data.groupby("business_model")["failure"].mean().reset_index()
        fig_bm = px.line(bm_f, x="business_model", y="failure",
                          markers=True, color_discrete_sequence=[PURPLE])
        fig_bm.update_layout(height=280, margin=dict(l=0,r=0,t=10,b=0),
                              yaxis_tickformat=".0%",
                              xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
        st.plotly_chart(fig_bm, use_container_width=True)

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
        fig_roc2.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name=f"AUC={auc(fpr,tpr):.3f}",
                                       line=dict(color=AMBER, width=2.5)))
        fig_roc2.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Baseline",
                                       line=dict(color="#3a3830", dash="dash", width=1)))
        fig_roc2.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                                xaxis_title="FPR", yaxis_title="TPR",
                                xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"),
                                legend=dict(font=dict(family="Space Mono",size=9)), **PLOT_CFG)
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
        comp_df = pd.DataFrame({
            "Model": ["Logistic Regression","Random Forest","Gradient Boost"],
            "Accuracy": [lr_acc*100, rf_acc*100, gb_acc*100],
            "Best": ["✓" if best_name=="Logistic Regression" else "",
                     "✓" if best_name=="Random Forest" else "",
                     "✓" if best_name=="Gradient Boost" else ""]
        })
        fig_comp = go.Figure(go.Bar(
            x=comp_df.Model, y=comp_df.Accuracy,
            marker_color=[AMBER if b=="✓" else "#2a2820" for b in comp_df.Best],
            text=[f"{v:.2f}%" for v in comp_df.Accuracy], textposition="outside",
            textfont=dict(family="Space Mono", size=11)
        ))
        fig_comp.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0),
                                yaxis=dict(range=[80,100],gridcolor="#1f1e1a"),
                                xaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
        st.plotly_chart(fig_comp, use_container_width=True)

# ─────────────────────────────────────────────
# ██ MY PROFILE
# ─────────────────────────────────────────────
elif selected == "My Profile":

    act = pd.read_csv("activity.csv")
    user_d = act[act.username == st.session_state.username].copy()

    st.markdown(f"""
    <div style='padding:8px 0 2px;'>
        <div style='font-family:Syne,sans-serif; font-size:30px; font-weight:800; color:#f0ebe3; letter-spacing:-1px;'>
            {st.session_state.username}
        </div>
        <div style='font-family:"Space Mono",monospace; font-size:9px; color:#3a3830; letter-spacing:3px; margin-top:4px;'>
            ANALYST PROFILE · EVALUATION HISTORY · PERFORMANCE METRICS
        </div>
    </div>
    <div class="amber-rule"></div>
    """, unsafe_allow_html=True)

    if not user_d.empty:
        avg_fp = user_d.failure_prob.mean()
        best_fp= user_d.failure_prob.min()
        worst_fp= user_d.failure_prob.max()
        total  = len(user_d)
        high_r = (user_d.failure_prob >= 0.55).sum()

        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Total Evaluations", total)
        c2.metric("Avg Risk Score", f"{avg_fp*100:.1f}%")
        c3.metric("Best Case", f"{best_fp*100:.1f}%")
        c4.metric("Worst Case", f"{worst_fp*100:.1f}%")
        c5.metric("High Risk Cases", int(high_r))

        st.markdown('<div class="amber-rule"></div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="sec-header">Risk Distribution</div>', unsafe_allow_html=True)
            tier_counts = user_d["risk_tier"].value_counts().reset_index()
            tier_counts.columns = ["Tier", "Count"]
            colors_map = {"CRITICAL": RED, "HIGH": ORANGE, "MEDIUM": AMBER, "LOW": GREEN}
            fig_tier = px.pie(tier_counts, values="Count", names="Tier", hole=0.55,
                               color="Tier", color_discrete_map=colors_map)
            fig_tier.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                                    legend=dict(font=dict(family="Space Mono",size=9)), **PLOT_CFG)
            st.plotly_chart(fig_tier, use_container_width=True)

        with col_b:
            st.markdown('<div class="sec-header">Failure Risk Over Time</div>', unsafe_allow_html=True)
            user_d = user_d.reset_index(drop=True)
            user_d["Run"] = range(1, len(user_d)+1)
            fig_trend = px.line(user_d, x="Run", y="failure_prob",
                                 markers=True, color_discrete_sequence=[AMBER])
            fig_trend.add_hline(y=0.5, line_dash="dot", line_color=RED,
                                 annotation_text="Failure Threshold",
                                 annotation_font=dict(family="Space Mono",size=9))
            fig_trend.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0),
                                     yaxis_tickformat=".0%",
                                     xaxis=dict(gridcolor="#1f1e1a"), yaxis=dict(gridcolor="#1f1e1a"), **PLOT_CFG)
            st.plotly_chart(fig_trend, use_container_width=True)

        # Achievement
        st.markdown('<div class="sec-header">Analyst Rank</div>', unsafe_allow_html=True)
        if total >= 20 and avg_fp < 0.4:
            badge, label, color = "🏆", "SENIOR RISK ANALYST", AMBER
        elif total >= 10:
            badge, label, color = "🎖️", "RISK ANALYST", BLUE
        elif total >= 5:
            badge, label, color = "📊", "JUNIOR ANALYST", GREEN
        else:
            badge, label, color = "🔍", "TRAINEE ANALYST", "#6b6558"

        st.markdown(f"""
        <div style='background:#121318; border:1px solid {color}33; border-radius:10px;
                    padding:24px; text-align:center;'>
            <div style='font-size:42px;'>{badge}</div>
            <div style='font-family:Syne,sans-serif; font-size:18px; font-weight:800;
                        color:{color}; letter-spacing:-0.5px; margin-top:8px;'>{label}</div>
            <div style='font-family:"Space Mono",monospace; font-size:10px; color:#3a3830;
                        letter-spacing:2px; margin-top:6px;'>
                {total} EVALUATIONS · AVG RISK SCORE: {avg_fp*100:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="amber-rule"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-header">Recent Evaluation History</div>', unsafe_allow_html=True)
        display_cols = ["date","time","funding","failure_prob","risk_tier"]
        st.dataframe(user_d[display_cols].tail(15).sort_values("date", ascending=False),
                     use_container_width=True)
        st.download_button("📥 Export Full History", user_d.to_csv(index=False), "my_evaluation_history.csv")
    else:
        st.info("No evaluations yet — head to **Risk Evaluator** to get started!")

# ─────────────────────────────────────────────
# ██ AI ASSISTANT
# ─────────────────────────────────────────────
elif selected == "AI Assistant":

    st.markdown("""
    <div style='padding:8px 0 2px;'>
        <div style='font-family:Syne,sans-serif; font-size:30px; font-weight:800; color:#f0ebe3; letter-spacing:-1px;'>
            AI Data Assistant
        </div>
        <div style='font-family:"Space Mono",monospace; font-size:9px; color:#3a3830; letter-spacing:3px; margin-top:4px;'>
            NATURAL LANGUAGE QUERIES · INSTANT ANALYTICS · DATA INTELLIGENCE
        </div>
    </div>
    <div class="amber-rule"></div>
    """, unsafe_allow_html=True)

    # Quick action chips
    st.markdown('<div class="sec-header">Quick Queries</div>', unsafe_allow_html=True)
    chip_cols = st.columns(5)
    chips = ["total startups", "success rate", "average funding", "top risk factors", "burn rate analysis"]
    for i, chip in enumerate(chips):
        with chip_cols[i]:
            if st.button(chip.upper(), use_container_width=True):
                st.session_state["qa_input"] = chip

    q_input = st.text_input("💬 Ask about the dataset...",
                             value=st.session_state.get("qa_input",""),
                             placeholder="e.g. 'what is the average burn rate of failed startups?'")

    if q_input:
        q = q_input.lower()

        if any(k in q for k in ["total", "count", "how many"]):
            st.success(f"📊 Total startups in dataset: **{len(data):,}**")
            fig = px.histogram(data, x="failure", color=data.failure.map({0:"Survived",1:"Failed"}),
                                color_discrete_map={"Survived":GREEN,"Failed":RED},
                                title="Failure vs Survival Distribution")
            fig.update_layout(**PLOT_CFG, margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig, use_container_width=True)

        elif any(k in q for k in ["success rate", "survival", "fail rate", "failure rate"]):
            rate = (1 - data.failure.mean()) * 100
            st.success(f"✅ Startup survival rate: **{rate:.1f}%** | Failure rate: **{100-rate:.1f}%**")
            fig = px.pie(names=["Survived","Failed"],
                          values=[data[data.failure==0].shape[0], data[data.failure==1].shape[0]],
                          hole=0.55, color_discrete_sequence=[GREEN, RED])
            fig.update_layout(**PLOT_CFG, margin=dict(l=0,r=0,t=10,b=0))
            st.plotly_chart(fig, use_container_width=True)

        elif "funding" in q:
            avg = data.funding.mean()
            med = data.funding.median()
            st.success(f"💰 Average funding: **${avg:,.0f}** | Median: **${med:,.0f}**")
            fig = px.histogram(data, x="funding", nbins=40, color_discrete_sequence=[AMBER],
                                title="Funding Distribution")
            fig.update_layout(**PLOT_CFG, margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig, use_container_width=True)

        elif any(k in q for k in ["burn rate", "burn"]):
            st.success(f"🔥 Failed startups avg burn rate: **{data[data.failure==1].burn_rate.mean():.3f}** | "
                       f"Survived: **{data[data.failure==0].burn_rate.mean():.3f}**")
            fig = go.Figure()
            for outcome, color, label in [(0,GREEN,"Survived"),(1,RED,"Failed")]:
                fig.add_trace(go.Histogram(x=data[data.failure==outcome].burn_rate,
                                            name=label, marker_color=color, opacity=0.7, nbinsx=30))
            fig.update_layout(barmode="overlay", title="Burn Rate Distribution",
                               **PLOT_CFG, margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig, use_container_width=True)

        elif any(k in q for k in ["risk factor", "important", "top factor", "key driver"]):
            fi = pd.DataFrame({"Feature":FEATURES,"Importance":rf_m.feature_importances_}).sort_values("Importance",ascending=False)
            st.success(f"🏆 Top risk factor: **{fi.iloc[0].Feature}** (importance: {fi.iloc[0].Importance:.3f})")
            fig = px.bar(fi.head(5), x="Feature", y="Importance",
                          color="Importance", color_continuous_scale=[[0,"#1f1e1a"],[1,AMBER]],
                          title="Top 5 Risk Factors")
            fig.update_layout(**PLOT_CFG, coloraxis_showscale=False, margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig, use_container_width=True)

        elif any(k in q for k in ["team", "experience"]):
            avg_team = data.team_experience.mean()
            st.success(f"👥 Average team experience: **{avg_team:.1f}/10**")
            tf = data.groupby("team_experience")["failure"].mean().reset_index()
            fig = px.bar(tf, x="team_experience", y="failure",
                          color="failure", color_continuous_scale=[[0,GREEN],[1,RED]],
                          title="Team Experience vs Failure Rate")
            fig.update_layout(**PLOT_CFG, coloraxis_showscale=False, yaxis_tickformat=".0%",
                               margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig, use_container_width=True)

        elif any(k in q for k in ["debt", "leverage"]):
            st.success(f"🏦 Failed startups avg debt ratio: **{data[data.failure==1].debt_ratio.mean():.2f}** | "
                       f"Survived: **{data[data.failure==0].debt_ratio.mean():.2f}**")
            fig = px.box(data, x=data.failure.map({0:"Survived",1:"Failed"}), y="debt_ratio",
                          color=data.failure.map({0:"Survived",1:"Failed"}),
                          color_discrete_map={"Survived":GREEN,"Failed":RED},
                          title="Debt Ratio by Outcome")
            fig.update_layout(**PLOT_CFG, margin=dict(l=0,r=0,t=40,b=0), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        elif any(k in q for k in ["revenue", "growth"]):
            st.success(f"📈 Failed startups avg revenue growth: **{data[data.failure==1].revenue_growth.mean()*100:.1f}%** | "
                       f"Survived: **{data[data.failure==0].revenue_growth.mean()*100:.1f}%**")
            fig = px.histogram(data, x="revenue_growth",
                                color=data.failure.map({0:"Survived",1:"Failed"}),
                                color_discrete_map={"Survived":GREEN,"Failed":RED},
                                nbins=40, barmode="overlay", title="Revenue Growth Distribution")
            fig.update_layout(**PLOT_CFG, margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig, use_container_width=True)

        elif any(k in q for k in ["competition", "compete"]):
            cf = data.groupby("competition")["failure"].mean().reset_index()
            st.success(f"⚔️ Highest failure rate at competition level: **{cf.loc[cf.failure.idxmax(),'competition']}**")
            fig = px.line(cf, x="competition", y="failure", markers=True,
                           color_discrete_sequence=[RED], title="Competition Level vs Failure Rate")
            fig.update_layout(**PLOT_CFG, yaxis_tickformat=".0%", margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("🤖 Try asking about: **total startups, failure rate, funding, burn rate, team experience, debt ratio, revenue growth, competition, top risk factors**")
            st.markdown("""
            <div style='background:#121318; border:1px solid #2a2820; border-radius:8px; padding:16px 18px; margin-top:8px;'>
                <div style='font-family:"Space Mono",monospace; font-size:10px; color:#6b6558; letter-spacing:2px; margin-bottom:10px;'>SAMPLE QUERIES</div>
                <div style='font-family:"DM Sans",sans-serif; font-size:13px; color:#d4cfc8; line-height:2;'>
                    • "What is the average funding of failed startups?"<br>
                    • "Show me burn rate analysis"<br>
                    • "What are the top risk factors?"<br>
                    • "How does competition affect failure?"<br>
                    • "What is the survival rate?"
                </div>
            </div>
            """, unsafe_allow_html=True)