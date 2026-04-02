import streamlit as st


st.title("Password Reset")

params = st.query_params
token = params.get("token")

# request reset

if not token:
    st.header("Forgot Password")
    email = st.text_input ("Enter your email")

    if st.button("Send Reset Link"):
        fake_token = "abc123"
        reset_link = f"http://localhost:8501/?token={fake_token}"
        st.success("Reset Link Generated")
        st.write(reset_link)

if token:

        st.header("Reset Your Password")
        new_password = st.text_input("Enter New Password:")
        if st.button("Update Password"):
            st. success("Password Successfully Updated")

