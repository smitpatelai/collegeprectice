import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Style Page",options=["Home","About","Count"],menu_icon=["person"],
                           icons=["house","book"],
                           styles={
                               "container":{"padding":"Spx","background-color":"#FOFFFF"},
                               "Icon":{"color":"Orange","font-size":"20px"},
                               "nav-link":{"font-size":"16px","text-align":"left"},
                               "nav-link-selected":{"background-color":"#OOFFFF"},
                           })

if selected == "Home":
    st.title("Home")
    st.subheader("Welcome to my website")

if selected == "About":
    st.title("About")
    st.subheader("About this app")


if selected == "Count":
    st.title("Number Counter")
    num = st.number_input("Enter Number", value=0)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Increase "):
            st.write("### Output:", num + 1)
    with col2:
        if st.button("Decrease "):
            st.write("### Output:", num - 1)