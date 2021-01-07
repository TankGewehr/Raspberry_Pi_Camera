import numpy as np
import cv2
import cvui

img_path=".\\icons\\example.png"
img=cv2.imread(img_path)
img2=img
state=0

(B,G,R)=cv2.split(img)  #将图像分为RGB
Light=0.3   #亮度初值
Contrast=80 #对比度初值
CheckState=[False]
r=[0]
g=[0]
b=[0]

icon_path=".\\icons\\ban.png"
icon=cv2.imread(icon_path)

cv2.namedWindow('Picture')
cvui.init('Picture')

#定义各个界面的操作
def state0():
    if(cvui.button(img2,10,10,'RGB')):
        Button1()

def state1():
    cvui.image(img2,10,100,icon)
    if(cvui.button(img2,10,10,'Back')):
        Button2()
    cvui.window(img2,360,50,110,230,'RGB')
    cvui.checkbox(img,370,80,'Save',CheckState)
    cvui.trackbar(img2,370,120,100,r,-100,100)
    cvui.trackbar(img2,370,160,100,g,-100,100)
    cvui.trackbar(img2,370,200,100,b,-100,100)
    if(cvui.mouse(cvui.CLICK) and 10<=cvui.mouse().x<=42 and 280<=cvui.mouse().y<=308):
        print('icon clicked at '+str(cvui.mouse().x)+','+str(cvui.mouse().y))
        CheckState[0]=True
    

#更新界面函数 通过state的不同来选择不同的界面函数
def UpdateState():
    global img,img2,CheckState
    img=cv2.merge([np.uint8(np.clip((B*(b[0]/50+1)),0,255)),np.uint8(np.clip((G*(g[0]/50+1)),0,255)),np.uint8(np.clip((R*(r[0]/50+1)),0,255))])
    img2=img
    if(CheckState[0]):
        SavePicture()
        CheckState[0]=False
    if(state==0):
        state0()
    elif(state==1):
        state1()

#按钮 一般用来修改state的值
def Button1():
    global state
    state=1

def Button2():
    global state
    state=0

#自定义函数 用于实现不同的功能
def SavePicture():
    cv2.imwrite('.\\icons\\saved.png',img)

while (True):
    cvui.printf(img2,0,0,0.4,0xff0000,str(state))
    UpdateState()
    cvui.update('Picture')
    cv2.imshow('Picture',img2)

    if cv2.waitKey(30)==27:
        break
cv2.destroyAllWindows()