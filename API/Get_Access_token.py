# encoding:utf-8
import requests 

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=MLtBNWHSlDGfuuyKobKHsBuX&client_secret=qxYbZSuMLCqK5tZtv8dZd3HSU9GcGqi0'
response = requests.get(host)
if response:
    print(response.json())