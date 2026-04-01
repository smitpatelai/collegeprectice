from io import BytesIO
import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import qrcode
from gtts import gTTS

st.title("Streamlit Interactive Lab")
options = st.sidebar.selectbox( "Choose Feature",["Webcam Capture", "Drawing Canvas", "QR Code Generate",
"Text to Speech","Dashboard"])

if options == "Webcam Capture":
    st.header("Webcam Capture")

    photo = st.camera_input("Take a photo")

    if photo:
        st.image(photo, caption="Captured Photo")

if options == "Drawing Canvas":
    st.header("Drawing Canvas")
    canvas = st_canvas (
        stroke_width=5,
        stroke_color="black",
        background_color="white",
        height=300,
        width=500,
        drawing_mode="freedraw"

    )

    if canvas.image_data is not None:
        st.image(canvas. image_data)

if options == "QR Code Generate":
    st.header("QR Code Generator")
    text = st.text_input("Enter Text")

    if text:
        qr = qrcode. QRCode ()
        qr.add_data(text)
        qr.make()

        img = qr.make_image(fill_color="black",back_color="white")

        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue())

if options == "Text to Speech":
    st.header("Txt To Speech")

    text = st.text_input ("Enter Text to speak")

    if text:
        tts =gTTS(text)
        tts.save("voice.mp3")
        st.audio("voice.mp3")

if options == "Dashboard":
    data = pd.DataFrame({
        "Sales":[100,200,300],
        "Profit":[20,40,10]
    })

    chart = st.selectbox("Select Chart",["Line","Bar","Area"])
    if chart == "Line":
        st.line_chart(data)
    elif chart == "Bar":
        st.bar_chart(data)
    else:
        st.write(data)