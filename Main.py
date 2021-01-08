import base64
import os
import time

import cv2
import cvui
import numpy as np
import requests


faceCascade=cv2.CascadeClassifier('.\\haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(1)
cap.set(3,1920)
cap.set(4,1080)
cv2.namedWindow('Camera',0)
cv2.resizeWindow('Camera',480,270)
cvui.init('Camera')
fourcc=cv2.VideoWriter_fourcc(*'XVID')  #视频编码器

ret,image=cap.read()
image_ui=image
(B,G,R)=cv2.split(image)  #将图像分为RGB
state=0 #状态
CheckState=[False,False,False,False]    #保存状态
burstnum=0  #连拍张数
r=[0]
g=[0]
b=[0]
light=0 #闪光灯
face=0  #人脸识别

result1=[]
photocount=0
explorephoto=0

result2=[]
burstcount=0
exploreburst=0

result3=[]
videocount=0
explorevideo=0

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
        if os.path.exists(photo_path+str(result1[num])[2:-2]+'.png'):
            os.remove(photo_path+str(result1[num])[2:-2]+'.png')
            files=open(photo_path+'photolist.txt','r+')
            line=files.readlines()
            line[num]=''
            if(num==photocount):
                line[num-1]=line[num-1][0:-1]
            files.close()
            files=open(photo_path+'photolist.txt','w+')
            line=files.writelines(line)
            files.close()

def refreshphotolist():
    global result1,photocount,explorephoto
    result1=[]
    photocount=0
    with open(photo_path+'photolist.txt','r') as f:
        for line in f:
            result1.append(list(line.strip('\n').split(',')))
            photocount+=1
    photocount-=1
    explorephoto=photocount

#连拍相关操作
burst_path=".\\burst\\"   #连拍照片存储位置
def burst(burst_name):   #根据照片名 返回对应对象
    return cv2.imread(burst_path+str(burst_name)+'.png')

def saveburst(img):    #存储函数 根据时间戳生成文件名
    global burstnum
    number=time.strftime("%Y%m%d%H%M%S")+str(burstnum)
    with open(burst_path+'burstlist.txt',"a") as f: #设置文件对象
        f.writelines('\n'+number)    #向文件目录逐行写入序号
    refreshburstlist()
    cv2.imwrite(burst_path+number+'.png',img)
    burstnum+=1

def deleteburst(num):
    if(num!=0):
        if os.path.exists(burst_path+str(result2[num])[2:-2]+'.png'):
            os.remove(burst_path+str(result2[num])[2:-2]+'.png')
            files=open(burst_path+'burstlist.txt','r+')
            line=files.readlines()
            line[num]=''
            if(num==burstcount):
                line[num-1]=line[num-1][0:-1]
            files.close()
            files=open(burst_path+'burstlist.txt','w+')
            line=files.writelines(line)
            files.close()

def refreshburstlist():
    global result2,burstcount,exploreburst
    result2=[]
    burstcount=0
    with open(burst_path+'burstlist.txt','r') as f:
        for line in f:
            result2.append(list(line.strip('\n').split(',')))
            burstcount+=1
    burstcount-=1
    exploreburst=burstcount

#视频相关操作
video_path=".\\videos\\"  #视频存储位置
def video(video_name):
    global CheckState,cap
    if(not CheckState[3]):
        CheckState[3]=True
        cap=cv2.VideoCapture(video_path+str(video_name)+'.avi')

videoout=cv2.VideoWriter(video_path+'VEDIOLIST.avi',fourcc,24,(1920,1080))

def savevideo():
    global videoout
    number=time.strftime("%Y%m%d%H%M%S")
    with open(video_path+'videolist.txt',"a") as f: #设置文件对象
        f.write('\n'+number)    #向文件目录逐行写入序号
    refreshvideolist()
    videoout=cv2.VideoWriter(video_path+number+'.avi',fourcc,24,(1920,1080))

def deletevideo(num):
    global cap
    if(num!=0):
        if os.path.exists(video_path+str(result3[num])[2:-2]+'.avi'):
            cap=cv2.VideoCapture(video_path+str(result3[num-1])[2:-2]+'.avi')
            os.remove(video_path+str(result3[num])[2:-2]+'.avi')
            files=open(video_path+'videolist.txt','r+')
            line=files.readlines()
            line[num]=''
            if(num==videocount):
                line[num-1]=line[num-1][0:-1]
            files.close()
            files=open(video_path+'videolist.txt','w+')
            line=files.writelines(line)
            files.close()

def refreshvideolist():
    global result3,videocount,explorevideo
    result3=[]
    videocount=0
    with open(video_path+'videolist.txt','r') as f:
        for line in f:
            result3.append(list(line.strip('\n').split(',')))
            videocount+=1
    videocount-=1
    explorevideo=videocount


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
    if(state==7 or state==12):   #若在RGB模式中
        (B,G,R)=cv2.split(image)  #将图像分为RGB
        image=cv2.merge([np.uint8(np.clip((B*(b[0]/50+1)),0,255)),np.uint8(np.clip((G*(g[0]/50+1)),0,255)),np.uint8(np.clip((R*(r[0]/50+1)),0,255))])   #合成RGB调整后的图像
    if(state!=8 or state!=9 or state!=11 or state!=12):   #若不在浏览模式
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
    cvui.update('Camera')

#定义各个界面的操作
def state0():   #初始界面
    icon('photo',104,476,1)
    icon('burst',632,476,2)
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
    if(icon('burst',896,832)):
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
    global CheckState,light
    if(CheckState[2]==False):
        if(icon('start',896,832)):
            savevideo()
            CheckState[2]=True
    else:
        if(icon('stop',896,832)):
            CheckState[2]=False
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
        icon('explore_photo',280,476,8)
    if(burstcount!=0):
        icon('explore_burst',896,476,9)
    if(videocount!=0):
        icon('explore_video',1526,476,10)
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
    icon('rgb',1526,476,7)
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
    print('explore:'+str(explorephoto)+' count:'+str(photocount))
    image_ui=photo(str(result1[explorephoto])[2:-2])
    while(image_ui is None):
        explorephoto-=1
        image_ui=photo(str(result1[explorephoto])[2:-2])
    icon('exit',16,16,4)
    if(icon('left',16,476)):
        explorephoto-=1
        if(explorephoto<0):
            explorephoto=0
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
    global image_ui,exploreburst
    print('explore:'+str(exploreburst)+' count:'+str(burstcount))
    image_ui=burst(str(result2[exploreburst])[2:-2])
    while(image_ui is None):
        exploreburst-=1
        image_ui=burst(str(result2[exploreburst])[2:-2])
    icon('exit',16,16,4)
    if(icon('left',16,476)):
        exploreburst-=1
        if(exploreburst<0):
            exploreburst=0
    if(icon('right',1776,476)):
        exploreburst+=1
        if(exploreburst>burstcount):
            exploreburst=burstcount
    icon('rgb',16,936,12)
    if(icon('delete',1776,936)):
        deleteburst(exploreburst)
        refreshburstlist()
    icon('home',1776,16,0)

def state10():  #文件浏览 视频
    global CheckState,explorevideo
    print('explore:'+str(explorevideo)+' count:'+str(videocount))
    video(str(result3[explorevideo])[2:-2])
    icon('exit',16,16,4)
    if(icon('left',16,476)):
        CheckState[3]=False
        explorevideo-=1
        if(explorevideo<0):
            explorevideo=0
    if(icon('right',1776,476)):
        CheckState[3]=False
        explorevideo+=1
        if(explorevideo>videocount):
            explorevideo=videocount
    if(icon('delete',1776,936)):
        CheckState[3]=False
        deletevideo(explorevideo)
        refreshvideolist()
    if(icon('home',1776,16,0)):
        CheckState[3]=False
        cap=cv2.VideoCapture(1)

def state11():  #百度AI 风格选择
    global image_ui
    API_style_path=photo_path+str(result1[explorephoto])[2:-2]+'.png'
    image_ui=photo(str(result1[explorephoto])[2:-2])
    icon('exit',16,16,8)
    if(icon('cloud_cartoon',592,196)):
        API_style(API_style_path,'cartoon')
    if(icon('cloud_pencil',880,196)):
        API_style(API_style_path,'pencil')
    if(icon('cloud_color_pencil',1160,196)):
        API_style(API_style_path,'color_pencil')
    if(icon('cloud_warm',592,472)):
        API_style(API_style_path,'warm')
    if(icon('cloud_wave',880,472)):
        API_style(API_style_path,'wave')
    if(icon('cloud_lavender',1160,472)):
        API_style(API_style_path,'lavender')
    if(icon('cloud_mononoke',592,760)):
        API_style(API_style_path,'mononoke')
    if(icon('cloud_scream',880,760)):
        API_style(API_style_path,'scream')
    if(icon('cloud_gothic',1160,760)):
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
    global CheckState,burstnum
    if(icon('photo',896,832)):
        CheckState[1]=True
        burstnum=9
    icon('exit',16,16,9)
    cvui.window(image_ui,1440,200,440,900,'RGB')
    cvui.trackbar(image_ui,1480,400,400,r,-100,100)
    cvui.trackbar(image_ui,1480,600,400,g,-100,100)
    cvui.trackbar(image_ui,1480,800,400,b,-100,100)
    icon('home',1776,16,0)

if __name__=='__main__':
    refreshphotolist()
    refreshburstlist()
    refreshvideolist()
    while (True):
        ret,image=cap.read()
        if(not ret):
            CheckState[3]=False
            image=cv2.imread(icon_path+'black.png')
        if(CheckState[2]==True):
            videoout.write(image)
        UI()
        try:
            cv2.imshow('Camera',image_ui)
        except:
            cv2.imshow('Camera',image)
        if cv2.waitKey(30) & 0xff==27 or state==-1:
            break

    cap.release()
    videoout.release()
    cv2.destroyAllWindows()