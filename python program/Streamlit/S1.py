import streamlit as st

st.set_page_config("Basics", page_icon="😊")

st.title("Infolabz")
st.header("Internship of data science")
st.subheader("Infolabz")
st.write("Streamlit basics")
st.text("This is Next")

#input
name = st.text("Enter Name:")
age = st.number_input("Enter Age:")

#checkbox
check = st.checkbox("I agree terms and conditions")

#select
select = st.selectbox("Enter Skill",["AI","DS","DA"])

st.button("Click Me")