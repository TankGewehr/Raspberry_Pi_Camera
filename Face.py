#import numpy as np
import cv2

faceCascade=cv2.CascadeClassifier('.\haarcascade_frontalface_default.xml')  #预训练分类器

cap=cv2.VideoCapture(0)
cap.set(3,480)
cap.set(4,320)

while True:
    ret,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(10,10)
    )

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray=gray[y:y+h,x:x+w]
        roi_color=img[y:y+h,x:x+w]

    cv2.imshow('video',img)

    if cv2.waitKey(30) & 0xff==27:
        break

cap.release()
cv2.destroyAllWindows()