import streamlit as st
import pandas as pd
import os

FILE_NAME = "student.csv"

#-----------------css----------
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")
# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = "Login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# ---------- FILE CREATION ----------
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "First_Name","Last_Name","Email","Phone",
        "Student_ID","Course","Year","Department",
        "Username","Password"
    ])
    df.to_csv(FILE_NAME,index=False)


# ---------- SIGNUP ----------
def signup():

    with st.form("signup"):

        st.title("Student Registration")

        col1,col2 = st.columns(2)

        with col1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")

        with col2:
            student_id = st.text_input("Student ID")
            course = st.selectbox("Course",
                        ["B.Tech","BCA","MCA","M.Tech"])
            year = st.selectbox("Year",
                        ["1","2","3","4"])
            department = st.selectbox("Department",
                        ["Computer Science","IT","AI","Data Science"])

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        repassword = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button("Register")

        if submit:

            df = pd.read_csv(FILE_NAME)

            if password != repassword:
                st.error("Passwords do not match")

            elif username in df["Username"].values:
                st.error("Username already exists")

            elif email in df["Email"].values:
                st.error("Email already exists")

            else:

                new_user = pd.DataFrame([{
                    "First_Name":first_name,
                    "Last_Name":last_name,
                    "Email":email,
                    "Phone":phone,
                    "Student_ID":student_id,
                    "Course":course,
                    "Year":year,
                    "Department":department,
                    "Username":username,
                    "Password":password
                }])

                df = pd.concat([df,new_user],ignore_index=True)
                df.to_csv(FILE_NAME,index=False)

                st.success("Registration successful")

                st.session_state.page="Login"
                st.rerun()

    if st.button("Already Registered? Login"):
        st.session_state.page="Login"
        st.rerun()


# ---------- LOGIN ----------
def login_page():

    st.title("Student Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        df = pd.read_csv(FILE_NAME)

        user = df[(df["Username"]==username) &
                  (df["Password"]==password)]

        if not user.empty:

            st.session_state.logged_in=True
            st.session_state.username=username
            st.session_state.page="Home"

            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid username or password")

    if st.button("New Student? Register"):
        st.session_state.page="Signup"
        st.rerun()


# ---------- HOME PAGE ----------
def home_page():

    st.title(f"Welcome {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.logged_in=False
        st.session_state.username=""
        st.session_state.page="Login"
        st.rerun()

    tab1,tab2 = st.tabs(["Profile","Settings"])

    df = pd.read_csv(FILE_NAME)
    user = df[df["Username"]==st.session_state.username]

    with tab1:
        st.header("Student Profile")
        st.dataframe(user)

    with tab2:
        st.header("Settings")
        st.write("Settings panel coming soon")


# ---------- PAGE ROUTER ----------
if st.session_state.page=="Login":
    login_page()

elif st.session_state.page=="Signup":
    signup()

elif st.session_state.page=="Home":
    if st.session_state.logged_in:
        home_page()
    else:
        st.session_state.page="Login"
        st.rerun()