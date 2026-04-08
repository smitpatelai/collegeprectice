import cv2

image = cv2.imread("1.jpeg")

if image is None:
    print("Error: Image not found!")
else:
    image = cv2.resize(image, (700, 700))
    cv2.putText(image,"SP Aslam",(200,50),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,2,(0,0,0),2)

cv2.imshow("Patel",image)
cv2.waitKey(0)
cv2.destroyAllWindows()