import numpy as np
import cv2

img_path=".\\icons\\example.png"
img=cv2.imread(img_path)    #用于显示的图像
(B,G,R)=cv2.split(img)      #将图像分为RGB
Light=0.3                   #亮度初值
Contrast=80                 #对比度初值
r=1                         #红色的比例初值
g=1                         #绿色的比例初值
b=1                         #蓝色的比例初值

def updata():
    global img
    img=cv2.merge([np.uint8(np.clip((B*b),0,255)),np.uint8(np.clip((G*g),0,255)),np.uint8(np.clip((R*r),0,255))])
    img=np.uint8(np.clip((Light*img+Contrast),0,255))

def updateR(x):
    global r
    r=cv2.getTrackbarPos('R','RGB')
    r*=0.01

def updateG(x):
    global g
    g=cv2.getTrackbarPos('G','RGB')
    g*=0.01

def updateB(x):
    global b
    b=cv2.getTrackbarPos('B','RGB')
    b*=0.01

def updateLight(x):
    global Light
    Light=cv2.getTrackbarPos('Light','RGB')
    Light*=0.01

def updateContrast(x):
    global Contrast
    Contrast=cv2.getTrackbarPos('Contrast','RGB')

def SavePicture(x):
    cv2.imwrite('.\\icons\\saved.png',img)
    cv2.setTrackbarPos('Save','RGB',0)


cv2.namedWindow('RGB')
cv2.createTrackbar('Light','RGB',0,300,updateLight)
cv2.createTrackbar('Contrast','RGB',0,255,updateContrast)
cv2.createTrackbar('R','RGB',0,300,updateR)
cv2.createTrackbar('G','RGB',0,300,updateG)
cv2.createTrackbar('B','RGB',0,300,updateB)
cv2.createTrackbar('Save','RGB',0,1,SavePicture)

cv2.setTrackbarPos('Light','RGB',100)
cv2.setTrackbarPos('Contrast','RGB',10)
cv2.setTrackbarPos('R','RGB',100)
cv2.setTrackbarPos('G','RGB',100)
cv2.setTrackbarPos('B','RGB',100)


while (True):
    updata()
    cv2.imshow('Picture',img)

    if cv2.waitKey(1)==27:
        break
cv2.destroyAllWindows()