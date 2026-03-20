from datetime import datetime
import streamlit as st
import numpy as np
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.express as px

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(page_title="AI Startup Success Dashboard", layout="wide")

def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("stylle.css")

# -----------------------------
# LOGIN / SIGNUP SYSTEM
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

if "role" not in st.session_state:   # ✅ ADD HERE
    st.session_state.role = "user"

if not os.path.exists("users.csv"):
    users = pd.DataFrame(columns=["username","email","password"])
    users.to_csv("users.csv",index=False)
# --------------------------------
# ADMIN FILE
# --------------------------------
if not os.path.exists("admin.csv"):
    admin = pd.DataFrame(columns=["username","email","password"])
    admin.to_csv("admin.csv", index=False)

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
        <h1 class="cool-title">👤 Create Account</h1>
        """,unsafe_allow_html=True)

        role = st.selectbox("Account Type", ["User","Admin"])  # ✅ ADDED HERE

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password",type="password")

        st.markdown("</div>",unsafe_allow_html=True)

        if st.button("Sign Up"):

            if role == "User":

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

                    st.success("User Account created")
                    st.session_state.page="login"
                    st.rerun()

            else:  # ADMIN SIGNUP

                admin = pd.read_csv("admin.csv")

                if username in admin["username"].values:
                    st.error("Admin already exists")

                else:
                    new_admin = pd.DataFrame({
                        "username":[username],
                        "email":[email],
                        "password":[password]
                    })

                    admin = pd.concat([admin,new_admin],ignore_index=True)
                    admin.to_csv("admin.csv",index=False)

                    st.success("Admin Account created")
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
        <h1 class="cool-title">👤 Login Account</h1>
        """,unsafe_allow_html=True)

        role = st.selectbox("Login As", ["User","Admin"])  # ✅ ADDED

        username = st.text_input("Username")
        password = st.text_input("Password",type="password")

        st.markdown("</div>",unsafe_allow_html=True)

        if st.button("Login"):

            if role == "User":

                users = pd.read_csv("users.csv")

                user = users[
                    (users["username"]==username) &
                    (users["password"]==password)
                ]

                if not user.empty:
                    st.session_state.logged_in=True
                    st.session_state.username = username
                    st.session_state.role = "user"
                    st.session_state.login_time = datetime.now()
                    st.rerun()
                else:
                    st.error("Invalid User Credentials")

            else:  # ADMIN LOGIN

                admin = pd.read_csv("admin.csv")

                admin_user = admin[
                    (admin["username"]==username) &
                    (admin["password"]==password)
                ]

                if not admin_user.empty:
                    st.session_state.logged_in=True
                    st.session_state.username = username
                    st.session_state.role = "admin"
                    st.session_state.login_time = datetime.now()
                    st.rerun()
                else:
                    st.error("Invalid Admin Credentials")

        if st.button("Create Account"):
            st.session_state.page="signup"
            st.rerun()
# --------------------------------
# ADMIN PANEL
# --------------------------------
if st.session_state.role == "admin":

    st.markdown(f"""
    <h1 style='text-align:center; color:red;'>
    👑 Admin Dashboard - {st.session_state.username}
    </h1>
    """, unsafe_allow_html=True)

    users_df = pd.read_csv("users.csv")
    activity_df = pd.read_csv("user_activity.csv")

    # --------------------------------
    # SUMMARY CARDS
    # --------------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("👤 Total Users", len(users_df))
    col2.metric("📊 Total Predictions", len(activity_df))
    col3.metric("🔥 Avg Success Rate",
                f"{activity_df['prediction_probability'].mean()*100:.2f}%" if not activity_df.empty else "0%")

    # --------------------------------
    # TABS
    # --------------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👤 Users",
        "📊 Activity",
        "📈 Charts",
        "📂 Raw Data",
        "🧠 AI Insights"
    ])

    # --------------------------------
    # USERS TAB
    # --------------------------------
    with tab1:
        st.subheader("Registered Users")
        st.dataframe(users_df)

    # --------------------------------
    # ACTIVITY TAB
    # --------------------------------
    with tab2:
        st.subheader("User Activity Logs")
        st.dataframe(activity_df)

    # --------------------------------
    # CHARTS TAB
    # --------------------------------
    with tab3:

        if not activity_df.empty:

            st.subheader("📊 Prediction Distribution")

            fig1 = px.histogram(
                activity_df,
                x="prediction_probability",
                nbins=20,
                title="Prediction Probability Distribution"
            )
            st.plotly_chart(fig1, use_container_width=True)

            st.subheader("📈 User Activity Count")

            user_counts = activity_df["username"].value_counts()

            fig2 = px.bar(
                x=user_counts.index,
                y=user_counts.values,
                labels={'x':'Username','y':'Predictions'},
                title="Predictions per User"
            )
            st.plotly_chart(fig2, use_container_width=True)

            st.subheader("📉 Success vs Failure")

            activity_df["result"] = activity_df["prediction_probability"].apply(
                lambda x: "Success" if x >= 0.5 else "Failure"
            )

            result_counts = activity_df["result"].value_counts()

            fig3 = px.pie(
                names=result_counts.index,
                values=result_counts.values,
                hole=0.6  # more donut look
            )

            # --------------------------------
            # DONUT CHART (ADD HERE)
            # --------------------------------
            st.subheader("🍩 User Contribution (Donut Chart)")

            user_counts = activity_df["username"].value_counts()

            fig_donut = px.pie(
                names=user_counts.index,
                values=user_counts.values,
                hole=0.5
            )

            st.plotly_chart(fig_donut, use_container_width=True)
            st.plotly_chart(fig3, use_container_width=True)

        else:
            st.warning("No activity data available")

    # --------------------------------
    # RAW DATA TAB
    # --------------------------------
    with tab4:

        st.subheader("Download Data")

        st.download_button(
            "Download Users CSV",
            users_df.to_csv(index=False),
            "users.csv"
        )

        st.download_button(
            "Download Activity CSV",
            activity_df.to_csv(index=False),
            "activity.csv"
        )
    #-----------------------------------
    #AI TAB
    #-----------------------------------
    with tab5:

        st.subheader("🤖 AI-Based Insights")

        activity_df = pd.read_csv("user_activity.csv")

        if not activity_df.empty:

            #------------
            #
            #------------
            selected_user = st.selectbox(
                "Filter by User",
                ["All"] + list(activity_df["username"].unique())
            )

            if selected_user != "All":
                activity_df = activity_df[activity_df["username"] == selected_user]

            #-------------------------------
            #
            #-------------------------------
            st.subheader("🚀 Top Startup Predictions")

            top_startups = activity_df.sort_values(
                by="prediction_probability",
                ascending=False
            )

            st.dataframe(top_startups.head(10))
            #--------------------------------
            #
            #----------------------------------
            st.subheader("⚡ Risk Level Classification")


            def risk_level(prob):
                if prob > 0.7:
                    return "Low Risk"
                elif prob > 0.4:
                    return "Medium Risk"
                else:
                    return "High Risk"


            activity_df["risk_level"] = activity_df["prediction_probability"].apply(risk_level)

            risk_counts = activity_df["risk_level"].value_counts()

            fig_risk = px.pie(
                names=risk_counts.index,
                values=risk_counts.values,
                hole=0.5
            )

            st.plotly_chart(fig_risk, use_container_width=True)

            # --------------------------------
            # 1. SUCCESS RATE
            # --------------------------------
            success_rate = (activity_df["prediction_probability"] >= 0.5).mean()

            st.metric("Overall Success Rate", f"{success_rate * 100:.2f}%")

            # --------------------------------
            # 2. HIGH RISK STARTUPS
            # --------------------------------
            high_risk = activity_df[activity_df["prediction_probability"] < 0.4]

            st.subheader("⚠️ High Risk Startups")
            st.dataframe(high_risk.head(10))

            # --------------------------------
            # 3. TOP PERFORMING USERS
            # --------------------------------
            st.subheader("🏆 Top Users")

            top_users = activity_df.groupby("username")["prediction_probability"].mean().sort_values(ascending=False)

            st.dataframe(top_users.head(5))

            # --------------------------------
            # 4. FEATURE IMPACT (AI LOGIC)
            # --------------------------------
            st.subheader("📈 Feature Impact Analysis")

            corr = activity_df[[
                "funding",
                "team_experience",
                "market_size",
                "competition",
                "business_model",
                "prediction_probability"
            ]].corr()

            fig_corr = px.imshow(
                corr,
                text_auto=True,
                title="Feature Correlation Heatmap"
            )

            st.plotly_chart(fig_corr, use_container_width=True)

            # --------------------------------
            # 5. TREND ANALYSIS
            # --------------------------------
            st.subheader("📊 Prediction Trend Over Time")

            activity_df["index"] = range(len(activity_df))

            fig_trend = px.line(
                activity_df,
                x="index",
                y="prediction_probability",
                title="Prediction Trend"
            )

            st.plotly_chart(fig_trend, use_container_width=True)
            #------------------------------------------
            #look like trend chart
            #---------------------------------------
            st.subheader("📅 User Activity Trend (Candlestick Style)")

            # Convert to datetime
            activity_df["login_date"] = pd.to_datetime(activity_df["login_date"])

            # Group by date and count logins
            daily_activity = activity_df.groupby("login_date").size().reset_index(name="count")

            # Create OHLC-style data
            daily_activity["open"] = daily_activity["count"].shift(1)
            daily_activity["close"] = daily_activity["count"]
            daily_activity["high"] = daily_activity[["open", "close"]].max(axis=1)
            daily_activity["low"] = daily_activity[["open", "close"]].min(axis=1)

            # Fill first row NaN
            daily_activity.fillna(method="bfill", inplace=True)

            # Create candlestick chart
            fig = go.Figure(data=[go.Candlestick(
                x=daily_activity["login_date"],
                open=daily_activity["open"],
                high=daily_activity["high"],
                low=daily_activity["low"],
                close=daily_activity["close"]
            )])

            # Optional: dark hacker-style UI
            fig.update_layout(
                title="User Activity Candlestick Trend",
                xaxis_title="Date",
                yaxis_title="Login Count",
                template="plotly_dark"
            )

            # Show in Streamlit
            st.plotly_chart(fig, use_container_width=True)

            fig.update_layout(
                font=dict(family="Courier New", size=14),
                title_font=dict(size=20),
            )

            st.subheader("📅 User Activity Trend")
            activity_df["login_date"] = pd.to_datetime(activity_df["login_date"])
            daily_activity = activity_df.groupby("login_date").size()
            fig_activity = px.line(x=daily_activity.index, y=daily_activity.values)
            st.plotly_chart(fig_activity, use_container_width=True)


            # --------------------------------
            # 6. AI TEXT INSIGHTS
            # --------------------------------
            st.subheader("🧠 Smart Insights")

            avg_prob = activity_df["prediction_probability"].mean()

            if avg_prob > 0.6:
                st.success("📈 Most startups show strong success potential.")
            elif avg_prob > 0.4:
                st.warning("⚖️ Startups have moderate success chances.")
            else:
                st.error("⚠️ Many startups are at high risk of failure.")

            st.info("💡 Insight: Increase funding + team experience to improve success rate.")

        else:
            st.warning("No activity data available")

    # --------------------------------
    # LOGOUT
    # --------------------------------
    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.username = ""
        st.session_state.role = "user"

        st.rerun()

    st.stop()

# --------------------------------
# TITLE
# --------------------------------

if not st.session_state.logged_in:

    st.markdown("""
    <h1 style='text-align: center; 
               font-size: 48px; 
               font-weight: bold;
               color: white;'>
    🚀 AI Startup Success Prediction Dashboard
    </h1>
    """, unsafe_allow_html=True)
    if st.session_state.page=="login":
        login()
    else:
        signup()

    st.stop()

st.markdown(f"""
<h1 style='text-align:center; color:#00f7ff;'>
👤 Welcome {st.session_state.username}
</h1>
""", unsafe_allow_html=True)

st.markdown('<div class="radar"></div>', unsafe_allow_html=True)

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

st.markdown('<div class="glow-card">🚀 Enter Your Startup Data</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="glow-card">🤖 AI Analysis Running...</div>', unsafe_allow_html=True)

    if prob>=0.5:
        st.success("✅ Startup likely to SUCCEED")
    else:
        st.error("⚠️ Startup has HIGH RISK of FAILURE")

    st.write("### Success Probability")
    st.progress(float(prob))
    st.write(f"Success Chance: {prob*100:.2f}%")
    st.markdown(f"""
    <div class="energy-bar">
        <div class="energy-fill" style="width:{prob * 100}%"></div>
    </div>
    """, unsafe_allow_html=True)

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
#------------------------------
#Donat chart
#-----------------------------

st.subheader("🍩 Your Prediction Stats")
st.markdown('<div class="glow-card">📊 Your Performance Analytics</div>', unsafe_allow_html=True)

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
#----------------
#parformance
#----------------
st.subheader("📊 Your Performance")

if not user_data.empty:
    avg_prob = user_data["prediction_probability"].mean()

    st.metric("Your Avg Success Rate", f"{avg_prob*100:.2f}%")
    st.markdown(f"""
    <div class="energy-bar">
        <div class="energy-fill" style="width:{avg_prob * 100}%"></div>
    </div>
    """, unsafe_allow_html=True)

    st.metric("Total Predictions", len(user_data))
#--------------
#growth trend
#--------------
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

#----------------------------
#ai suggestions
#-------------
st.subheader("🤖 Personalized AI Suggestions")

if not user_data.empty:

    avg_funding = user_data["funding"].mean()
    avg_team = user_data["team_experience"].mean()

    if avg_funding < 1000000:
        st.warning("💡 Try increasing funding for better results")

    if avg_team < 5:
        st.warning("💡 Improve team experience")

    if user_data["competition"].mean() > 6:
        st.error("⚠️ High competition — choose a niche market")

    st.success("✅ Strong business model increases success chances")


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
# STARTUP MARKET TREND (STOCK STYLE)
# --------------------------------

st.subheader("📈 Startup Market Trend")

chart_data["startup_index"] = (
    chart_data["funding"]/1000000 +
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
st.plotly_chart(fig3d,use_container_width=True)

#------------------
#History
#------------------
st.subheader("📂 Your Prediction History")

if not user_data.empty:
    st.dataframe(user_data.tail(10))
#--------------------
#Achievement
#------------------
st.subheader("🏆 Your Achievement")

if not user_data.empty:

    avg_prob = user_data["prediction_probability"].mean()

    if avg_prob > 0.7:
        st.success("🥇 Pro Founder")
    elif avg_prob > 0.5:
        st.info("🥈 Growing Entrepreneur")
    else:
        st.warning("🥉 Beginner Level")

#--------------------
# Download
#--------------------
st.download_button(
    "📥 Download My Report",
    user_data.to_csv(index=False),
    "my_startup_report.csv"
)

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
    st.session_state.username = ""
    st.session_state.role = "user"

    st.rerun()