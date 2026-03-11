import streamlit as st
import pandas as pd
import os
import re

# page , logged in , username
if "page" not in st.session_state:
    st.session_state.page = "Login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

FILE_NAME = "userss.csv"


def signup():
    if not os.path.exists(FILE_NAME):
        df = pd.DataFrame(columns=["First_Name", "Last_Name", "Email", "Phone", "Username", "Password"])
        df.to_csv(FILE_NAME, index=False)

    with st.form("signup"):
        st.header("Sign Up")

        first_name = st.text_input("Enter First Name")
        last_name = st.text_input("Enter Last Name")
        email = st.text_input("Enter Email")
        phone = st.text_input("Enter Phone Number")
        username = st.text_input("Enter Username")
        password = st.text_input("Enter Password", type="password")
        repassword = st.text_input(" Re Enter Password", type="password")

        submit = st.form_submit_button("Sign Up")

        if submit:

            df = pd.read_csv(FILE_NAME)

            # FIX COLUMN NAME ISSUE
            df.columns = df.columns.str.replace(" ", "_")

            if not first_name or not last_name or not email or not phone or not username or not password or not repassword:
                st.error("Please fill all fields")

            elif not re.match(r"^[\w.\-]+@[\w.\-]+\w+$", email):
                st.error("Email Address Not Valid")

            elif not re.match(r"^\d{10}$", phone):
                st.error("Phone number must be 10 digits")

            elif password != repassword:
                st.error("Please Enter Correct Re Password")

            elif len(password) < 8:
                st.error("Password must be 8 characters or long")

            elif not re.search(r"[A-Z]", password):
                st.error("Password must Contain one uppercase")

            elif not re.search(r"[a-z]", password):
                st.error("Password must contain one lowercase letter")

            elif not re.search(r"[0-9]", password):
                st.error("Password must contain one number")

            elif not re.search(r"[!@#$%^&*]", password):
                st.error("Password must contain special letters")

            elif username in df["Username"].values:
                st.error("Username Already Exists")

            elif email in df["Email"].values:
                st.error("Email Address Already Exists")

            else:

                newdata = pd.DataFrame([{
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "Phone": phone,
                    "Username": username,
                    "Password": password
                }])

                # 🔧 FIX FOR InvalidIndexError (ADDED LINES)
                df = df.loc[:, ~df.columns.duplicated()]
                newdata = newdata.loc[:, ~newdata.columns.duplicated()]
                df.reset_index(drop=True, inplace=True)

                df = pd.concat([df, newdata], ignore_index=True)

                df.to_csv(FILE_NAME, index=False)

                st.success("Account created successfully")

                st.session_state.page = "Login"

                st.rerun()


def login_page():

    st.title("Login Page")

    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    if st.button("Login"):

        df = pd.read_csv("userss.csv")

        # FIX COLUMN NAME ISSUE
        df.columns = df.columns.str.replace(" ", "_")

        user = df[(df["Username"] == username) & (df["Password"] == password)]

        if not user.empty:

            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "Home"

            st.success("User logged in successdully")

            st.rerun()

        else:
            st.error("Invalid Username or Password")

    if st.button("New User? Register Here"):

        st.session_state.page = "Signup"

        st.rerun()


def home_page():

    st.title(f"WELLCOME {st.session_state.username}")

    if st.button("LOG OUT"):

        st.session_state.page = "Login"
        st.session_state.username = ""
        st.session_state.logged_in = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["Dashboard", "Profile", "Settings"])

    with tab1:

        st.header("Dashboard")

        st.write("Paheli Fursat me nikal")

    with tab2:

        st.header("Profile")

        df = pd.read_csv("userss.csv")

        # FIX COLUMN NAME ISSUE
        df.columns = df.columns.str.replace(" ", "_")

        userdata = df[df["Username"] == st.session_state.username]

        st.write(userdata)

    with tab3:

        st.header("Settings")

        st.write("Iski bhi setting he par teri nahi he")


if st.session_state.page == "Signup":
    signup()

elif st.session_state.page == "Login":
    login_page()

elif st.session_state.page == "Home":

    if st.session_state.logged_in:
        home_page()

    else:
        st.session_state.page = "Login"
        st.rerun()