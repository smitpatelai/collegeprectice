import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
st.set_page_config(page_title="Student Information")
with st.sidebar:
    selection = option_menu(
        "Information",
        options=["Home","About","Dataset","Details","Setting"],
        icons=["house","people","table","list","gear"],
        menu_icon="person",
        default_index=0
    )
# Home
if selection == "Home":
    st.title("Project Title")
    st.subheader("Sub Head")
    st.write("Description")

# About
elif selection == "About":
    st.header("About Us")
    st.write("This project shows student information using Streamlit.")

# Dataset
elif selection == "Dataset":
    df = pd.read_csv("students.csv")
    st.dataframe(df)
# Details Section
elif selection == "Details":
    st.header("Student Details Form")
    with st.form("student_form"):
        name = st.text_input("1. Student Name")
        student_id = st.number_input("2. Student ID", min_value=1)
        age = st.number_input("3. Age", min_value=16, max_value=30)
        email = st.text_input("4. Email Address")
        department = st.selectbox(
            "5. Department",
            ["Mathematics", "Physics", "Chemistry", "Computer Science", "Biology"]
        )
        subjects = st.multiselect(
            "6. Subjects",
            ["Python", "Statistics", "AI", "Data Science", "Math"]
        )
        gender = st.radio(
            "7. Gender",
            ["Male", "Female", "Other"]
        )
        attendance = st.slider(
            "8. Attendance (%)",
            0, 100
        )
        dob = st.date_input("9. Date of Birth")
        class_time = st.time_input("10. Class Time")
        address = st.text_area("11. Address")
        result = st.file_uploader("12. Upload Document",["jpg","jpeg","png","pdf"])
        check = st.checkbox("I Agree  Terms and Conditions")
        submit = st.form_submit_button("Submit")
        if submit:
            st.success("Form Submitted Successfully!")
# Setting
elif selection == "Setting":
    st.header("Settings")
    st.write("Application settings will appear here.")