import base64
import os
import time

import cv2
import cvui
import numpy as np
import requests

#照片相关操作
photo_path=".\\photos\\"   #照片存储位置
def photo(photo_name):   #根据照片名 返回对应对象
    return cv2.imread(photo_path+photo_name+'.png')

burst_path=".\\burst\\"   #连拍照片存储位置
def photo(photo_name):   #根据照片名 返回对应对象
    return cv2.imread(photo_path+photo_name+'.png')

def savephoto(img):    #存储函数 根据时间戳生成文件名
    cv2.imwrite(photo_path+time.strftime("%Y%m%d%H%M%S")+'.png',img)

def saveburst(img,ms):    #存储函数 根据时间戳生成文件名
    cv2.imwrite(photo_path+time.strftime("%Y%m%d%H%M%S")+str(ms)+'.png',img)

#视频相关操作
video_path=".\\videos\\"  #视频存储位置
def video(video_name):
    return cv2.imread(video_path+video_name+'.mp4')

#图标相关操作
icon_path=".\\icons\\"     #图标存储位置
def icon(icon_name,icon_x,icon_y,tostate=-2):  #在指定位置创建相应图标 当图标被单击时返回1
    global image_ui,state
    icon=cv2.imread(icon_path+icon_name+'.png')
    cvui.image(image_ui,icon_x,icon_y,icon)
    #size=image.shape
    #if(cvui.mouse(cvui.CLICK) and icon_x<=cvui.mouse().x<=icon_x+size[1] and icon_y<=cvui.mouse().y<=icon_y+size[0]):
    if(cvui.mouse(cvui.CLICK) and icon_x<=cvui.mouse().x<=icon_x+128 and icon_y<=cvui.mouse().y<=icon_y+128):
        print('icon clicked at '+str(cvui.mouse().x)+','+str(cvui.mouse().y))
        if(tostate!=-2):
            state=tostate
        return True
    else:
        return False

'''
cartoon：卡通画风格
pencil：铅笔风格
color_pencil：彩色铅笔画风格
warm：彩色糖块油画风格
wave：神奈川冲浪里油画风格
lavender：薰衣草油画风格
mononoke：奇异油画风格
scream：呐喊油画风格
gothic：哥特油画风格
'''

def API_style(path,style):
    request_url="https://aip.baidubce.com/rest/2.0/image-process/v1/style_trans"
    f=open(path,'rb')   #二进制方式打开图片文件
    img=base64.b64encode(f.read())

    params={"image":img,"option":style}
    access_token='24.7c638e4ac68acc586591a29370217d63.2592000.1612169848.282335-23477762'
    request_url=request_url+"?access_token="+access_token
    headers={'content-type':'application/x-www-form-urlencoded'}
    response=requests.post(request_url, data=params, headers=headers)
    if response:
        #print (response.json())
        imgdata=base64.b64decode(response.json()['image'])
        file=open(photo_path+time.strftime("%Y%m%d%H%M%S")+'.png','wb')
        file.write(imgdata)
        file.close()


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
light=0
face=0

def UI():   #更新界面进程 通过state的不同来选择不同的界面函数
    global image,image_ui,state
    if(state==6):
        (B,G,R)=cv2.split(image)  #将图像分为RGB
        image=cv2.merge([np.uint8(np.clip((B*(b[0]/50+1)),0,255)),np.uint8(np.clip((G*(g[0]/50+1)),0,255)),np.uint8(np.clip((R*(r[0]/50+1)),0,255))])
    image_ui=image
    if(CheckState[0]):
        savephoto(image)
        CheckState[0]=False
    if(state==0):
        state0()
    elif(state==1):
        state1()
    elif(state==2):
        state2()
    elif(state==3):
        state3()
    elif(state==4):
        state4()
    elif(state==5):
        #state5()
        pass
    elif(state==6):
        state6()
        pass
    cvui.update('Camera')


#定义各个界面的操作
'''
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
'''
'''
def state0():
    global state
    if(icon('photo',384,476)):
        state=1
    if(icon('video',896,476)):
        state=2
    if(icon('explore',1408,476)):
        state=3
    if(icon('shutdown',1776,16)):
        state=-1
'''

def state0():
    icon('photo',384,476,1)
    icon('video',896,476,2)
    icon('explore',1408,476,3)
    icon('shutdown',1776,16,-1)

def state1():
    if(icon('photo',896,936)):
        CheckState[0]=True
    icon('settings',16,16,4)
    icon('eye',16,936,5)
    icon('home',1776,16,0)

def state2():
    pass

def state3():
    pass

def state4():
    global light,face
    icon('exit',16,16,1)
    if(icon('light',384,476)):
        if(light==0):
            light=1
            print('Flash light mode enable')
        else:
            light=0
            print('Flash light mode disable')
    if(icon('face',896,476)):
        if(face==0):
            face=1
            print('Face mode enable')
        else:
            face=0
            print('Face mode disable')
    icon('menu',1408,476,6)
    icon('home',1776,16,0)

def state5():
    pass

def state6():
    pass
    #API_style('.\\photos\\20210106200808.png','cartoon')

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
        if cv2.waitKey(30) & 0xff==27 or state==-1:
            break

    cap.release()
    cv2.destroyAllWindows()