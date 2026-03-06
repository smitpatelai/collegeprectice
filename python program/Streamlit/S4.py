import streamlit as st
from streamlit_option_menu import option_menu

if "count" not in st.session_state:
    st.session_state.count = 0

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = 0
with st.sidebar:
    selected = option_menu("Counter Web",options=["Home","Count"],
                           icons=["house","plus-circle"])

if selected == "Home":
    st.title("Home")
    st.subheader("Welcome to the home page")

elif selected == "Count":
    st.header("Counter")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Increase"):
            st.session_state.count += 1
            st.session_state.button_clicked += 1

    with col2:
        if st.button("Decrease"):
            st.session_state.count -= 1
            st.session_state.button_clicked += 1

    st.write(f"Session Count: {st.session_state.count}")
    st.write(f"Session Button Clicked: {st.session_state.button_clicked}")

