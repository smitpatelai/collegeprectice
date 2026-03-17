import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide",page_title="Role Base Login")
# users , current_user , logged in

if "users" not in st.session_state:
    st.session_state. users = []

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "logged_in" not in st.session_state:
    st.session_state. logged_in = False

# username | password | role
def register():
    st.session_state. users. append(({"username":st.session_state.reg_user, "password":st. session_state.reg_passwor,
        "role":st.session_state.reg_role}))

    st.success("Registration Successfull")


def login():
    for user in st.session_state.users:
        if user["username"] == st.session_state. log_user and user["password"] == st.session_state. Log_pass:
            st.session_state. logged_in = True
            st.session_state.current_user = user
            return

    else:
        st.error("Invalid Credentials")

