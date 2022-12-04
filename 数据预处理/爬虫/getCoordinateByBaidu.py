#ak:4zOe4FEzuYr4M6VagaegLzRvxeZKRe9M
import numpy as np
import pandas as pd
import json
from urllib.request import urlopen, quote
import requests

def getCoordinate(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = '4zOe4FEzuYr4M6VagaegLzRvxeZKRe9M' # 浏览器端密钥
    address = quote(address) # 由于地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + address  + '&output=' + output + '&ak=' + ak 
    req = urlopen(uri)
    res = req.read().decode() 
    temp = json.loads(res)
    
    lat = temp['result']['location']['lat']
    lng = temp['result']['location']['lng']
    return lat, lng

csv =  pd.read_csv('location.csv',header=None,delimiter=',')

data = csv.values

latitude = []
longitude = []

for i in range(20000):
    address = data[i][0]
    print(i)
    try:
        la,lo = getCoordinate(address)
        latitude.append(la)
        longitude.append(lo)
    except:
        latitude.append(-1)
        longitude.append(-1)


latitude = np.array(latitude)
latitude = pd.DataFrame(latitude)
latitude.to_csv('latitude.csv',index=False,header=False,encoding="utf_8_sig")
longitude = np.array(longitude)
longitude= pd.DataFrame(longitude)
longitude.to_csv('longitude.csv',index=False,header=False,encoding="utf_8_sig")
