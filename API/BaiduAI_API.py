import requests
import base64

'''
图像风格转换
'''

request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/style_trans"
# 二进制方式打开图片文件
f = open('.\icons\example.png', 'rb')
img = base64.b64encode(f.read())

params = {"image":img,"option":"pencil"}
access_token = '24.7c638e4ac68acc586591a29370217d63.2592000.1612169848.282335-23477762'
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    #print (response.json())
    imgdata = base64.b64decode(response.json()['image'])
    file=open('output.png','wb')
    file.write(imgdata)
    file.close()