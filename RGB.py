import numpy as np
import cv2

img_path=".\icons\example.jpg"
img=cv2.imread(img_path)
img2=cv2.imread(img_path)
(B,G,R)=cv2.split(img2)
Light=0.3
Contrast=80
r=1
g=1
b=1

#def nothing(x):
    #pass

def updateR(x):
    global r,R,img,img2
    r=cv2.getTrackbarPos('R','RGB')
    r*=0.01
    img=cv2.merge([np.uint8(np.clip((B*b),0,255)),np.uint8(np.clip((G*g),0,255)),np.uint8(np.clip((R*r),0,255))])

def updateG(x):
    global g,G,img,img2
    g=cv2.getTrackbarPos('G','RGB')
    g*=0.01
    img=cv2.merge([np.uint8(np.clip((B*b),0,255)),np.uint8(np.clip((G*g),0,255)),np.uint8(np.clip((R*r),0,255))])

def updateB(x):
    global b,B,img,img2
    b=cv2.getTrackbarPos('B','RGB')
    b*=0.01
    img=cv2.merge([np.uint8(np.clip((B*b),0,255)),np.uint8(np.clip((G*g),0,255)),np.uint8(np.clip((R*r),0,255))])

def updateLight(x):
    global Light,img,img2
    Light=cv2.getTrackbarPos('Light','RGB')
    Light=Light*0.01
    img=np.uint8(np.clip((Light*img2+Contrast),0,255))

def updateContrast(x):
    global Contrast,img,img2
    Contrast=cv2.getTrackbarPos('Contrast','RGB')
    img=np.uint8(np.clip((Light*img2+Contrast),0,255))

cv2.namedWindow('RGB')
cv2.createTrackbar('Light','RGB',0,300,updateLight)
cv2.createTrackbar('Contrast','RGB',0,255,updateContrast)
cv2.createTrackbar('R','RGB',0,300,updateR)
cv2.createTrackbar('G','RGB',0,300,updateG)
cv2.createTrackbar('B','RGB',0,300,updateB)

cv2.setTrackbarPos('Light','RGB',100)
cv2.setTrackbarPos('Contrast','RGB',10)
cv2.setTrackbarPos('R','RGB',100)
cv2.setTrackbarPos('G','RGB',100)
cv2.setTrackbarPos('B','RGB',100)

while (True):
    cv2.imshow('Picture',img)

    if cv2.waitKey(1)==27:
        break
cv2.destroyAllWindows()