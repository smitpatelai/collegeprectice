import cv2

cap = cv2.VideoCapture(0)

# Define codec and output file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('captured_video.avi', fourcc, 20.0, (640, 480))

recording = False   # flag to control recording

print("Press 's' to START recording")
print("Press 'p' to STOP recording")
print("Press 'q' to EXIT")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Show frame always
    cv2.imshow('Recording', frame)

    key = cv2.waitKey(1) & 0xFF

    # Start recording
    if key == ord('s'):
        recording = True
        print("Recording Started...")

    # Stop recording
    elif key == ord('p'):
        recording = False
        print("Recording Stopped...")

    # Exit
    elif key == ord('q'):
        break

    # Write frame only when recording is True
    if recording:
        out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()