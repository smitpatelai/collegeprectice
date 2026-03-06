import streamlit as st
import pandas as pd
from altair import Title
from streamlit_option_menu import option_menu

with st.sidebar:
    selection = option_menu("Administration",options=["Home","About","dataset","Settings"],
                            icons=["house","people","table","gear"],menu_icon="person",default_index=0)

if selection == "Home":
    st.title("Project Title")
    st.subheader("Sub Head")
    st.write("Description")

elif selection == "About":
    st.title("About")
    st.subheader("Sub Head")
    st.write("Description")

elif selection == "dataset":
    df = pd.read_csv("workforce_data.csv")
    st.dataframe(df)

elif selection == "Details":
    st.title("FiLl the form")
    with st.form("student_form"):

        name = st.text_input("Enter Student Name")

        age = st.number_input("Enter Age", min_value=10, max_value=30)

        address = st.text_area("Enter Address")

        course = st.selectbox("Select Course", ["BE", "BCA", "B.Tech", "BSC"])

        gender = st.radio("Select Gender", ["Male", "Female", "Other"])

        hostel = st.checkbox("Need Hostel Facility")

        skills = st.multiselect(
            "Select Skills",
            ["Python", "SQL", "Java", "C++", "Machine Learning", "ReactJS"]
        )

        rating = st.slider("Programming Skill Level", 0, 10)

        dob = st.date_input("Date of Birth")

        time = st.time_input("Class Time")

        photo = st.file_uploader("Upload Student Photo")

        fav_color = st.color_picker("Select Favorite Color")

        submit = st.form_submit_button("Submit")

    if submit:
        st.success("Form Submitted Successfully!")

        st.write("### Student Details")
        st.write("Name:", name)
        st.write("Age:", age)
        st.write("Address:", address)
        st.write("Course:", course)
        st.write("Gender:", gender)
        st.write("Hostel:", hostel)
        st.write("Skills:", skills)
        st.write("Skill Rating:", rating)
        st.write("DOB:", dob)
        st.write("Class Time:", time)
        st.write("Favorite Color:", fav_color)

        if photo:
            st.image(photo, caption="Uploaded Photo")

    elif selection == "Settings":
        st.title("Settings")
        st.write("Student details are in dataset")
        st.write("For student form select details option")
