import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go  # For 3D charts and gauges

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(page_title="AI Startup Success Dashboard", layout="wide")

# def load_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#
def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:  # specify UTF-8
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# -----------------------------
# LOGIN / SIGNUP SYSTEM
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# Create users database
if not os.path.exists("users.csv"):
    users = pd.DataFrame(columns=["username","email","password"])
    users.to_csv("users.csv",index=False)


def signup():

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        # st.markdown('<div class="login-container">', unsafe_allow_html=True)
        #
        # st.title(" 🚀Create Account")
        #
        # username = st.text_input("Username")
        # email = st.text_input("Email")
        # password = st.text_input("Password", type="password")

        st.markdown("""
            <div class="login-container">

            <h1 class="cool-title">🚀 Create Account</h1>

            """, unsafe_allow_html=True)

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Sign Up"):

            users = pd.read_csv("users.csv")

            if username in users["username"].values:
                st.error("Username already exists")

            else:
                new_user = pd.DataFrame({
                    "username":[username],
                    "email":[email],
                    "password":[password]
                })

                users = pd.concat([users,new_user],ignore_index=True)
                users.to_csv("users.csv",index=False)

                st.success("Account created successfully")
                st.session_state.page = "login"
                st.rerun()

        if st.button("Go to Login"):
            st.session_state.page="login"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


def login():

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
            <div class="login-container">

            <h1 class="cool-title">🚀 Login Account</h1>

            """, unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Login"):

            users = pd.read_csv("users.csv")

            user = users[
                (users["username"]==username) &
                (users["password"]==password)
            ]

            if not user.empty:
                st.session_state.logged_in=True
                st.rerun()

            else:
                st.error("Invalid Username or Password")

        if st.button("Create Account"):
            st.session_state.page="signup"
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# if st.session_state.logged_in:
st.title("🚀 AI Startup Success Prediction Dashboard")

if not st.session_state.logged_in:

    if st.session_state.page=="login":
        login()

    else:
        signup()

    st.stop()

st.write("Predict startup success probability using a machine learning model built from scratch.")

# --------------------------------
# CREATE DATASET (1000+)
# --------------------------------

if not os.path.exists("dataset.csv"):

    np.random.seed(42)

    rows = 1200

    funding = np.random.randint(50000,5000000,rows)
    team_exp = np.random.randint(1,10,rows)
    market_size = np.random.randint(1,10,rows)
    competition = np.random.randint(1,10,rows)
    business_model = np.random.randint(1,10,rows)

    score = (
        (funding/1000000*0.3) +
        (team_exp*0.25) +
        (market_size*0.2) +
        (business_model*0.2) -
        (competition*0.15)
    )

    success = (score > np.median(score)).astype(int)

    df = pd.DataFrame({
        "funding":funding,
        "team_experience":team_exp,
        "market_size":market_size,
        "competition":competition,
        "business_model":business_model,
        "success":success
    })

    df.to_csv("dataset.csv",index=False)

# --------------------------------
# LOAD DATA
# --------------------------------

data = pd.read_csv("dataset.csv")

X = data.drop("success",axis=1).values
y = data["success"].values.reshape(-1,1)

# Normalize funding
X[:,0] = X[:,0]/1000000

# Add bias column
ones = np.ones((X.shape[0],1))
X = np.concatenate((ones,X),axis=1)

# --------------------------------
# SIGMOID FUNCTION
# --------------------------------

def sigmoid(z):
    return 1/(1+np.exp(-z))

# --------------------------------
# TRAIN MODEL
# --------------------------------

if not os.path.exists("weights.npy"):

    weights = np.zeros((X.shape[1],1))

    lr = 0.01
    epochs = 7000

    for i in range(epochs):

        z = np.dot(X,weights)
        predictions = sigmoid(z)

        error = predictions - y
        gradient = np.dot(X.T,error)/len(y)

        weights = weights - lr*gradient

    np.save("weights.npy",weights)

weights = np.load("weights.npy")

# --------------------------------
# MODEL ACCURACY
# --------------------------------

z = np.dot(X,weights)
pred = sigmoid(z)

pred_labels = (pred >= 0.5).astype(int)

accuracy = (pred_labels == y).mean()

st.metric("Model Accuracy",f"{accuracy*100:.2f}%")

# --------------------------------
# CONFUSION MATRIX
# --------------------------------

tp = np.sum((pred_labels==1) & (y==1))
tn = np.sum((pred_labels==0) & (y==0))
fp = np.sum((pred_labels==1) & (y==0))
fn = np.sum((pred_labels==0) & (y==1))

cm = pd.DataFrame(
    [[tn,fp],[fn,tp]],
    columns=["Predicted Fail","Predicted Success"],
    index=["Actual Fail","Actual Success"]
)

st.subheader("📉 Confusion Matrix")
st.dataframe(cm)

# --------------------------------
# DATA INSIGHTS
# --------------------------------

st.subheader("📊 Startup Dataset Insights")

col1,col2 = st.columns(2)

with col1:
    st.write("Funding Distribution")
    st.bar_chart(data["funding"])

with col2:
    success_rate = data.groupby("market_size")["success"].mean()
    st.write("Market Size vs Success Rate")
    st.line_chart(success_rate)

# --------------------------------
# FEATURE IMPORTANCE
# --------------------------------

st.subheader("📈 Feature Influence")

importance = pd.DataFrame({
    "Feature":[
        "Funding",
        "Team Experience",
        "Market Size",
        "Competition",
        "Business Model"
    ],
    "Weight":weights[1:].flatten()
})

st.bar_chart(importance.set_index("Feature"))

# --------------------------------
# 3D SCATTER PLOT (Futuristic)
# --------------------------------

st.subheader("🌌 3D Startup Metrics Overview")

fig3d = go.Figure(data=[go.Scatter3d(
    x=data['funding']/1000000,
    y=data['team_experience'],
    z=data['market_size'],
    mode='markers',
    marker=dict(
        size=7,
        color=data['success'],
        colorscale='Viridis',
        opacity=0.9,
        line=dict(width=1, color='white')
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
# USER INPUT
# --------------------------------

st.subheader("🧾 Enter Startup Details")

col3,col4,col5 = st.columns(3)

with col3:
    funding = st.number_input("Funding Amount ($)",min_value=0)

with col4:
    team_exp = st.slider("Team Experience",1,10)

with col5:
    market_size = st.slider("Market Size",1,10)

col6,col7 = st.columns(2)

with col6:
    competition = st.slider("Competition Level",1,10)

with col7:
    business_model = st.slider("Business Model Strength",1,10)

# --------------------------------
# PREDICTION
# --------------------------------

if st.button("Predict Startup Success"):

    funding = funding/1000000

    features = np.array([
        1,
        funding,
        team_exp,
        market_size,
        competition,
        business_model
    ]).reshape(1,-1)

    z = np.dot(features,weights)
    prob = sigmoid(z).item()

    st.subheader("Prediction Result")

    if prob >= 0.5:
        st.success("✅ Startup likely to SUCCEED")
    else:
        st.error("⚠️ Startup has HIGH RISK of FAILURE")

    st.write("### Success Probability")
    st.progress(float(prob))
    st.write(f"Success Chance: {prob*100:.2f}%")

    # --------------------------------
    # SUCCESS GAUGE (Futuristic)
    # --------------------------------

    st.subheader("🧭 Startup Success Gauge")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=prob*100,
        title={'text': "Success Probability (%)", 'font': {'color': '#00ffe0'}},
        gauge={
            'axis': {'range': [0,100], 'tickcolor':'#00ffe0'},
            'bar': {'color': "#ff00ff"},
            'bgcolor': "rgba(0,0,0,0.3)",
            'steps': [
                {'range': [0,50], 'color': "#ff0000"},
                {'range': [50,75], 'color': "#ffff00"},
                {'range': [75,100], 'color': "#00ff00"}
            ],
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness':0.75, 'value': prob*100}
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

    # --------------------------------
    # INVESTOR RECOMMENDATION
    # --------------------------------

    st.subheader("💰 Investor Recommendation")

    if prob > 0.75:
        st.success("Strong investment opportunity")
    elif prob > 0.55:
        st.warning("Moderate potential – evaluate carefully")
    else:
        st.error("High risk – investment not recommended")

# --------------------------------
# DATASET PREVIEW
# --------------------------------

st.subheader("📂 Dataset Preview")

st.dataframe(data.head(50))

if st.button("Logout"):
    st.session_state.logged_in=False
    st.session_state.page="login"
    st.rerun()
