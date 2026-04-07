import cv2

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        print("issur in fetching frame")
        break

    cv2.imshow("frame",frame)

    key = cv2.waitKey(1)

    if key ==ord("g"):
        grayimg = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        cv2.imwrite("grayimge.png",grayimg)
        print("gray picture saved")
    elif key ==ord("c"):
        cv2.imwrite("color.png",frame)
        print("color picture saved")
    elif key ==ord("q"):
        break



cap.release()
cv2.destroyAllWindows()