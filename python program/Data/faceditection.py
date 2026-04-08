import numpy as np
import cv2

canvas = np.ones((600,600,3), dtype="uint8")*255

cv2.line(canvas,(0,0),(600,600),(0,0,255),5)


cv2.rectangle(canvas,(0,0),(600,600),(0,0,255),5)

cv2.rectangle(canvas,(40,40),(400,200),(0,157,255),5)


cv2.circle(canvas,(400,400),50,(140,90,255),5)

cv2.arrowedLine(canvas,(200,400),(200,300),(10,60,255),5)

cv2.putText(canvas,"Patel",(100,200),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,3,(140,190,255),5)


cv2.imshow("Canvas", canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()