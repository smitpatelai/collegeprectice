import streamlit as st
import pandas as pd

data = {
    "Student" : ["Aman","Raj","Aaryan","Het","Yash","Smit"],
    "Course"  : ["Python","Data Science","Machine Learning","Data Analytics","Python","Machine Learning"],
    "City"    : ["Ahmedabad","Gandhinagar","Morbi","Rajkot","Jamnagar","Diu"]
}

df = pd.DataFrame(data)

# read query params

params = st.query_params
course_params = params.get("course","All")
city_params = params.get("city","All")

# filter
course = st.selectbox("Select Course",["All","Python","Data Science","Machine Learning","Data Analytics","Python","Machine Learning"],
                      index=["All","Python","Data Science","Machine Learning","Data Analytics","Python","Machine Learning"].index(course_params))

city = st.selectbox("Select City",["All","Ahmedabad","Gandhinagar","Morbi","Rajkot","Jamnagar","Diu"],
                    index=["All","Ahmedabad","Gandhinagar","Morbi","Rajkot","Jamnagar","Diu"].index(city_params))

# filter dataset
filtered_df = df.copy()

if course != "All":
    filtered_df = filtered_df[filtered_df["Course"]==course]

if city != "All":
    filtered_df = filtered_df[filtered_df["City"]==city]

st.subheader("Filtered Data")
st.dataframe(filtered_df)
st.write("Current URL Params :",course_params)