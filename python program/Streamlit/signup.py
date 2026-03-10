import streamlit as st
import pandas as pd
import os
import re

st.set_page_config(page_title="Sign UP Page")
FILE_NAME = "users.csv"
st.header("Sign UP")

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Username",
        "Password"
    ])
    df.to_csv(FILE_NAME, index=False)

if "signup_success" not in st.session_state:
    st.session_state.signup_success = False

with st.form("Signup"):
    first_name = st.text_input("Enter your First Name:", placeholder="Enter Your First Name")
    last_name = st.text_input("Enter your Last Name:", placeholder="Enter Your Last Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    re_password = st.text_input("Confirm Password", type="password")

    submit = st.form_submit_button("Sign Up")

if submit:
    if not first_name or not last_name or not email or not phone or not username or not password or not re_password:
        st.error("Please fill all details")

    elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        st.error("Invalid Email Format")

    elif not re.match(r"^\d{10}$", phone):
        st.error("Phone must be 10 digits")

    elif password != re_password:
        st.error("Passwords do not match")

    elif len(password) < 8:
        st.error("Password must be at least 8 characters long")

    elif not re.search(r"[A-Z]", password):
        st.error("Password must contain one uppercase letter")

    elif not re.search(r"[a-z]", password):
        st.error("Password must contain one lowercase letter")

    elif not re.search(r"[0-9]", password):
        st.error("Password must contain one number")

    elif not re.search(r"[!@#$%^&*]", password):
        st.error("Password must contain one special character")

    else:
        df = pd.read_csv(FILE_NAME)

        if username in df["Username"].values:
            st.error("Username already exists")
        else:
            new_user = pd.DataFrame({
                "First Name": [first_name],
                "Last Name": [last_name],
                "Email": [email],
                "Phone": [phone],
                "Username": [username],
                "Password": [password]
            })

            df = pd.concat([df, new_user], ignore_index=True)
            df.to_csv(FILE_NAME, index=False)

            st.success("Signup Successful!")