import streamlit as st
import pandas as pd
import os

st.set_page_config("Sign UP Page")
FILE_NAME = "users. csv"
st.header("Sign UP")
if not os.path.exists(FILE_NAME) :
    df = pd. DataFrame(columns=[
        "First Name"
        "Last Name"
        "Email",
        "Phone",
        "Username",
        "Password"
    ])
    df.to_csv(FILE_NAME, index=False)

if "signup_success" not in st.session_state:
    st.session_state.signup_success = False

with st.form("Signup") :
    first_name = st.text_input ( "Enter your First Name:", placeholder="Enter Your First Name")
    last_name = st.text_input ( "Enter your Last Name: ", placeholder="Enter Your Last Name")
    email = st.text_input ("Email")
    phone = st.text_input("phone")
    username = st.text_input ("UserName")
    password = st.text_input ( "Password", type="password")
    re_password = st.text_input ( "Confirm Password", type="password")
    submit = st.form_submit_button("sign up")

