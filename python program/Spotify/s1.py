import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config("Spotify Analytics", layout="wide", page_icon="🎵")

# ── Load CSS ──────────────────────────────────────────────
def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("spotify.css")

# ── Spotify SVG Logo ─────────────────────────────────────
SPOTIFY_LOGO = """
<svg viewBox="0 0 496 512" xmlns="http://www.w3.org/2000/svg">
  <path fill="#1DB954" d="M248 8C111.1 8 8 111.1 8 248s103.1 240 240 240 240-103.1 240-240S384.9 8 248 8zm110.7
  339.4c-4.3 7.1-13.4 9.2-20.5 4.9-56.2-34.3-126.9-42-210.3-23-8 1.8-16-3.2-17.8-11.2-1.8-8
  3.2-16 11.2-17.8 91.1-20.8 169.3-11.9 232.3 26.6 7.1 4.3 9.3 13.4 5 20.5zm29.5-65.8c-5.4
  8.8-16.8 11.5-25.5 6.2-64.3-39.5-162.4-50.9-238.4-27.9-9.9 3-20.4-2.5-23.3-12.4-3-9.9
  2.5-20.4 12.4-23.3 86.8-26.4 194.5-13.6 268.2 31.8 8.7 5.4 11.4 16.8 6.6 25.6zm2.5-68.4
  c-77.1-45.8-204.3-50-277.9-27.7-11.8 3.6-24.3-3.1-27.9-14.9-3.6-11.8 3.1-24.3 14.9-27.9
  84.4-25.6 224.8-20.7 313.3 32.2 10.6 6.3 14 20 7.7 30.6-6.3 10.5-20 13.9-30.1 7.7z"/>
</svg>
"""

# ─────────────────────────────────────────────────────────
# AUTH HELPERS
# ─────────────────────────────────────────────────────────
def init_auth():
    if "users" not in st.session_state:
        st.session_state["users"] = {"demo@spotify.com": "demo123"}
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "current_user" not in st.session_state:
        st.session_state["current_user"] = None
    if "auth_page" not in st.session_state:
        st.session_state["auth_page"] = "login"

def login(email, password):
    users = st.session_state["users"]
    if email in users and users[email] == password:
        st.session_state["logged_in"] = True
        st.session_state["current_user"] = email
        return True
    return False

def signup(email, password):
    users = st.session_state["users"]
    if email in users:
        return False
    users[email] = password
    st.session_state["logged_in"] = True
    st.session_state["current_user"] = email
    return True

def logout():
    st.session_state["logged_in"] = False
    st.session_state["current_user"] = None
    st.session_state["auth_page"] = "login"

# ─────────────────────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────────────────────
def show_login():
    st.markdown('<div class="sp-auth-bg"></div>', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 1.4, 1])
    with col_c:
        st.markdown('<div class="sp-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sp-logo">{SPOTIFY_LOGO}</div>', unsafe_allow_html=True)
        st.markdown('<p class="sp-card-title">Log in to Spotify Analytics</p>', unsafe_allow_html=True)

        # Social buttons
        st.markdown(
            '<button class="sp-social-btn">'
            '<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.32-8.16 2.32-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>'
            '&nbsp; Continue with Google</button>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<button class="sp-social-btn">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.335-1.755-1.335-1.755-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12"/></svg>'
            '&nbsp; Continue with GitHub</button>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<button class="sp-social-btn">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="#1877F2"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>'
            '&nbsp; Continue with Facebook</button>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="sp-divider">or</div>', unsafe_allow_html=True)

        st.markdown('<p class="sp-field-label">Email address</p>', unsafe_allow_html=True)
        email = st.text_input("__email", placeholder="Email address", key="login_email", label_visibility="collapsed")

        st.markdown('<p class="sp-field-label" style="margin-top:12px;">Password</p>', unsafe_allow_html=True)
        password = st.text_input("__password", placeholder="Password", key="login_password", type="password", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Log In", use_container_width=True, type="primary", key="login_btn"):
            if not email or not password:
                st.error("Please enter your email and password.")
            elif login(email, password):
                st.rerun()
            else:
                st.error("Incorrect email or password.")

        st.markdown(
            '<p style="text-align:center;margin-top:16px;">'
            '<a href="#" style="color:#fff;font-size:13px;font-weight:600;text-decoration:underline;">'
            'Forgot your password?</a></p>',
            unsafe_allow_html=True
        )
        st.markdown('<hr style="border-color:#282828;margin:24px 0;">', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align:center;color:#A7A7A7;font-size:15px;margin-bottom:12px;">'
            "Don't have an account?</p>",
            unsafe_allow_html=True
        )
        if st.button("Sign up for Spotify Analytics", use_container_width=True, key="goto_signup"):
            st.session_state["auth_page"] = "signup"
            st.rerun()
        st.markdown(
            '<p style="text-align:center;color:#6A6A6A;font-size:12px;margin-top:20px;">'
            '✦ Demo: demo@spotify.com &nbsp;/&nbsp; demo123</p>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# SIGNUP PAGE
# ─────────────────────────────────────────────────────────
def show_signup():
    st.markdown('<div class="sp-auth-bg"></div>', unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 1.4, 1])
    with col_c:
        st.markdown('<div class="sp-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="sp-logo">{SPOTIFY_LOGO}</div>', unsafe_allow_html=True)
        st.markdown('<p class="sp-card-title">Sign up for free to start listening</p>', unsafe_allow_html=True)

        st.markdown(
            '<button class="sp-social-btn">'
            '<svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.32-8.16 2.32-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>'
            '&nbsp; Sign up with Google</button>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<button class="sp-social-btn">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.335-1.755-1.335-1.755-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12"/></svg>'
            '&nbsp; Sign up with GitHub</button>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<button class="sp-social-btn">'
            '<svg width="18" height="18" viewBox="0 0 24 24" fill="#1877F2"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>'
            '&nbsp; Sign up with Facebook</button>',
            unsafe_allow_html=True
        )

        st.markdown('<div class="sp-divider">or</div>', unsafe_allow_html=True)

        st.markdown('<p class="sp-field-label">What\'s your email?</p>', unsafe_allow_html=True)
        email = st.text_input("__su_email", placeholder="Enter your email address.", key="signup_email", label_visibility="collapsed")

        st.markdown('<p class="sp-field-label" style="margin-top:12px;">Create a password</p>', unsafe_allow_html=True)
        password = st.text_input("__su_pw", placeholder="Create a password.", key="signup_password", type="password", label_visibility="collapsed")

        st.markdown('<p class="sp-field-label" style="margin-top:12px;">Confirm your password</p>', unsafe_allow_html=True)
        confirm = st.text_input("__su_cf", placeholder="Confirm your password.", key="signup_confirm", type="password", label_visibility="collapsed")

        st.markdown('<p class="sp-field-label" style="margin-top:12px;">What should we call you?</p>', unsafe_allow_html=True)
        name = st.text_input("__su_name", placeholder="Enter a profile name.", key="signup_name", label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Create Account", use_container_width=True, type="primary", key="signup_btn"):
            if not email or not password or not confirm:
                st.error("Please fill in all required fields.")
            elif password != confirm:
                st.error("Passwords don't match.")
            elif len(password) < 6:
                st.error("Your password's too short. Use at least 6 characters.")
            elif not signup(email, password):
                st.error("This email is already registered. Try logging in instead.")
            else:
                st.success(f"Welcome{', ' + name if name else ''}! 🎉")
                st.rerun()

        st.markdown(
            '<p style="text-align:center;color:#A7A7A7;font-size:12px;margin:16px 0;">'
            'By creating an account, you agree to Spotify\'s '
            '<a href="#" style="color:#fff;text-decoration:underline;">Terms of Service</a> and '
            '<a href="#" style="color:#fff;text-decoration:underline;">Privacy Policy</a>.</p>',
            unsafe_allow_html=True
        )
        st.markdown('<hr style="border-color:#282828;margin:20px 0;">', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align:center;color:#A7A7A7;font-size:15px;margin-bottom:12px;">'
            'Already have an account?</p>',
            unsafe_allow_html=True
        )
        if st.button("Log in here", use_container_width=True, key="goto_login"):
            st.session_state["auth_page"] = "login"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# AUTH GATE
# ─────────────────────────────────────────────────────────
init_auth()

if not st.session_state["logged_in"]:
    if st.session_state["auth_page"] == "login":
        show_login()
    else:
        show_signup()
    st.stop()

# ─────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv("spotify.csv")
    df.drop_duplicates(inplace=True)
    median_dur = df["duration"].median()
    df["duration"] = df["duration"].fillna(median_dur)
    df = df[df["duration"] >= 60]
    df["language"] = df["language"].fillna("Unknown")
    df["collaboration"] = df["collaboration"].fillna("No Collaboration")
    df.rename(columns={
        "song_id": "track_id",
        "song_title": "track_name",
        "genre": "track_genre",
        "stream": "streams",
        "explicit_content": "explicit_raw"
    }, inplace=True)
    df["explicit"] = df["explicit_raw"].map({"Yes": True, "No": False})
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["release_year"] = df["release_date"].dt.year
    df = df.dropna(subset=["release_year"])
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].str.strip()
    return df

df = load_data()

# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;padding:8px 0 16px;">'
        f'<div style="width:32px;height:32px;">{SPOTIFY_LOGO}</div>'
        f'<span style="font-size:18px;font-weight:800;color:#fff;letter-spacing:-.5px;">Spotify Analytics</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    initials = st.session_state["current_user"][0].upper()
    email_display = st.session_state["current_user"]
    st.markdown(
        f'<div class="sp-user-pill">'
        f'<div class="sp-avatar">{initials}</div>'
        f'<span class="sp-email">{email_display}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    if st.button("Log Out", use_container_width=True, key="logout_btn"):
        logout()
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    selected = option_menu(
        "Main Menu",
        ["Dataset", "Overview", "Track Analytics"],
        icons=["table", "bar-chart", "music-note-list"],
        menu_icon="spotify",
        default_index=0,
        styles={
            "container":        {"background-color": "transparent", "padding": "0"},
            "menu-title":       {"color": "#A7A7A7", "font-size": "11px", "font-weight": "700",
                                 "letter-spacing": "1.5px", "text-transform": "uppercase"},
            "menu-icon":        {"color": "#1DB954"},
            "icon":             {"color": "#A7A7A7", "font-size": "16px"},
            "nav-link":         {"color": "#A7A7A7", "font-size": "14px", "font-weight": "600",
                                 "border-radius": "6px", "padding": "10px 14px", "margin-bottom": "2px"},
            "nav-link-selected": {"background-color": "#282828", "color": "#FFFFFF"},
        }
    )

# ─────────────────────────────────────────────────────────
# Plotly dark base layout
# ─────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(24,24,24,1)",
    font=dict(family="DM Sans", color="#A7A7A7"),
    title_font=dict(family="DM Sans", color="#FFFFFF", size=16),
    xaxis=dict(gridcolor="#282828", linecolor="#282828"),
    yaxis=dict(gridcolor="#282828", linecolor="#282828"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

# ─────────────────────────────────────────────────────────
# DATASET
# ─────────────────────────────────────────────────────────
if selected == "Dataset":
    st.title("Data Explorer")
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Value", df.isna().sum().sum())
    st.divider()

    st.subheader("Select Column")
    selected_column = st.multiselect("Select Column to Display", df.columns, default=df.columns)
    filtered_df = df[selected_column]

    st.subheader("Search in Dataset")
    search_value = st.text_input("Enter Value to Search")
    if search_value:
        filtered_df = filtered_df[filtered_df.astype(str).apply(
            lambda row: row.str.contains(search_value, case=False).any(), axis=1
        )]

    st.subheader("Select Row Range")
    row_range = st.slider("Choose row range", 0, len(filtered_df), (0, min(100, len(filtered_df))))
    filtered_df = filtered_df.iloc[row_range[0]:row_range[1]]

    col1, col2 = st.columns(2)
    with col1:
        selected_col = st.selectbox("Select Column", filtered_df.columns)
    with col2:
        unique_values = ["All"] + list(filtered_df[selected_col].dropna().unique())
        selected_value = st.selectbox("Select Value", unique_values)

    if selected_value != "All":
        filtered_df = filtered_df[filtered_df[selected_col] == selected_value]

    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(label="Download Filtered Data", data=csv,
                       file_name="filtered_data.csv", mime="text/csv")

# ─────────────────────────────────────────────────────────
# OVERVIEW
# ─────────────────────────────────────────────────────────
if selected == "Overview":
    st.header("Track Overview")
    total_tracks   = len(df)
    total_streams  = df["streams"].sum()
    avg_popularity = df["popularity"].mean()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tracks",       total_tracks)
    col2.metric("Total Streams",      f"{total_streams:,.0f}")
    col3.metric("Avg Popularity",     f"{avg_popularity:.1f}")
    col4.metric("Avg Duration (sec)", f"{df['duration'].mean():.0f}s")
    st.divider()

# ─────────────────────────────────────────────────────────
# TRACK ANALYTICS
# ─────────────────────────────────────────────────────────
if selected == "Track Analytics":
    st.title("Advance Track Intelligence Dashboard")
    high_pop = df[df["popularity"] >= 70]

    st.subheader("Total Streams by Release Year")
    streams_year = df.groupby("release_year")["streams"].sum().reset_index()
    fig1 = px.line(streams_year, x="release_year", y="streams", markers=True,
                   title="Total Streams Trend (1994–2024)",
                   color_discrete_sequence=["#1DB954"])
    fig1.update_layout(height=420, **PLOTLY_LAYOUT)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("High Popularity Tracks: Genre → Label Hierarchy")
    fig2 = px.sunburst(high_pop, path=["track_genre", "label"], values="streams",
                       color="streams", color_continuous_scale="Turbo")
    fig2.update_layout(height=520, **PLOTLY_LAYOUT)
    st.plotly_chart(fig2, use_container_width=True)

    with st.container(border=True):
        bar_chart = (df.groupby("track_genre")["streams"].mean()
                     .reset_index().sort_values(by="streams", ascending=False).head(10))
        fig3 = px.bar(bar_chart, x="track_genre", y="streams", color="track_genre",
                      title="Top Genres by Average Streams")
        fig3.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig3, use_container_width=True)

    barh_chart = df["track_genre"].value_counts().head(10)
    fig4 = px.bar(barh_chart, y=barh_chart.index, x=barh_chart.values,
                  orientation='h', title="Top 10 Genres by Track Count", color=barh_chart.index)
    fig4.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig4, use_container_width=True)

    with st.container(border=True):
        st.subheader("Music Flow Analysis (Genre → Language)")
        flow = df.groupby(["track_genre", "language"]).size().reset_index(name="Count")
        source_label = flow["track_genre"].unique().tolist()
        target_label = flow["language"].unique().tolist()
        labels = source_label + target_label
        source = flow["track_genre"].apply(lambda x: labels.index(x))
        target = flow["language"].apply(lambda x: labels.index(x))
        value  = flow["Count"].tolist()
        fig5 = go.Figure(data=[go.Sankey(
            node=dict(pad=15, thickness=20,
                      line=dict(color="#1DB954", width=0.5),
                      label=labels, color="#282828"),
            link=dict(source=source, target=target, value=value,
                      color="rgba(29,185,84,0.2)")
        )])
        fig5.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig5, use_container_width=True)