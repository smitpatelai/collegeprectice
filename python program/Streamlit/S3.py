import streamlit as st
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Style Page",options=["Home","About"],menu_icon=["person"],
                           icons=["house","book"],
                           styles={
                               "container":{"padding":"Spx","background-color":"#FOFFFF"},
                               "Icon":{"color":"Orange","font-size":"20px"},
                               "nav-link":{"font-size":"16px","text-align":"left"},
                               "nav-link-selected":{"background-color":"#OOFFFF"},
                           })

if selected == "Home":
    st.title("Home")

