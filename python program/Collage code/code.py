from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(page_title="AI Startup Success Dashboard", layout="wide")

def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("stylee.css")

# -----------------------------
# LOGIN / SIGNUP SYSTEM
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if not os.path.exists("users.csv"):
    users = pd.DataFrame(columns=["username","email","password"])
    users.to_csv("users.csv",index=False)

# --------------------------------
# USER ACTIVITY LOG FILE
# --------------------------------

if not os.path.exists("user_activity.csv"):
    activity = pd.DataFrame(columns=[
        "username",
        "login_date",
        "login_time",
        "logout_time",
        "funding",
        "team_experience",
        "market_size",
        "competition",
        "business_model",
        "prediction_probability"
    ])
    activity.to_csv("user_activity.csv", index=False)


def signup():

    col1,col2,col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div class="login-container">
        <h1 class="cool-title">🚀 Create Account</h1>
        """,unsafe_allow_html=True)

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password",type="password")

        st.markdown("</div>",unsafe_allow_html=True)

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
                st.session_state.page="login"
                st.rerun()

        if st.button("Go to Login"):
            st.session_state.page="login"
            st.rerun()

def login():

    col1,col2,col3 = st.columns([1,2,1])

    with col2:

        st.markdown("""
        <div class="login-container">
        <h1 class="cool-title">🚀 Login Account</h1>
        """,unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password",type="password")

        st.markdown("</div>",unsafe_allow_html=True)

        if st.button("Login"):

            users = pd.read_csv("users.csv")

            user = users[
                (users["username"]==username) &
                (users["password"]==password)
            ]

            if not user.empty:
                st.session_state.logged_in=True
                st.session_state.username = username
                st.session_state.login_time = datetime.now()
                st.rerun()
            else:
                st.error("Invalid Username or Password")

        if st.button("Create Account"):
            st.session_state.page="signup"
            st.rerun()

# --------------------------------
# TITLE
# --------------------------------

st.title("🚀 AI Startup Success Prediction Dashboard")

if not st.session_state.logged_in:

    if st.session_state.page=="login":
        login()
    else:
        signup()

    st.stop()
st.markdown('<div class="ai-robot">🤖</div>', unsafe_allow_html=True)

st.write("Predict startup success probability using a machine learning model built from scratch.")

# --------------------------------
# CREATE DATASET
# --------------------------------

if not os.path.exists("dataset.csv"):

    np.random.seed(42)

    rows=1200

    funding=np.random.randint(50000,5000000,rows)
    team_exp=np.random.randint(1,10,rows)
    market_size=np.random.randint(1,10,rows)
    competition=np.random.randint(1,10,rows)
    business_model=np.random.randint(1,10,rows)

    score=(
        (funding/1000000*0.3)+
        (team_exp*0.25)+
        (market_size*0.2)+
        (business_model*0.2)-
        (competition*0.15)
    )

    success=(score>np.median(score)).astype(int)

    df=pd.DataFrame({
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

data=pd.read_csv("dataset.csv")
chart_data=data.copy()

X=data.drop("success",axis=1).values
y=data["success"].values.reshape(-1,1)

X[:,0]=X[:,0]/1000000

ones=np.ones((X.shape[0],1))
X=np.concatenate((ones,X),axis=1)

# --------------------------------
# SIGMOID
# --------------------------------

def sigmoid(z):
    return 1/(1+np.exp(-z))

# --------------------------------
# TRAIN MODEL
# --------------------------------

if not os.path.exists("weights.npy"):

    weights=np.zeros((X.shape[1],1))

    lr=0.01
    epochs=7000

    for i in range(epochs):

        z=np.dot(X,weights)
        predictions=sigmoid(z)

        error=predictions-y
        gradient=np.dot(X.T,error)/len(y)

        weights=weights-lr*gradient

    np.save("weights.npy",weights)

weights=np.load("weights.npy")

# --------------------------------
# MODEL ACCURACY
# --------------------------------

z=np.dot(X,weights)
pred=sigmoid(z)

pred_labels=(pred>=0.5).astype(int)

accuracy=(pred_labels==y).mean()

st.metric("Model Accuracy",f"{accuracy*100:.2f}%")

# --------------------------------
# CONFUSION MATRIX
# --------------------------------

tp=np.sum((pred_labels==1)&(y==1))
tn=np.sum((pred_labels==0)&(y==0))
fp=np.sum((pred_labels==1)&(y==0))
fn=np.sum((pred_labels==0)&(y==1))

cm=pd.DataFrame(
    [[tn,fp],[fn,tp]],
    columns=["Predicted Fail","Predicted Success"],
    index=["Actual Fail","Actual Success"]
)

st.subheader("📉 Confusion Matrix")
st.dataframe(cm)

# --------------------------------
# USER INPUT
# --------------------------------

st.subheader("🧾 Enter Startup Details")

col3,col4,col5=st.columns(3)

with col3:
    funding=st.number_input("Funding Amount ($)",min_value=0)

with col4:
    team_exp=st.slider("Team Experience",1,10)

with col5:
    market_size=st.slider("Market Size",1,10)

col6,col7=st.columns(2)

with col6:
    competition=st.slider("Competition Level",1,10)

with col7:
    business_model=st.slider("Business Model Strength",1,10)

# --------------------------------
# PREDICTION
# --------------------------------

if st.button("Predict Startup Success"):

    funding_norm=funding/1000000

    features=np.array([
        1,
        funding_norm,
        team_exp,
        market_size,
        competition,
        business_model
    ]).reshape(1,-1)

    z=np.dot(features,weights)
    prob=sigmoid(z).item()

    new_row=pd.DataFrame({
        "funding":[funding],
        "team_experience":[team_exp],
        "market_size":[market_size],
        "competition":[competition],
        "business_model":[business_model],
        "success":[1 if prob>=0.5 else 0]
    })

    chart_data=pd.concat([chart_data,new_row],ignore_index=True)

    st.subheader("Prediction Result")

    if prob>=0.5:
        st.success("✅ Startup likely to SUCCEED")
    else:
        st.error("⚠️ Startup has HIGH RISK of FAILURE")

    st.write("### Success Probability")
    st.progress(float(prob))
    st.write(f"Success Chance: {prob*100:.2f}%")

    # Save work data to activity file

    activity = pd.read_csv("user_activity.csv")

    login_date = st.session_state.login_time.strftime("%Y-%m-%d")
    login_time = st.session_state.login_time.strftime("%H:%M:%S")

    new_activity = pd.DataFrame({
        "username": [st.session_state.username],
        "login_date": [login_date],
        "login_time": [login_time],
        "logout_time": [""],
        "funding": [funding],
        "team_experience": [team_exp],
        "market_size": [market_size],
        "competition": [competition],
        "business_model": [business_model],
        "prediction_probability": [prob]
    })

    activity = pd.concat([activity, new_activity], ignore_index=True)
    activity.to_csv("user_activity.csv", index=False)

# --------------------------------
# SUCCESS GAUGE
# --------------------------------

    st.subheader("🧭 Startup Success Gauge")

    fig_gauge=go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob*100,
        title={'text':"Success Probability (%)"},
        gauge={
            'axis':{'range':[0,100]},
            'bar':{'color':"#ff00ff"},
            'steps':[
                {'range':[0,50],'color':"#ff0000"},
                {'range':[50,75],'color':"#ffff00"},
                {'range':[75,100],'color':"#00ff00"}
            ]
        }
    ))

    st.plotly_chart(fig_gauge,use_container_width=True)

# --------------------------------
# LIVE AI CONFIDENCE METER
# --------------------------------

    st.subheader("🧠 Live AI Confidence Meter")

    confidence=abs(prob-0.5)*2*100

    fig_conf=go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        title={'text':"AI Confidence Level (%)"},
        gauge={
            'axis':{'range':[0,100]},
            'bar':{'color':"#00ffe0"},
            'steps':[
                {'range':[0,40],'color':"#ff4b4b"},
                {'range':[40,70],'color':"#ffa600"},
                {'range':[70,100],'color':"#00ff7f"}
            ]
        }
    ))

    st.plotly_chart(fig_conf,use_container_width=True)

    if confidence>70:
        st.success("AI Model is Highly Confident")
    elif confidence>40:
        st.warning("AI Model has Moderate Confidence")
    else:
        st.error("AI Model Confidence is Low")

# --------------------------------
# DATA INSIGHTS
# --------------------------------

st.subheader("📊 Startup Dataset Insights")

col1,col2=st.columns(2)

with col1:
    st.write("Funding Distribution")
    st.bar_chart(chart_data["funding"])

with col2:
    success_rate=chart_data.groupby("market_size")["success"].mean()
    st.write("Market Size vs Success Rate")
    st.line_chart(success_rate)

# --------------------------------
# FEATURE IMPORTANCE
# --------------------------------

st.subheader("📈 Feature Influence")

importance=pd.DataFrame({
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
# 3D CHART
# --------------------------------

st.subheader("🌌 3D Startup Metrics Overview")

fig3d=go.Figure(data=[go.Scatter3d(
    x=chart_data['funding']/1000000,
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

st.plotly_chart(fig3d,use_container_width=True)

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

    st.session_state.logged_in = False
    st.session_state.page = "login"

    st.rerun()