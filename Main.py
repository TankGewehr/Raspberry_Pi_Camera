import base64
import os
import time

import cv2
import cvui
import numpy as np
import requests


faceCascade=cv2.CascadeClassifier('.\haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(1)
cap.set(3,1920)
cap.set(4,1080)
cv2.namedWindow('Camera',0)
cv2.resizeWindow('Camera',480,270)
cvui.init('Camera')

ret,image=cap.read()
image_ui=image
(B,G,R)=cv2.split(image)  #将图像分为RGB
state=0 #状态
CheckState=[False,False]    #保存状态
burstnum=0  #连拍张数
r=[0]
g=[0]
b=[0]
light=0 #闪光灯
face=0  #人脸识别
result=[]
photocount=0
explorephoto=0

#照片相关操作
photo_path=".\\photos\\"   #照片存储位置
def photo(photo_name):   #根据照片名 返回对应对象
    return cv2.imread(photo_path+str(photo_name)+'.png')

def savephoto(img):    #存储函数 根据时间戳生成文件名
    number=time.strftime("%Y%m%d%H%M%S")
    with open(photo_path+'photolist.txt',"a") as f: #设置文件对象
        f.write('\n'+number)    #向文件目录逐行写入序号
    refreshphotolist()
    cv2.imwrite(photo_path+number+'.png',img)

def deletephoto(num):
    if(num!=0):
        if os.path.exists(photo_path+str(result[num-1])[2:-2]+'.png'):
            os.remove(photo_path+str(result[num-1])[2:-2]+'.png')
            with open(photo_path+'photolist.txt','r') as old_file:
                with open(photo_path+'photolist.txt','r+') as new_file:
                    current_line=0    #定位到需要删除的行
                    while current_line<(num-1):
                        old_file.readline()
                        current_line+=1   #当前光标在被删除行的行首，记录该位置
                    seek_point=old_file.tell()    #设置光标位置
                    new_file.seek(seek_point,0)    #读需要删除的行，光标移到下一行行首
                    old_file.readline() #被删除行的下一行读给 next_line
                    next_line=old_file.readline() #连续覆盖剩余行，后面所有行上移一行
                    while next_line:
                        new_file.write(next_line)
                        next_line=old_file.readline()
                    new_file.truncate() #写完最后一行后截断文件，因为删除操作，文件整体少了一行，原文件最后一行需要去掉

def refreshphotolist():
    global result,photocount,explorephoto
    result=[]
    photocount=0
    with open(photo_path+'photolist.txt','r') as f:
        for line in f:
            result.append(list(line.strip('\n').split(',')))
            photocount+=1
    photocount-=1
    explorephoto=photocount

burst_path=".\\burst\\"   #连拍照片存储位置
def burst(photo_name):   #根据照片名 返回对应对象
    return cv2.imread(photo_path+str(photo_name)+'.png')

def saveburst(img):    #存储函数 根据时间戳生成文件名
    global burstnum
    number=time.strftime("%Y%m%d%H%M%S")
    with open(burst_path+'burstlist.txt',"a") as f: #设置文件对象
        f.writelines(number)    #向文件目录逐行写入序号
    cv2.imwrite(photo_path+number+str(burstnum)+'.png',img)
    burstnum+=1

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

#调用百度AI API对图像风格进行调整
def API_style(path,style):  #API_style('.\\photos\\20210106200808.png','cartoon')
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
        number=time.strftime("%Y%m%d%H%M%S")
        with open(photo_path+'photolist.txt',"a") as f: #设置文件对象
            f.write('\n'+number)    #向文件目录逐行写入序号
        refreshphotolist()
        file=open(photo_path+number+'.png','wb')
        file.write(imgdata)
        file.close()
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

def UI():   #更新界面进程 通过state的不同来选择不同的界面函数
    global image,image_ui,state,burstnum
    if(state==6):   #若在eye模式中
        (B,G,R)=cv2.split(image)  #将图像分为RGB
        image=cv2.merge([np.uint8(np.clip((B*(b[0]/50+1)),0,255)),np.uint8(np.clip((G*(g[0]/50+1)),0,255)),np.uint8(np.clip((R*(r[0]/50+1)),0,255))])   #合成RGB调整后的图像
        if(face==1):    #人脸识别
            gray=cv2.cvtColor(image_ui,cv2.COLOR_BGR2GRAY)  #转化为灰度图像
            faces=faceCascade.detectMultiScale(gray,scaleFactor=1.2,minNeighbors=5,minSize=(10,10)) #识别参数
            for (x,y,w,h) in faces: #框选出人脸
                cv2.rectangle(image_ui,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray=gray[y:y+h,x:x+w]
                roi_color=image_ui[y:y+h,x:x+w]
    if(state==7):   #若在RGB模式中
        (B,G,R)=cv2.split(image)  #将图像分为RGB
        image=cv2.merge([np.uint8(np.clip((B*(b[0]/50+1)),0,255)),np.uint8(np.clip((G*(g[0]/50+1)),0,255)),np.uint8(np.clip((R*(r[0]/50+1)),0,255))])   #合成RGB调整后的图像
    if(state!=4 or state!=8 or state!=11):   #若不在浏览模式
        image_ui=image
    if(CheckState[0]):  #保存照片
        savephoto(image)
        CheckState[0]=False
    if(CheckState[1]):  #保存连拍照片
        saveburst(image)
        time.sleep(0.1) #理论连拍间隔
        if(burstnum==10):
            burstnum=0
            CheckState[1]=False
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
        state5()
    elif(state==6):
        state6()
    elif(state==7):
        state7()
    elif(state==8):
        state8()
    elif(state==9):
        state9()
    elif(state==10):
        state10()
    elif(state==11):
        state11()
    elif(state==12):
        state12()
    elif(state==13):
        state13()
    cvui.update('Camera')

#定义各个界面的操作
'''
def state0():   #cvui按钮
    global image_ui
    if(cvui.button(image_ui,10,10,'RGB')):
        Button1()

def state1():   #RGB
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

def state3():   #文件浏览
    global image_ui,exploretime
    image_ui=cv2.imread(photo_path+str(exploretime)+'.png')
    while(image_ui is None):
        exploretime-=1
        image_ui=cv2.imread(photo_path+str(exploretime)+'.png')
    icon('home',1776,16,0)
    if(icon('delete',1776,936)):
        if os.path.exists(photo_path+str(exploretime)+'.png'):
            os.remove(photo_path+str(exploretime)+'.png')
'''
def state0():   #初始界面
    icon('photo',104,476,1)
    icon('o',632,476,2)
    icon('video',1160,476,3)
    icon('explore',1688,476,4)
    icon('shutdown',1776,16,-1)

def state1():   #拍照模式 主界面
    global CheckState
    if(icon('photo',896,832)):
        CheckState[0]=True
    icon('settings',16,16,5)
    icon('eye',16,832,6)
    icon('home',1776,16,0)

def state2():   #连拍模式 主界面
    global CheckState,light
    if(icon('o',896,832)):
        CheckState[1]=True
    if(icon('light',16,16)):
        if(light==0):
            light=1
            print('Flash light mode enable')
        else:
            light=0
            print('Flash light mode disable')
    icon('home',1776,16,0)

def state3():   #视频模式 主界面
    global light
    icon('video',896,832)
    if(icon('light',16,16)):
        if(light==0):
            light=1
            print('Flash light mode enable')
        else:
            light=0
            print('Flash light mode disable')
    icon('home',1776,16,0)

def state4():   #文件浏览 主界面
    if(photocount!=0):
        icon('photo',280,476,8)
    icon('o',896,476,9)
    icon('video',1526,476,10)
    icon('home',1776,16,0)

def state5():   #拍照模式 设置
    global light,face
    icon('exit',16,16,1)
    if(icon('light',280,476)):
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
    icon('menu',1526,476,7)
    icon('home',1776,16,0)

def state6():   #eye模式
    global CheckState
    if(icon('photo',896,832)):
        CheckState[0]=True
    icon('eye_close',16,832,1)
    icon('home',1776,16,0)

def state7():   #拍照模式 设置 RGB
    global CheckState
    if(icon('photo',896,832)):
        CheckState[0]=True
    icon('exit',16,16,5)
    cvui.window(image_ui,1440,200,440,900,'RGB')
    cvui.trackbar(image_ui,1480,400,400,r,-100,100)
    cvui.trackbar(image_ui,1480,600,400,g,-100,100)
    cvui.trackbar(image_ui,1480,800,400,b,-100,100)
    icon('home',1776,16,0)

def state8():   #文件浏览 照片
    global image_ui,explorephoto
    #print(str(result[count-1])[2:-2])
    print('explore:'+str(explorephoto))
    image_ui=photo(str(result[explorephoto])[2:-2])
    icon('exit',16,16,4)
    #if(icon('refresh',896,16)):
        #refreshphotolist()
    if(icon('left',16,476)):
        explorephoto-=1
        if(explorephoto<1):
            explorephoto=1
    if(icon('right',1776,476)):
        explorephoto+=1
        if(explorephoto>photocount):
            explorephoto=photocount
    icon('cloud_up',16,936,11)
    if(icon('delete',1776,936)):
        deletephoto(explorephoto)
        refreshphotolist()
    icon('home',1776,16,0)

def state9():   #文件浏览 连拍
    icon('exit',16,16,4)

    icon('menu',16,476,12)

    icon('home',1776,16,0)

def state10():  #文件浏览 视频
    icon('exit',16,16,4)

    icon('menu',16,476,13)

    icon('home',1776,16,0)

def state11():  #百度AI 风格选择
    global image_ui
    API_style_path=photo_path+str(result[explorephoto])[2:-2]+'.png'
    image_ui=photo(str(result[explorephoto])[2:-2])
    icon('exit',16,16,8)
    if(icon('cloud_down',592,196)):
        API_style(API_style_path,'cartoon')
    if(icon('cloud_down',880,196)):
        API_style(API_style_path,'pencil')
    if(icon('cloud_down',1160,196)):
        API_style(API_style_path,'color_pencil')
    if(icon('cloud_down',592,472)):
        API_style(API_style_path,'warm')
    if(icon('cloud_down',880,472)):
        API_style(API_style_path,'wave')
    if(icon('cloud_down',1160,472)):
        API_style(API_style_path,'lavender')
    if(icon('cloud_down',592,760)):
        API_style(API_style_path,'mononoke')
    if(icon('cloud_down',880,760)):
        API_style(API_style_path,'scream')
    if(icon('cloud_down',1160,760)):
        API_style(API_style_path,'gothic')
    icon('home',1776,16,0)
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

def state12():  #文件浏览 连拍 RGB
    icon('exit',16,16,9)
    icon('home',1776,16,0)

def state13():  #文件浏览 视频 RGB
    icon('exit',16,16,10)
    icon('home',1776,16,0)

'''
#按钮 一般用来修改state的值
def Button1():
    global state
    state=1

def Button2():
    global state
    state=0
'''

if __name__=='__main__':
    refreshphotolist()
    while (True):
        ret,image=cap.read()
        UI()
        try:
            cv2.imshow('Camera',image_ui)
        except:
            cv2.imshow('Camera',image)
        if cv2.waitKey(30) & 0xff==27 or state==-1:
            break

    cap.release()
    cv2.destroyAllWindows()