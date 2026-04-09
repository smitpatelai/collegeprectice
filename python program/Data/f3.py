import streamlit as st
import cv2

st.title(" Live Camera - Face Detection")

# Load Haarcascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Checkbox
run = st.checkbox("Start Camera")

frame_placeholder = st.empty()

if run:
    cap = cv2.VideoCapture(0)

    while run:
        ret, frame = cap.read()

        if not ret:
            st.error("Camera not working")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        # Draw rectangles
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        # Show frame
        frame_placeholder.image(frame, channels="BGR")

        # Small delay (important)
        key= cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

else:
    st.write("Camera is OFF")