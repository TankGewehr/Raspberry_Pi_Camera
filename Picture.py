import numpy as np
import cv2

#cap=cv2.VideoCapture(0)
#cap.set(3,480)
#cap.set(4,320)

img=cv2.imread('.\icons\example.jpg')

while True:
    #ret,img=cap.read()
    cv2.imshow('Picture',img)
    if cv2.waitKey(30) & 0xff==27:
        break

#cap.release()
cv2.destroyAllWindows()