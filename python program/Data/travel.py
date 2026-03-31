import streamlit as st

st.set_page_config(page_title="AI Travel Finder",page_icon="🌍",layout="wide")
st.title("🌍 AI Travel Finder")
st.write("Tell me your mood: **adventure,peace,beach,hills,historical**")

places = {
    "adventure":{
        "place":"Manali",
        "desc":"🗻 perfect for trekking.paragliding and new adventure in the Himalayas",
        "images":[
            "https://loremflickr.com/800/500/"
        ]
    }
}