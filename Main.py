import numpy as np
import cv2
import cvui
import requests
import base64
import os

photo_path=".\photos\\"   #照片存储位置
def photo(x):
    return cv2.imread(photo_path+x+'.png')


video_path=".\\videos\\"  #视频存储位置
def video(x):
    return cv2.imread(video_path+x+'.png')


icon_path=".\icons\\"     #图标位置
def icon(x):
    return cv2.imread(icon_path+x+'.png')


cap=cv2.VideoCapture(1)
cap.set(3,1920)
cap.set(4,1080)
ret,img=cap.read()
cv2.namedWindow('Camera',0)
cv2.resizeWindow('Camera',480,270)
cvui.init('Camera')



while (True):
    ret,img=cap.read()
    img2=img

    print('cursor at '+str(cvui.mouse().x)+','+str(cvui.mouse().y))
    #UpdateState()
    cvui.update('Camera')
    cv2.imshow('Camera',img2)

    if cv2.waitKey(30) & 0xff==27:
        break

cap.release()
cv2.destroyAllWindows()