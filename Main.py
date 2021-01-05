import numpy as np
import cv2
import cvui
import requests
import base64
import os
import time


#照片相关操作
photo_path=".\photos\\"   #照片存储位置
def photo(photo_name):   #根据照片名 返回对应对象
    return cv2.imread(photo_path+photo_name+'.png')

def savephoto(img):    #存储函数 根据时间戳生成文件名
    cv2.imwrite(photo_path+time.strftime("%Y%m%d%H%M%S")+'.png',img)

#视频相关操作
video_path=".\\videos\\"  #视频存储位置
def video(video_name):
    return cv2.imread(video_path+video_name+'.mp4')

#图标相关操作
icon_path=".\icons\\"     #图标存储位置
def icon(icon_name,icon_x,icon_y):  #在指定位置创建相应图标 当图标被单击时返回1
    icon=cv2.imread(icon_path+icon_name+'.png')
    cvui.image(image_ui,icon_x,icon_y,icon)
    size=image.shape
    if(cvui.mouse(cvui.CLICK) and icon_x<=cvui.mouse().x<=icon_x+size[1] and icon_y<=cvui.mouse().y<=icon_y+size[0]):
        return True
    else:
        return False


cap=cv2.VideoCapture(1)
cap.set(3,1920)
cap.set(4,1080)
cv2.namedWindow('Camera',0)
cv2.resizeWindow('Camera',480,270)
cvui.init('Camera')

ret,image=cap.read()
image_ui=image
(B,G,R)=cv2.split(image)  #将图像分为RGB
state=0
CheckState=[False]
r=[0]
g=[0]
b=[0]

def UI():   #更新界面进程 通过state的不同来选择不同的界面函数
    global image,image_ui,state
    (B,G,R)=cv2.split(image)  #将图像分为RGB
    image=cv2.merge([np.uint8(np.clip((B*(b[0]/50+1)),0,255)),np.uint8(np.clip((G*(g[0]/50+1)),0,255)),np.uint8(np.clip((R*(r[0]/50+1)),0,255))])
    image_ui=image
    if(state==0):
        state0()
    elif(state==1):
        state1()
    cvui.update('Camera')


#定义各个界面的操作
def state0():
    global image_ui
    if(cvui.button(image_ui,10,10,'RGB')):
        Button1()

def state1():
    global image
    if(cvui.button(image_ui,10,10,'Back')):
        Button2()
    cvui.window(image_ui,360,50,110,230,'RGB')
    cvui.checkbox(image_ui,370,80,'Save',CheckState)
    cvui.trackbar(image_ui,370,120,100,r,-100,100)
    cvui.trackbar(image_ui,370,160,100,g,-100,100)
    cvui.trackbar(image_ui,370,200,100,b,-100,100)
    if(icon('cam',1000,1000)):
        CheckState[0]=True
    if(CheckState[0]):
        savephoto(image)
        CheckState[0]=False


#按钮 一般用来修改state的值
def Button1():
    global state
    state=1

def Button2():
    global state
    state=0

if __name__=='__main__':
    while (True):
        ret,image=cap.read()
        UI()
        cv2.imshow('Camera',image_ui)
        if cv2.waitKey(30) & 0xff==27:
            break

    cap.release()
    cv2.destroyAllWindows()