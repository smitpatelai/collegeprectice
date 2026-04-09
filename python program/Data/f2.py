import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")

img = cv2.imread("img_1.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces_detect = face_cascade.detectMultiScale(gray,1.1,3)

print(faces_detect)

for (x,y,w,h) in faces_detect:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()