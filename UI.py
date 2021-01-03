import numpy as np
import cv2
import cvui

img_path=".\icons\example.png"
img=cv2.imread(img_path)
state=0

cv2.namedWindow('Picture')
cvui.init('Picture')

#定义各个界面的操作
def state0():
    if(cvui.button(img,40,100,'button1')):
        Button1()

def state1():
    if(cvui.button(img,40,100,'button2')):
        Button2()

#更新界面函数 通过state的不同来选择不同的界面函数
def UpdateState():
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

while (True):
    cvui.printf(img,0,0,0.4,0xff0000,str(state))
    cvui.imshow('Picture',img)
    UpdateState()
    cvui.update('Picture')
    cv2.imshow('Picture',img)

    if cv2.waitKey(1)==27:
        break
cv2.destroyAllWindows()