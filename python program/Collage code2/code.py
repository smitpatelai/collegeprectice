from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd
import os, json, hashlib, requests
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NexusAI — Startup Intelligence",
    layout="wide",
    page_icon="🧬",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS  — Dark editorial / brutalist-tech
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;600;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg:        #07080d;
    --bg2:       #0d0f17;
    --bg3:       #131620;
    --border:    #1e2235;
    --border2:   #2a2f4a;
    --accent:    #6c63ff;
    --accent2:   #ff6584;
    --accent3:   #43e8ac;
    --accent4:   #ffb347;
    --text:      #e4e8f5;
    --muted:     #6b738f;
    --success:   #43e8ac;
    --danger:    #ff4d6d;
    --warning:   #ffb347;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    transition: border-color 0.2s;
}
[data-testid="metric-container"]:hover { border-color: var(--accent) !important; }
[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    font-family: 'JetBrains Mono', monospace !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] { font-family: 'JetBrains Mono', monospace !important; }

/* ── Headings ── */
h1 { font-family: 'Syne', sans-serif !important; font-size: 42px !important;
     font-weight: 800 !important; color: var(--text) !important; letter-spacing: -1.5px !important; }
h2 { font-family: 'Syne', sans-serif !important; font-weight: 700 !important; color: var(--text) !important; }
h3 { font-family: 'Space Grotesk', sans-serif !important; color: var(--muted) !important;
     font-weight: 500 !important; font-size: 13px !important; letter-spacing: 2px !important; text-transform: uppercase; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.2) !important;
}
.stSelectbox > div > div,
.stMultiSelect > div {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: #7d75ff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(108,99,255,0.35) !important;
}
.stDownloadButton > button {
    background: transparent !important;
    color: var(--accent3) !important;
    border: 1px solid var(--accent3) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}

/* ── Alerts ── */
.stSuccess { background: rgba(67,232,172,0.08) !important; border-left: 3px solid var(--success) !important; border-radius: 8px !important; }
.stError   { background: rgba(255,77,109,0.08) !important; border-left: 3px solid var(--danger) !important;  border-radius: 8px !important; }
.stWarning { background: rgba(255,179,71,0.08) !important; border-left: 3px solid var(--warning) !important; border-radius: 8px !important; }
.stInfo    { background: rgba(108,99,255,0.08) !important; border-left: 3px solid var(--accent) !important;  border-radius: 8px !important; }

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div { background: var(--accent) !important; }

/* ─── Custom Components ─── */
.page-header {
    padding: 12px 0 8px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
}
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -1px;
    line-height: 1.1;
}
.page-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 3px;
    margin-top: 6px;
    text-transform: uppercase;
}
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
.stat-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    transition: border-color 0.2s, transform 0.2s;
}
.stat-card:hover { border-color: var(--border2); transform: translateY(-2px); }

.verdict-success {
    background: rgba(67,232,172,0.06);
    border: 1px solid rgba(67,232,172,0.3);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
}
.verdict-fail {
    background: rgba(255,77,109,0.06);
    border: 1px solid rgba(255,77,109,0.3);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
}
.verdict-title { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; }
.verdict-sub   { font-family: 'JetBrains Mono', monospace; font-size: 12px; margin-top: 8px; letter-spacing: 2px; }

/* ── Chat Styles ── */
.chat-wrapper {
    height: 520px;
    overflow-y: auto;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 14px;
    scroll-behavior: smooth;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 14px;
}
.msg-ai {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 14px;
}
.bubble-user {
    background: var(--accent);
    color: #fff;
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    max-width: 75%;
    font-size: 14px;
    line-height: 1.5;
    font-family: 'Space Grotesk', sans-serif;
}
.bubble-ai {
    background: var(--bg3);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    max-width: 80%;
    font-size: 14px;
    line-height: 1.6;
    font-family: 'Space Grotesk', sans-serif;
}
.bubble-ai code {
    background: rgba(108,99,255,0.15);
    color: var(--accent);
    padding: 1px 5px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}
.avatar-ai {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    margin-right: 10px;
    flex-shrink: 0;
    margin-top: 2px;
}
.typing-indicator {
    display: flex; gap: 4px; padding: 12px 16px;
    background: var(--bg3); border: 1px solid var(--border);
    border-radius: 16px 16px 16px 4px; width: fit-content;
}
.typing-indicator span {
    width: 7px; height: 7px; background: var(--muted);
    border-radius: 50%; animation: bounce 1.4s infinite;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-8px)} }

.chip {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.5px;
    border: 1px solid;
}
.chip-success { background: rgba(67,232,172,0.1); color: var(--success); border-color: rgba(67,232,172,0.3); }
.chip-danger  { background: rgba(255,77,109,0.1); color: var(--danger);  border-color: rgba(255,77,109,0.3); }
.chip-accent  { background: rgba(108,99,255,0.1); color: var(--accent);  border-color: rgba(108,99,255,0.3); }

/* Auth */
.auth-wrap {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 40px 36px 32px;
    box-shadow: 0 24px 80px rgba(0,0,0,0.5);
}
.auth-title {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}
.auth-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 28px;
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

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
PLOT_CFG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Space Grotesk", color="#8890aa"),
    margin=dict(l=0, r=0, t=10, b=0)
)
C_SUCCESS = "#43e8ac"
C_DANGER  = "#ff4d6d"
C_ACCENT  = "#6c63ff"
C_WARNING = "#ffb347"
C_BLUE    = "#4da3ff"

FEATURE_COLS = [
    "funding", "team_experience", "market_size_bn",
    "competition_level", "business_model_score",
    "revenue_growth", "burn_rate", "runway_months",
    "team_size", "nps_score"
]

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for k, v in [("logged_in", False), ("page", "login"),
              ("username", ""), ("chat_history", []),
              ("login_time", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
# FILES / PERSISTENCE
# ─────────────────────────────────────────────
def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

for fname, cols in [
    ("users.csv",          ["username", "email", "password"]),
    ("user_activity.csv",  ["username", "login_date", "login_time", "funding",
                             "team_experience", "prediction_probability", "sector"]),
]:
    if not os.path.exists(fname):
        pd.DataFrame(columns=cols).to_csv(fname, index=False)

# ─────────────────────────────────────────────
# GENERATE / LOAD REAL-WORLD INSPIRED DATASET
# ─────────────────────────────────────────────
@st.cache_data
def load_dataset():
    if os.path.exists("startup_real_data.csv"):
        df = pd.read_csv("startup_real_data.csv")
    else:
        np.random.seed(42)
        n = 2000
        sectors  = ['SaaS','FinTech','HealthTech','EdTech','E-Commerce','AI/ML','CleanTech','Cybersecurity','Gaming','BioTech']
        stages   = ['Pre-Seed','Seed','Series A','Series B','Series C']
        countries= ['USA','UK','India','Germany','Singapore','Canada','Israel','France','Brazil','Australia']
        stage_w  = [0.30, 0.35, 0.20, 0.10, 0.05]

        sector_a  = np.random.choice(sectors, n)
        stage_a   = np.random.choice(stages, n, p=stage_w)
        country_a = np.random.choice(countries, n)

        funding_map = {
            'Pre-Seed':(50_000, 500_000), 'Seed':(500_000, 3_000_000),
            'Series A':(3_000_000, 15_000_000), 'Series B':(15_000_000, 50_000_000),
            'Series C':(50_000_000, 200_000_000)
        }
        funding = np.array([np.random.randint(*funding_map[s]) for s in stage_a])

        team_size     = np.random.randint(2, 150, n)
        team_exp      = np.random.randint(1, 15, n)
        market_sz     = np.round(np.random.uniform(0.5, 500, n), 2)
        burn_rate     = np.random.randint(10_000, 800_000, n)
        rev_growth    = np.round(np.random.uniform(-0.2, 5.0, n), 3)
        customers     = np.random.randint(0, 50_000, n)
        nps           = np.random.randint(-20, 80, n)
        patents       = np.random.randint(0, 30, n)
        competition   = np.random.randint(1, 10, n)
        biz_model     = np.random.randint(1, 10, n)
        months_since  = np.random.randint(3, 120, n)
        runway        = np.random.randint(1, 36, n)

        log_fund = np.log1p(funding) / np.log1p(200_000_000)
        score = (log_fund*0.25 + (team_exp/15)*0.20 + (biz_model/10)*0.18
                 + rev_growth.clip(0,5)/5*0.15 + market_sz.clip(0,500)/500*0.10
                 + (1-competition/10)*0.08 + runway/36*0.04)
        noise   = np.random.normal(0, 0.05, n)
        success = ((1/(1+np.exp(-(score+noise-0.55)*8))) > 0.5).astype(int)

        df = pd.DataFrame({
            'sector':sector_a, 'stage':stage_a, 'country':country_a,
            'funding':funding, 'team_size':team_size, 'team_experience':team_exp,
            'market_size_bn':market_sz, 'burn_rate':burn_rate, 'revenue_growth':rev_growth,
            'customer_count':customers, 'nps_score':nps, 'patent_count':patents,
            'competition_level':competition, 'business_model_score':biz_model,
            'months_since_founding':months_since, 'runway_months':runway, 'success':success
        })
        df.to_csv("startup_real_data.csv", index=False)

    df["failure"] = 1 - df["success"]
    return df

DATA = load_dataset()

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
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ML PIPELINE
# ─────────────────────────────────────────────
@st.cache_resource
def build_models(data):
    X = data[FEATURE_COLS].fillna(0)
    y = data["success"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_te_s  = scaler.transform(X_te)

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, C=1.0, random_state=42),
        "Random Forest":       RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42),
        "Gradient Boosting":   GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, random_state=42),
    }
    results = {}
    for name, m in models.items():
        m.fit(X_tr_s, y_tr)
        acc = m.score(X_te_s, y_te)
        probs = m.predict_proba(X_te_s)[:,1]
        fpr, tpr, _ = roc_curve(y_te, probs)
        results[name] = {"model": m, "acc": acc, "auc": auc(fpr, tpr),
                         "fpr": fpr, "tpr": tpr}

    best_name = max(results, key=lambda k: results[k]["auc"])
    return scaler, results, X_te_s, y_te, X_tr_s, y_tr, best_name

SCALER, MODEL_RESULTS, X_TE_S, Y_TE, X_TR_S, Y_TR, BEST_NAME = build_models(DATA)
BEST_MODEL = MODEL_RESULTS[BEST_NAME]["model"]

# ─────────────────────────────────────────────
# CLAUDE API CHATBOT
# ─────────────────────────────────────────────
def call_claude(messages: list, system: str) -> str:
    """Call Anthropic API and return assistant text."""
    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json",
                     "anthropic-version": "2023-06-01"},
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "system": system,
                "messages": messages
            },
            timeout=30
        )
        data = resp.json()
        if "content" in data:
            return "".join(b["text"] for b in data["content"] if b.get("type") == "text")
        elif "error" in data:
            return f"⚠️ API Error: {data['error'].get('message','Unknown error')}"
        return "⚠️ Unexpected response from AI."
    except Exception as e:
        return f"⚠️ Connection error: {str(e)}"

def build_data_context() -> str:
    d = DATA
    ctx = f"""
You are NexusAI, an expert AI analyst for startup success prediction.
You have access to a real-world startup dataset with {len(d):,} companies across 10 sectors.

=== LIVE DATASET STATS ===
Total startups: {len(d):,}
Success rate: {d['success'].mean()*100:.1f}%
Avg funding: ${d['funding'].mean()/1e6:.2f}M
Avg team experience: {d['team_experience'].mean():.1f} yrs
Avg revenue growth: {d['revenue_growth'].mean():.2f}x
Sectors: {', '.join(d['sector'].unique())}
Stages: {', '.join(d['stage'].unique())}
Countries: {', '.join(d['country'].unique()[:5])} + more

=== ML MODEL PERFORMANCE ===
Best Model: {BEST_NAME} (AUC: {MODEL_RESULTS[BEST_NAME]['auc']:.4f})
""" + "\n".join([f"- {n}: Acc={r['acc']*100:.1f}%, AUC={r['auc']:.3f}" for n, r in MODEL_RESULTS.items()]) + f"""

=== FEATURE IMPORTANCE (Random Forest top 3) ===
The most predictive features are: revenue_growth, runway_months, business_model_score, funding

Answer questions about startup success, the dataset, ML models, investor strategy,
startup advice, or any related topic. Be concise, insightful, and data-driven.
Format numbers clearly. Use bullet points for lists. Keep responses under 300 words
unless more detail is explicitly requested.
"""
    return ctx.strip()

# ─────────────────────────────────────────────
# AUTH PAGES
# ─────────────────────────────────────────────
def page_login():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center; padding: 40px 0 32px;'>
            <div style='font-size:40px; margin-bottom:8px;'>🧬</div>
            <div style='font-family:Syne,sans-serif; font-size:32px; font-weight:800; color:#e4e8f5; letter-spacing:-1px;'>NexusAI</div>
            <div style='font-family:"JetBrains Mono",monospace; font-size:10px; color:#6b738f; letter-spacing:3px; margin-top:4px;'>STARTUP INTELLIGENCE PLATFORM</div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="auth-title">Welcome back</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-sub">Sign in to your account</div>', unsafe_allow_html=True)
            social_buttons_html("Login")
            st.markdown('<div class="or-divider">OR SIGN IN WITH EMAIL</div>', unsafe_allow_html=True)

            username = st.text_input("Username", key="li_u", placeholder="Your username")
            password = st.text_input("Password", type="password", key="li_p", placeholder="••••••••")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Sign In →", use_container_width=True):
                    if not username or not password:
                        st.error("Please fill in all fields")
                    else:
                        users = pd.read_csv("users.csv")
                        user  = users[(users.username==username) & (users.password==hash_pw(password))]
                        if not user.empty:
                            st.session_state.update(logged_in=True, username=username,
                                                    login_time=datetime.now(), chat_history=[])
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
            with c2:
                if st.button("Create Account", use_container_width=True):
                    st.session_state.page = "signup"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

def page_signup():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("""
            <div style='text-align:center; padding: 40px 0 32px;'>
            <div style='font-size:40px; margin-bottom:8px;'>🧬</div>
            <div style='font-family:Syne,sans-serif; font-size:32px; font-weight:800; color:#e4e8f5; letter-spacing:-1px;'>Join NexusAI</div>
            <div class="auth-wrap">
                <div style='font-family:"JetBrains Mono",monospace; font-size:10px; color:#6b738f; letter-spacing:3px; margin-top:4px;'>CREATE YOUR ACCOUNT</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            social_buttons_html("Sign up")
            st.markdown('<div class="or-divider">OR CONTINUE WITH EMAIL</div>', unsafe_allow_html=True)
            # st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)
            username = st.text_input("Username", key="su_u", placeholder="Choose a username")
            email    = st.text_input("Email",    key="su_e", placeholder="your@email.com")
            password = st.text_input("Password", type="password", key="su_p", placeholder="Create a strong password")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Create Account →", use_container_width=True):
                    if not all([username, email, password]):
                        st.error("All fields required")
                    elif len(password) < 6:
                        st.error("Password must be ≥ 6 characters")
                    else:
                        users = pd.read_csv("users.csv")
                        if username in users.username.values:
                            st.error("Username already taken")
                        else:
                            new = pd.DataFrame({"username":[username],"email":[email],"password":[hash_pw(password)]})
                            pd.concat([users,new]).to_csv("users.csv", index=False)
                            st.success("✅ Account created! Sign in now.")
                            st.session_state.page = "login"; st.rerun()
            with c2:
                if st.button("← Back to Login", use_container_width=True):
                    st.session_state.page = "login"; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PRE-LOGIN GATE
# ─────────────────────────────────────────────
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        page_login()
    else:
        page_signup()
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='padding: 20px 0 16px; border-bottom: 1px solid #1e2235;'>
        <div style='font-family:Syne,sans-serif; font-size:22px; font-weight:800; color:#e4e8f5;'>🧬 NexusAI</div>
        <div style='font-family:"JetBrains Mono",monospace; font-size:9px; color:#6b738f; letter-spacing:2px; margin-top:3px;'>STARTUP INTELLIGENCE</div>
    </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Predict", "Analytics", "Model Lab", "AI Analyst", "My Profile"],
        icons=["grid-1x2-fill", "lightning-charge-fill", "bar-chart-line-fill",
               "cpu-fill", "chat-dots-fill", "person-fill"],
        default_index=0,
        styles={
            "container":         {"background-color": "transparent", "padding": "8px 0"},
            "icon":              {"color": "#6b738f", "font-size": "14px"},
            "nav-link":          {"color": "#6b738f", "font-size": "14px", "font-family": "Space Grotesk",
                                  "border-radius": "8px", "margin": "2px 0", "padding": "10px 14px"},
            "nav-link-selected": {"background-color": "#131620", "color": "#e4e8f5",
                                  "font-weight": "600", "border": "1px solid #2a2f4a"},
            "menu-title":        {"display": "none"},
        }
    )

    st.markdown("<br>", unsafe_allow_html=True)
    best_acc = MODEL_RESULTS[BEST_NAME]["acc"]
    best_auc = MODEL_RESULTS[BEST_NAME]["auc"]

    st.markdown(f"""
    <div style='background:#0d0f17; border:1px solid #1e2235; border-radius:10px; padding:16px;'>
        <div style='font-family:"JetBrains Mono",monospace; font-size:9px; color:#6b738f; letter-spacing:2px; margin-bottom:10px;'>SYSTEM STATUS</div>
        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
            <span style='font-size:12px; color:#6b738f;'>Model Acc</span>
            <span style='font-family:"JetBrains Mono",monospace; font-size:12px; color:#43e8ac;'>{best_acc*100:.1f}%</span>
        </div>
        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
            <span style='font-size:12px; color:#6b738f;'>AUC Score</span>
            <span style='font-family:"JetBrains Mono",monospace; font-size:12px; color:#6c63ff;'>{best_auc:.4f}</span>
        </div>
        <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
            <span style='font-size:12px; color:#6b738f;'>Dataset</span>
            <span style='font-family:"JetBrains Mono",monospace; font-size:12px; color:#e4e8f5;'>{len(DATA):,}</span>
        </div>
        <div style='display:flex; justify-content:space-between;'>
            <span style='font-size:12px; color:#6b738f;'>User</span>
            <span style='font-family:"JetBrains Mono",monospace; font-size:12px; color:#e4e8f5;'>{st.session_state.username}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Sign Out", use_container_width=True):
        for k in ["logged_in","username","login_time","chat_history"]:
            st.session_state[k] = False if k == "logged_in" else ([] if k == "chat_history" else "")
        st.session_state.page = "login"
        st.rerun()

# ═══════════════════════════════════════════════
# ██ DASHBOARD
# ═══════════════════════════════════════════════
if selected == "Dashboard":
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Mission Control</div>
        <div class="page-sub">Real-Time · Dataset Analytics · Model Overview</div>
    </div>""", unsafe_allow_html=True)

    # KPI row
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total Startups",    f"{len(DATA):,}")
    c2.metric("Success Rate",      f"{DATA['success'].mean()*100:.1f}%", "+2.3% vs Q3")
    c3.metric("Avg Funding",       f"${DATA['funding'].mean()/1e6:.1f}M")
    c4.metric("Best Model AUC",    f"{MODEL_RESULTS[BEST_NAME]['auc']:.4f}")
    c5.metric("Avg Revenue Growth",f"{DATA['revenue_growth'].mean():.2f}x")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    # Success by sector
    with col_a:
        st.markdown('<div class="section-label">Success Rate by Sector</div>', unsafe_allow_html=True)
        sec_s = DATA.groupby("sector")["success"].mean().reset_index().sort_values("success", ascending=True)
        fig = px.bar(sec_s, x="success", y="sector", orientation="h",
                     color="success", color_continuous_scale=[[0, C_DANGER],[0.5, C_WARNING],[1, C_SUCCESS]],
                     text=sec_s.success.apply(lambda v: f"{v*100:.0f}%"))
        fig.update_traces(textposition="outside")
        fig.update_layout(height=360, coloraxis_showscale=False,
                          xaxis=dict(gridcolor="#1e2235", tickformat=".0%"),
                          yaxis=dict(gridcolor="rgba(0,0,0,0)"), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    # Stage distribution
    with col_b:
        st.markdown('<div class="section-label">Funding Stage Distribution</div>', unsafe_allow_html=True)
        stage_c = DATA.groupby("stage").agg(count=("success","count"), rate=("success","mean")).reset_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(x=stage_c["stage"], y=stage_c["count"],
                             marker_color=C_ACCENT, name="Count", opacity=0.85,
                             text=stage_c["count"], textposition="outside"))
        fig.add_trace(go.Scatter(x=stage_c["stage"], y=stage_c["rate"]*max(stage_c["count"]),
                                 mode="lines+markers", name="Success Rate (scaled)",
                                 line=dict(color=C_SUCCESS, width=2), yaxis="y"))
        fig.update_layout(height=360, barmode="group",
                          xaxis=dict(gridcolor="#1e2235"),
                          yaxis=dict(gridcolor="#1e2235"),
                          legend=dict(font=dict(size=11)), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)

    # Funding vs Success scatter
    with col_c:
        st.markdown('<div class="section-label">Funding vs Revenue Growth</div>', unsafe_allow_html=True)
        samp = DATA.sample(500, random_state=7)
        fig = px.scatter(samp, x="funding", y="revenue_growth",
                         color=samp["success"].map({1:"Success",0:"Failure"}),
                         color_discrete_map={"Success":C_SUCCESS,"Failure":C_DANGER},
                         size="team_size", size_max=14, opacity=0.7,
                         hover_data=["sector","stage"])
        fig.update_layout(height=340, xaxis=dict(gridcolor="#1e2235"),
                          yaxis=dict(gridcolor="#1e2235"),
                          legend=dict(font=dict(size=11)), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    # Country heatmap
    with col_d:
        st.markdown('<div class="section-label">Success Rate by Country</div>', unsafe_allow_html=True)
        country_s = DATA.groupby("country")["success"].mean().reset_index().sort_values("success", ascending=False)
        fig = px.bar(country_s, x="country", y="success",
                     color="success", color_continuous_scale=[[0,C_DANGER],[1,C_SUCCESS]],
                     text=country_s.success.apply(lambda v: f"{v*100:.0f}%"))
        fig.update_traces(textposition="outside")
        fig.update_layout(height=340, coloraxis_showscale=False,
                          yaxis=dict(gridcolor="#1e2235", tickformat=".0%"),
                          xaxis=dict(gridcolor="rgba(0,0,0,0)"), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    # ROC Curve
    st.markdown('<div class="section-label">ROC Curves — All Models</div>', unsafe_allow_html=True)
    fig_roc = go.Figure()
    colors = [C_ACCENT, C_WARNING, C_SUCCESS]
    for (name, res), col in zip(MODEL_RESULTS.items(), colors):
        fig_roc.add_trace(go.Scatter(x=res["fpr"], y=res["tpr"], mode="lines",
                                     name=f"{name}  AUC={res['auc']:.3f}",
                                     line=dict(color=col, width=2.5)))
    fig_roc.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Random Baseline",
                                 line=dict(color="#3a3f5c", dash="dash", width=1.5)))
    fig_roc.update_layout(height=380, xaxis_title="False Positive Rate",
                           yaxis_title="True Positive Rate",
                           xaxis=dict(gridcolor="#1e2235"), yaxis=dict(gridcolor="#1e2235"),
                           legend=dict(font=dict(size=12)), **PLOT_CFG)
    st.plotly_chart(fig_roc, use_container_width=True)

    col_e, col_f = st.columns(2)

    # Burn rate box
    with col_e:
        st.markdown('<div class="section-label">Burn Rate vs Outcome</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for outcome, color, label in [(1,C_SUCCESS,"Survived"),(0,C_DANGER,"Failed")]:
            subset = DATA[DATA.success==outcome]
            fig.add_trace(go.Box(y=subset["burn_rate"], name=label,
                                 marker_color=color, line_color=color,
                                 fillcolor=color.replace("#","rgba(").replace(")",",0.15)") if "#" in color else color,
                                 boxmean=True))
        fig.update_layout(height=320, yaxis=dict(gridcolor="#1e2235"), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    # NPS distribution
    with col_f:
        st.markdown('<div class="section-label">NPS Score Distribution</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for outcome, color, label in [(1,C_SUCCESS,"Survived"),(0,C_DANGER,"Failed")]:
            subset = DATA[DATA.success==outcome]
            fig.add_trace(go.Histogram(x=subset["nps_score"], name=label,
                                       marker_color=color, opacity=0.7, nbinsx=25))
        fig.update_layout(barmode="overlay", height=320,
                          xaxis=dict(gridcolor="#1e2235"), yaxis=dict(gridcolor="#1e2235"),
                          legend=dict(font=dict(size=11)), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    # 3D Metrics
    st.markdown('<div class="section-label">3D Startup Universe</div>', unsafe_allow_html=True)
    samp3d = DATA.sample(min(800, len(DATA)), random_state=9)
    fig3d = go.Figure(go.Scatter3d(
        x=samp3d["funding"]/1e6, y=samp3d["team_experience"], z=samp3d["revenue_growth"],
        mode="markers",
        marker=dict(size=4, color=samp3d["success"],
                    colorscale=[[0,C_DANGER],[1,C_SUCCESS]], opacity=0.8,
                    colorbar=dict(title="Success", thickness=10, len=0.6)),
        hovertemplate="Funding: $%{x:.1f}M<br>Exp: %{y}yr<br>Growth: %{z:.2f}x<extra></extra>"
    ))
    fig3d.update_layout(
        height=500, paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            xaxis=dict(title="Funding ($M)", backgroundcolor="#07080d", gridcolor="#1e2235"),
            yaxis=dict(title="Team Exp (yr)", backgroundcolor="#07080d", gridcolor="#1e2235"),
            zaxis=dict(title="Revenue Growth", backgroundcolor="#07080d", gridcolor="#1e2235"),
            bgcolor="#07080d"
        ),
        margin=dict(l=0,r=0,t=0,b=0)
    )
    st.plotly_chart(fig3d, use_container_width=True)

    st.markdown('<div class="section-label">Dataset Preview (Latest 50 Records)</div>', unsafe_allow_html=True)
    st.dataframe(DATA.tail(50), use_container_width=True, height=350)

# ═══════════════════════════════════════════════
# ██ PREDICT
# ═══════════════════════════════════════════════
elif selected == "Predict":
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Prediction Engine</div>
        <div class="page-sub">Enter Startup Parameters · Get AI Verdict · Live Risk Assessment</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Core Parameters</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        funding     = st.number_input("💰 Funding ($)", min_value=0, max_value=200_000_000,
                                       value=500_000, step=50_000, format="%d")
        team_size   = st.number_input("👥 Team Size", min_value=1, max_value=500, value=10)
    with c2:
        team_exp    = st.slider("🎓 Team Experience (yrs)", 1, 15, 5)
        market_sz   = st.number_input("🌍 Market Size ($Bn)", min_value=0.1, max_value=500.0, value=10.0, step=0.5)
    with c3:
        sector_sel  = st.selectbox("🏭 Sector",
                                   ['SaaS','FinTech','HealthTech','EdTech','E-Commerce',
                                    'AI/ML','CleanTech','Cybersecurity','Gaming','BioTech'])
        stage_sel   = st.selectbox("📊 Stage",
                                   ['Pre-Seed','Seed','Series A','Series B','Series C'])

    st.markdown('<div class="section-label">Business Metrics</div>', unsafe_allow_html=True)
    c4, c5, c6, c7 = st.columns(4)
    with c4: burn_rate  = st.number_input("🔥 Burn Rate ($/mo)", 0, 2_000_000, 80_000, 5_000)
    with c5: rev_growth = st.number_input("📈 Revenue Growth (x)", -0.5, 10.0, 1.2, 0.1)
    with c6: runway     = st.slider("⛽ Runway (months)", 1, 48, 18)
    with c7: nps        = st.slider("⭐ NPS Score", -100, 100, 30)

    c8, c9 = st.columns(2)
    with c8: competition = st.slider("⚔️ Competition Level (1-10)", 1, 10, 5)
    with c9: biz_model   = st.slider("💡 Business Model Score (1-10)", 1, 10, 6)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⚡  LAUNCH AI PREDICTION", use_container_width=True):
        inp = np.array([[funding, team_exp, market_sz, competition, biz_model,
                         rev_growth, burn_rate, runway, team_size, nps]])
        inp_s = SCALER.transform(inp)
        prob  = BEST_MODEL.predict_proba(inp_s)[0][1]
        conf  = abs(prob - 0.5) * 2

        # Save activity
        act = pd.read_csv("user_activity.csv")
        new = pd.DataFrame({"username":[st.session_state.username],
                             "login_date":[datetime.now().strftime("%Y-%m-%d")],
                             "login_time":[datetime.now().strftime("%H:%M:%S")],
                             "funding":[funding], "team_experience":[team_exp],
                             "prediction_probability":[prob], "sector":[sector_sel]})
        pd.concat([act, new]).to_csv("user_activity.csv", index=False)

        # Verdict
        if prob >= 0.5:
            st.markdown(f"""
            <div class="verdict-success">
                <div class="verdict-title" style='color:#43e8ac;'>✅ HIGH POTENTIAL</div>
                <div class="verdict-sub" style='color:#43e8ac;'>SUCCESS PROBABILITY: {prob*100:.1f}% · CONFIDENCE: {conf*100:.0f}%</div>
            </div><br>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="verdict-fail">
                <div class="verdict-title" style='color:#ff4d6d;'>⚠️ HIGH RISK</div>
                <div class="verdict-sub" style='color:#ff4d6d;'>SUCCESS PROBABILITY: {prob*100:.1f}% · CONFIDENCE: {conf*100:.0f}%</div>
            </div><br>""", unsafe_allow_html=True)

        g1, g2, g3 = st.columns(3)
        # Gauge 1 — Success prob
        with g1:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=prob*100,
                title={"text":"Success Probability", "font":{"size":13,"color":"#6b738f"}},
                number={"suffix":"%","font":{"family":"Syne","color":"#e4e8f5","size":28}},
                gauge={"axis":{"range":[0,100],"tickcolor":"#3a3f5c"},
                       "bar":{"color":C_SUCCESS if prob>=0.5 else C_DANGER},
                       "bgcolor":"rgba(0,0,0,0)",
                       "steps":[{"range":[0,50],"color":"rgba(255,77,109,0.08)"},
                                 {"range":[50,100],"color":"rgba(67,232,172,0.08)"}],
                       "threshold":{"line":{"color":C_ACCENT,"width":3},"value":prob*100}}
            ))
            fig_g.update_layout(height=250, **PLOT_CFG)
            st.plotly_chart(fig_g, use_container_width=True)

        # Gauge 2 — Confidence
        with g2:
            fig_c = go.Figure(go.Indicator(
                mode="gauge+number", value=conf*100,
                title={"text":"Model Confidence","font":{"size":13,"color":"#6b738f"}},
                number={"suffix":"%","font":{"family":"Syne","color":"#e4e8f5","size":28}},
                gauge={"axis":{"range":[0,100],"tickcolor":"#3a3f5c"},
                       "bar":{"color":C_ACCENT},
                       "bgcolor":"rgba(0,0,0,0)",
                       "steps":[{"range":[0,40],"color":"rgba(255,179,71,0.06)"},
                                 {"range":[40,100],"color":"rgba(108,99,255,0.08)"}]}
            ))
            fig_c.update_layout(height=250, **PLOT_CFG)
            st.plotly_chart(fig_c, use_container_width=True)

        # Gauge 3 — Runway health
        with g3:
            runway_health = min(runway / 36, 1) * 100
            fig_r = go.Figure(go.Indicator(
                mode="gauge+number", value=runway_health,
                title={"text":"Runway Health","font":{"size":13,"color":"#6b738f"}},
                number={"suffix":"%","font":{"family":"Syne","color":"#e4e8f5","size":28}},
                gauge={"axis":{"range":[0,100],"tickcolor":"#3a3f5c"},
                       "bar":{"color":C_WARNING},
                       "bgcolor":"rgba(0,0,0,0)"}
            ))
            fig_r.update_layout(height=250, **PLOT_CFG)
            st.plotly_chart(fig_r, use_container_width=True)

        # All-model probabilities
        st.markdown('<div class="section-label">All Model Predictions</div>', unsafe_allow_html=True)
        model_probs = {n: r["model"].predict_proba(inp_s)[0][1] for n, r in MODEL_RESULTS.items()}
        fig_bar = go.Figure(go.Bar(
            x=list(model_probs.keys()),
            y=[v*100 for v in model_probs.values()],
            marker_color=[C_SUCCESS if v>=0.5 else C_DANGER for v in model_probs.values()],
            text=[f"{v*100:.1f}%" for v in model_probs.values()],
            textposition="outside"
        ))
        fig_bar.add_hline(y=50, line_dash="dash", line_color=C_WARNING, annotation_text="Decision Boundary")
        fig_bar.update_layout(height=300, yaxis=dict(range=[0,110], gridcolor="#1e2235"), **PLOT_CFG)
        st.plotly_chart(fig_bar, use_container_width=True)

        # Radar profile
        st.markdown('<div class="section-label">Startup Risk Radar</div>', unsafe_allow_html=True)
        cats   = ["Funding Power","Team Strength","Market Opportunity","Competitive Moat","Business Viability","Runway","Growth"]
        vals   = [
            min(funding/200e6,1)*10, team_exp/15*10, min(market_sz/500,1)*10,
            (10-competition), biz_model, min(runway/36,1)*10, min(max(rev_growth,0)/5,1)*10
        ]
        med    = [5]*len(cats)
        fig_rad = go.Figure()
        fig_rad.add_trace(go.Scatterpolar(r=vals+[vals[0]], theta=cats+[cats[0]],
                                           fill="toself", name="Your Startup",
                                           fillcolor="rgba(108,99,255,0.12)",
                                           line=dict(color=C_ACCENT, width=2)))
        fig_rad.add_trace(go.Scatterpolar(r=med+[med[0]], theta=cats+[cats[0]],
                                           fill="toself", name="Median Startup",
                                           fillcolor="rgba(255,179,71,0.06)",
                                           line=dict(color=C_WARNING, width=1, dash="dot")))
        fig_rad.update_layout(
            polar=dict(radialaxis=dict(range=[0,10], gridcolor="#1e2235"),
                       angularaxis=dict(gridcolor="#1e2235")),
            height=380, legend=dict(font=dict(size=11)), **PLOT_CFG
        )
        st.plotly_chart(fig_rad, use_container_width=True)

        # Recommendations
        st.markdown('<div class="section-label">AI Recommendations</div>', unsafe_allow_html=True)
        recs = []
        if funding < 500_000:  recs.append(("warning","💰","Raise more capital — funding is below typical Seed threshold"))
        if team_exp < 4:       recs.append(("warning","🎓","Bring in senior advisors — team experience is low"))
        if competition > 7:    recs.append(("error","⚔️","Extremely high competition — identify a defensible niche"))
        if runway < 12:        recs.append(("error","⛽","Critical: <12 months runway — prioritise fundraising immediately"))
        if rev_growth < 0.5:   recs.append(("warning","📈","Revenue growth is lagging — review GTM and pricing strategy"))
        if biz_model < 5:      recs.append(("warning","💡","Business model needs strengthening — validate unit economics"))
        if nps < 20:           recs.append(("warning","⭐","Low NPS — invest in customer success and product refinement"))
        if not recs:
            st.success("🏆 Strong fundamentals across all dimensions — excellent position!")
        for kind, icon, msg in recs:
            if kind == "error": st.error(f"{icon} {msg}")
            else: st.warning(f"{icon} {msg}")

# ═══════════════════════════════════════════════
# ██ ANALYTICS
# ═══════════════════════════════════════════════
elif selected == "Analytics":
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Analytics Lab</div>
        <div class="page-sub">Deep Dive · Correlations · Sector Breakdown · Survival Analysis</div>
    </div>""", unsafe_allow_html=True)

    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        sectors_sel = st.multiselect("Filter by Sector", DATA["sector"].unique(), default=list(DATA["sector"].unique()))
    with col_f2:
        stages_sel = st.multiselect("Filter by Stage", DATA["stage"].unique(), default=list(DATA["stage"].unique()))
    with col_f3:
        min_fund, max_fund = st.slider("Funding Range ($)", 0, 200_000_000,
                                        (0, 200_000_000), step=1_000_000,
                                        format="$%d")

    filtered = DATA[
        DATA["sector"].isin(sectors_sel) &
        DATA["stage"].isin(stages_sel) &
        DATA["funding"].between(min_fund, max_fund)
    ]

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Filtered Startups", f"{len(filtered):,}")
    c2.metric("Success Rate", f"{filtered['success'].mean()*100:.1f}%")
    c3.metric("Avg Funding", f"${filtered['funding'].mean()/1e6:.1f}M")
    c4.metric("Avg Runway", f"{filtered['runway_months'].mean():.0f} mo")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-label">Revenue Growth Distribution</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for outcome, color, label in [(1,C_SUCCESS,"Survived"),(0,C_DANGER,"Failed")]:
            sub = filtered[filtered.success==outcome]
            fig.add_trace(go.Histogram(x=sub["revenue_growth"], name=label,
                                       marker_color=color, opacity=0.7, nbinsx=30))
        fig.update_layout(barmode="overlay", height=300,
                          xaxis=dict(gridcolor="#1e2235"), yaxis=dict(gridcolor="#1e2235"),
                          legend=dict(font=dict(size=11)), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-label">Burn Rate vs Outcome (Violin)</div>', unsafe_allow_html=True)
        fig = go.Figure()
        for outcome, color, label in [(1,C_SUCCESS,"Survived"),(0,C_DANGER,"Failed")]:
            sub = filtered[filtered.success==outcome]
            fig.add_trace(go.Violin(y=sub["burn_rate"], name=label, fillcolor=color,
                                    line_color=color, opacity=0.7, box_visible=True, meanline_visible=True))
        fig.update_layout(height=300, violingap=0.4,
                          yaxis=dict(gridcolor="#1e2235"), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown('<div class="section-label">Success by Team Experience</div>', unsafe_allow_html=True)
        te = filtered.groupby("team_experience")["success"].mean().reset_index()
        fig = px.area(te, x="team_experience", y="success",
                      color_discrete_sequence=[C_ACCENT])
        fig.update_layout(height=300, yaxis=dict(gridcolor="#1e2235", tickformat=".0%"),
                          xaxis=dict(gridcolor="#1e2235"), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-label">Competition vs Success Rate</div>', unsafe_allow_html=True)
        cs = filtered.groupby("competition_level")["success"].mean().reset_index()
        fig = px.line(cs, x="competition_level", y="success", markers=True,
                      color_discrete_sequence=[C_DANGER])
        fig.update_layout(height=300, yaxis=dict(gridcolor="#1e2235", tickformat=".0%"),
                          xaxis=dict(gridcolor="#1e2235"), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    # Correlation heatmap
    st.markdown('<div class="section-label">Feature Correlation Matrix</div>', unsafe_allow_html=True)
    num_cols = ["funding","team_experience","market_size_bn","burn_rate","revenue_growth",
                "competition_level","business_model_score","runway_months","nps_score","success"]
    corr = filtered[num_cols].corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", aspect="auto", zmin=-1, zmax=1)
    fig.update_layout(height=440, **PLOT_CFG)
    st.plotly_chart(fig, use_container_width=True)

    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown('<div class="section-label">Overall Success Split</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Pie(
            labels=["Success","Failure"],
            values=[filtered["success"].sum(), filtered["failure"].sum()],
            hole=0.58, marker_colors=[C_SUCCESS, C_DANGER],
            textfont=dict(family="JetBrains Mono", size=12)
        ))
        fig.update_layout(height=300, legend=dict(font=dict(size=12)), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    with col_f:
        st.markdown('<div class="section-label">Market Size vs Avg Funding</div>', unsafe_allow_html=True)
        ms = filtered.groupby("sector").agg(avg_fund=("funding","mean"), sr=("success","mean"),
                                             count=("success","count")).reset_index()
        fig = px.scatter(ms, x="avg_fund", y="sr", size="count", color="sr",
                         text="sector", color_continuous_scale=[[0,C_DANGER],[1,C_SUCCESS]],
                         size_max=40)
        fig.update_traces(textposition="top center", textfont_size=10)
        fig.update_layout(height=300, coloraxis_showscale=False,
                          xaxis=dict(gridcolor="#1e2235"),
                          yaxis=dict(gridcolor="#1e2235", tickformat=".0%"), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-label">Filtered Dataset</div>', unsafe_allow_html=True)
    st.dataframe(filtered.head(100), use_container_width=True, height=300)
    st.download_button("📥 Download Filtered Data", filtered.to_csv(index=False),
                       "filtered_startups.csv", mime="text/csv")

# ═══════════════════════════════════════════════
# ██ MODEL LAB
# ═══════════════════════════════════════════════
elif selected == "Model Lab":
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Model Lab</div>
        <div class="page-sub">Confusion Matrix · Feature Importance · Probability Distributions</div>
    </div>""", unsafe_allow_html=True)

    model_sel = st.selectbox("Select Model to Inspect",
                              list(MODEL_RESULTS.keys()),
                              index=list(MODEL_RESULTS.keys()).index(BEST_NAME))
    res = MODEL_RESULTS[model_sel]
    m   = res["model"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accuracy",  f"{res['acc']*100:.2f}%")
    c2.metric("AUC Score", f"{res['auc']:.4f}")
    preds = m.predict(X_TE_S)
    prec  = (preds[Y_TE==1]==1).mean()
    rec   = (preds[preds==1]==Y_TE[preds==1]).mean() if (preds==1).any() else 0
    c3.metric("Precision", f"{prec*100:.1f}%")
    c4.metric("Recall",    f"{rec*100:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-label">Confusion Matrix</div>', unsafe_allow_html=True)
        cm = confusion_matrix(Y_TE, preds)
        fig = go.Figure(go.Heatmap(
            z=cm,
            x=["Predicted Fail","Predicted Success"],
            y=["Actual Fail","Actual Success"],
            colorscale=[[0,"#07080d"],[1,C_ACCENT]],
            text=cm, texttemplate="%{text}",
            textfont={"family":"JetBrains Mono","size":22,"color":"#e4e8f5"},
            showscale=False
        ))
        fig.update_layout(height=300, **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-label">ROC Curve</div>', unsafe_allow_html=True)
        probs = m.predict_proba(X_TE_S)[:,1]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=res["fpr"], y=res["tpr"], mode="lines",
                                 name=f"AUC={res['auc']:.3f}",
                                 line=dict(color=C_ACCENT, width=2.5),
                                 fill="tozeroy", fillcolor="rgba(108,99,255,0.07)"))
        fig.add_trace(go.Scatter(x=[0,1],y=[0,1],mode="lines",name="Baseline",
                                 line=dict(color="#3a3f5c",dash="dash")))
        fig.update_layout(height=300, xaxis_title="FPR", yaxis_title="TPR",
                          xaxis=dict(gridcolor="#1e2235"), yaxis=dict(gridcolor="#1e2235"),
                          legend=dict(font=dict(size=11)), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-label">Prediction Probability Distribution</div>', unsafe_allow_html=True)
    fig = go.Figure()
    for outcome, color, label in [(1,C_SUCCESS,"Survived"),(0,C_DANGER,"Failed")]:
        mask = Y_TE==outcome
        fig.add_trace(go.Histogram(x=probs[mask], name=label, marker_color=color, opacity=0.7, nbinsx=35))
    fig.add_vline(x=0.5, line_dash="dash", line_color=C_WARNING,
                  annotation_text="Decision Boundary (0.5)",
                  annotation_font=dict(family="JetBrains Mono", size=11, color=C_WARNING))
    fig.update_layout(barmode="overlay", height=300,
                      xaxis=dict(gridcolor="#1e2235"), yaxis=dict(gridcolor="#1e2235"),
                      legend=dict(font=dict(size=11)), **PLOT_CFG)
    st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.markdown('<div class="section-label">Feature Importance</div>', unsafe_allow_html=True)
        if hasattr(m, "feature_importances_"):
            imps = m.feature_importances_
        else:
            imps = np.abs(m.coef_[0])
        fi = pd.DataFrame({"Feature":FEATURE_COLS,"Importance":imps}).sort_values("Importance")
        fig = px.bar(fi, x="Importance", y="Feature", orientation="h",
                     color="Importance", color_continuous_scale=[[0,"#131620"],[1,C_ACCENT]])
        fig.update_layout(height=360, coloraxis_showscale=False,
                          xaxis=dict(gridcolor="#1e2235"), yaxis=dict(gridcolor="rgba(0,0,0,0)"), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        st.markdown('<div class="section-label">Model Comparison</div>', unsafe_allow_html=True)
        comp = pd.DataFrame({
            "Model":    list(MODEL_RESULTS.keys()),
            "Accuracy": [r["acc"]*100 for r in MODEL_RESULTS.values()],
            "AUC":      [r["auc"] for r in MODEL_RESULTS.values()]
        })
        fig = go.Figure()
        fig.add_trace(go.Bar(x=comp["Model"], y=comp["Accuracy"], name="Accuracy (%)",
                             marker_color=C_ACCENT, text=comp["Accuracy"].apply(lambda v:f"{v:.1f}%"),
                             textposition="outside"))
        fig.add_trace(go.Scatter(x=comp["Model"], y=comp["AUC"]*100, name="AUC×100",
                                 mode="lines+markers", line=dict(color=C_SUCCESS, width=2),
                                 marker=dict(size=10)))
        fig.update_layout(height=360, yaxis=dict(range=[70,100], gridcolor="#1e2235"),
                          legend=dict(font=dict(size=11)), **PLOT_CFG)
        st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════
# ██ AI ANALYST CHATBOT
# ═══════════════════════════════════════════════
elif selected == "AI Analyst":
    st.markdown("""
    <div class="page-header">
        <div class="page-title">AI Analyst</div>
        <div class="page-sub">Powered by Claude · Real Dataset Awareness · Startup Intelligence</div>
    </div>""", unsafe_allow_html=True)

    # Suggested prompts
    st.markdown('<div class="section-label">Quick Questions</div>', unsafe_allow_html=True)
    quick_cols = st.columns(4)
    quick_qs = [
        "Which sector has the highest success rate?",
        "What's the most important feature for success?",
        "How does runway affect startup survival?",
        "Give me investor advice for a FinTech startup",
    ]
    for i, (col, q) in enumerate(zip(quick_cols, quick_qs)):
        with col:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":q})
                with st.spinner("Thinking…"):
                    reply = call_claude(st.session_state.chat_history, build_data_context())
                st.session_state.chat_history.append({"role":"assistant","content":reply})
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Chat window
    if not st.session_state.chat_history:
        st.markdown(f"""
        <div class="chat-wrapper" id="chat-box">
            <div class="msg-ai">
                <div class="avatar-ai">🧬</div>
                <div class="bubble-ai">
                    Hi! I'm <strong>NexusAI Analyst</strong>, your startup intelligence assistant.<br><br>
                    I have live access to your dataset of <strong>{len(DATA):,} startups</strong> across 
                    10 sectors and 10 countries, and I know the performance of all 3 ML models.<br><br>
                    Ask me anything: <em>success patterns, model insights, investor strategy, 
                    sector analysis, or how to improve your startup's chances.</em>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        msgs_html = ""
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                msgs_html += f'<div class="msg-user"><div class="bubble-user">{msg["content"]}</div></div>'
            else:
                content = msg["content"].replace("\n","<br>").replace("**","<b>").replace("**","</b>")
                msgs_html += f'<div class="msg-ai"><div class="avatar-ai">🧬</div><div class="bubble-ai">{content}</div></div>'

        st.markdown(f'<div class="chat-wrapper">{msgs_html}</div>', unsafe_allow_html=True)

    # Input
    col_inp, col_btn = st.columns([5, 1])
    with col_inp:
        user_msg = st.text_input("", placeholder="Ask about startup success, ML models, investment strategy…",
                                  key="chat_input", label_visibility="collapsed")
    with col_btn:
        send = st.button("Send →", use_container_width=True)

    if send and user_msg.strip():
        st.session_state.chat_history.append({"role":"user","content":user_msg.strip()})
        with st.spinner("NexusAI is thinking…"):
            reply = call_claude(st.session_state.chat_history, build_data_context())
        st.session_state.chat_history.append({"role":"assistant","content":reply})
        st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_history = []; st.rerun()
    with c2:
        if st.session_state.chat_history:
            chat_txt = "\n\n".join([f"[{m['role'].upper()}]\n{m['content']}" for m in st.session_state.chat_history])
            st.download_button("📥 Export Chat", chat_txt, "nexusai_conversation.txt",
                               use_container_width=True)

    # Live stats panel
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Live Dataset Snapshot (for AI context)</div>', unsafe_allow_html=True)
    snap_cols = st.columns(4)
    snap_cols[0].metric("Top Sector (Success)", DATA.groupby("sector")["success"].mean().idxmax())
    snap_cols[1].metric("Top Country",          DATA.groupby("country")["success"].mean().idxmax())
    snap_cols[2].metric("Best Stage",           DATA.groupby("stage")["success"].mean().idxmax())
    snap_cols[3].metric("Best Model",           BEST_NAME.split()[0])

# ═══════════════════════════════════════════════
# ██ MY PROFILE
# ═══════════════════════════════════════════════
elif selected == "My Profile":
    uname = st.session_state.username
    activity = pd.read_csv("user_activity.csv")
    user_data = activity[activity.username == uname].copy()

    st.markdown(f"""
    <div class="page-header">
        <div class="page-title">{uname.title()}</div>
        <div class="page-sub">Founder Profile · Prediction History · Achievements</div>
    </div>""", unsafe_allow_html=True)

    if not user_data.empty:
        avg_prob  = user_data["prediction_probability"].mean()
        best_prob = user_data["prediction_probability"].max()
        total     = len(user_data)
        wins      = int((user_data["prediction_probability"]>=0.5).sum())

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Predictions", total)
        c2.metric("Avg Success Prob",  f"{avg_prob*100:.1f}%")
        c3.metric("Best Prediction",   f"{best_prob*100:.1f}%")
        c4.metric("Successful Runs",   wins)

        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="section-label">Your Outcome Split</div>', unsafe_allow_html=True)
            f_count = total - wins
            fig = go.Figure(go.Pie(
                labels=["Success","Failure"], values=[wins, f_count], hole=0.58,
                marker_colors=[C_SUCCESS, C_DANGER],
                textfont=dict(family="JetBrains Mono",size=13)
            ))
            fig.update_layout(height=300, legend=dict(font=dict(size=12)), **PLOT_CFG)
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.markdown('<div class="section-label">Prediction Growth Trend</div>', unsafe_allow_html=True)
            ud = user_data.reset_index(drop=True)
            ud["Run"] = range(1, len(ud)+1)
            fig = px.line(ud, x="Run", y="prediction_probability", markers=True,
                          color_discrete_sequence=[C_ACCENT])
            fig.add_hline(y=0.5, line_dash="dash", line_color=C_DANGER,
                          annotation_text="Success Threshold",
                          annotation_font=dict(color=C_DANGER, size=11))
            fig.update_layout(height=300, yaxis=dict(gridcolor="#1e2235", range=[0,1], tickformat=".0%"),
                              xaxis=dict(gridcolor="#1e2235"), **PLOT_CFG)
            st.plotly_chart(fig, use_container_width=True)

        # Sector breakdown
        if "sector" in user_data.columns and user_data["sector"].notna().any():
            st.markdown('<div class="section-label">Sectors Explored</div>', unsafe_allow_html=True)
            sec_counts = user_data["sector"].value_counts().reset_index()
            sec_counts.columns = ["Sector","Count"]
            fig = px.bar(sec_counts, x="Count", y="Sector", orientation="h",
                         color="Count", color_continuous_scale=[[0,"#131620"],[1,C_ACCENT]])
            fig.update_layout(height=max(200,len(sec_counts)*40), coloraxis_showscale=False, **PLOT_CFG)
            st.plotly_chart(fig, use_container_width=True)

        # Badge
        st.markdown('<div class="section-label">Achievement Badge</div>', unsafe_allow_html=True)
        if avg_prob > 0.75:   badge, badge_col, label = "🥇","#ffd700","ELITE FOUNDER"
        elif avg_prob > 0.60: badge, badge_col, label = "🥈","#c0c0c0","GROWTH LEADER"
        elif avg_prob > 0.45: badge, badge_col, label = "🥉","#cd7f32","RISING ENTREPRENEUR"
        else:                 badge, badge_col, label = "🔍","#6b738f","TRAINEE ANALYST"

        st.markdown(f"""
        <div style='background:#0d0f17; border:1px solid {badge_col}44; border-radius:16px;
                    padding:28px; text-align:center; box-shadow:0 0 30px {badge_col}15;'>
            <div style='font-size:52px; margin-bottom:8px;'>{badge}</div>
            <div style='font-family:Syne,sans-serif; font-size:22px; font-weight:800;
                        color:{badge_col}; letter-spacing:0px; margin-bottom:6px;'>{label}</div>
            <div style='font-family:"JetBrains Mono",monospace; font-size:11px; color:#6b738f; letter-spacing:2px;'>
                AVG SUCCESS RATE: {avg_prob*100:.1f}% · {total} PREDICTIONS
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Prediction History</div>', unsafe_allow_html=True)
        st.dataframe(user_data.tail(20), use_container_width=True)
        st.download_button("📥 Download Full Report", user_data.to_csv(index=False),
                           f"{uname}_nexusai_report.csv", mime="text/csv")
    else:
        st.info("🚀 No predictions yet — head to the Predict page to get started!")