import streamlit as st

st.title("Dynamic City Map")

city = st.chat_input("Type your city here")

if city:
    st.write(f"Showing location for {city}")
    st.components.v1.iframe(f"https://google.com/maps?q={city}&t=&z=12&ie=UTF&&iwloc=&output=embed",height=500)

