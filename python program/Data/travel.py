import streamlit as st

st.set_page_config(page_title="AI Travel Finder",page_icon="🌍",layout="wide")
st.title("🌍 AI Travel Finder")
st.write("Tell me your mood : **adventure,peace,hills,historical**")

#loremflicker.com
#https://loremflicker.com/WIDTH/HEIGHT/KEYWOWRD1,KEYWORD2
#free, open source, no api key, st.image()

places = {
    "adventure":{
        "place":"Manali",
        "desc":"🏔️ Perfect for trekking,paraglidding and new adventure in the himalayas",
        "images":[
            "https://loremflickr.com/800/500/manali,himalayas",
            "https://loremflickr.com/800/500/solang,valley,snow"
        ],
        "video_search":"Manali travel guide 2025"
    },
    "peace":{
        "place":"Rishikesh",
        "desc":"😇 Calm place for yoga,meditation etc",
        "images":[
            "https://loremflickr.com/800/500/rishikesh,ganga",
            "https://loremflickr.com/800/500/laxman,jhula,rishikesh"
        ],
        "video_search":"Rishikesh travel guide 2025"
    },
    "beach":{
    "place": "Goa",
    "desc":"Enjoy beaches, nightlife, water sports and food",
    "images":[
        "https://loremflickr.com/500/300/goa,beach,india",
        "https://loremflickr.com/500/300/baga,beach,sunset"
        ],
    "video_search":"Goa travel guide 2024"
    },

    "hills":{
        "place": "Matheran",
        "desc":" Enjoy Sunset and Toy Train at Matheran",
        "images": [
            "https://loremflickr.com/500/300/matheran,hills",
            "https://loremflickr.com/500/300/toytrain,matheran"
        ],
        "video_search": "Matheran travel guide 2024"
    },

    "historical" :{
        "place": "Jaipur",
        "desc": "# Forts, palaces and royal pink city",
        "images": [
            "https://loremflickr.com/500/300/amber,fort,rajasthan",
            "https://loremflickr.com/500/300/hawa,mahal,jaipur"],
    "video_search": "Jaipur travel guide 2024"
    }
}

#query
query = st.chat_input("Where do you want to go? (e.g. 'I want adventure')")
if query:
    q = query. lower ()

    for mood in places:
        if mood in q:
            data = places [mood]

            st.subheader(f"Recommended Place : {data['place' ]}")
            st.info(data["desc"])

            st.subheader("m Photos")
            cols = st.columns(2)
            for i, img_url in enumerate(data["images"]):
                cols[i].image(img_url, use_container_width=True)

            # video
            st.subheader(f"🎬 Travel Video")
            yt_search = "https://www.youtube.com/results?search_query=" + data["video_search"].replace(" ", "+")
            st.link_button(f"Watch{data['place']} | Travel video on youtube",yt_search,use_container_width=True)

            st.subheader(" Location")
            st.components.v1.iframe(f"https://google.com/maps?q={data['place']}&t=&z=12&10=UTF8&iwloc=&output=embed"
                                    , height=500)

            break

    else:
                st.warning(" Try typing : ** adventure, hills, beach, peace, historical ***" )