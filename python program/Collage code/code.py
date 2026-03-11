import streamlit as st
import numpy as np
import pandas as pd
import os

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(page_title="AI Startup Success Dashboard", layout="wide")

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")
st.title("🚀 AI Startup Success Prediction Dashboard")
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