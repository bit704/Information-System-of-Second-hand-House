import numpy as np
import pandas as pd
import requests
import time
from multiprocessing.dummy import Pool
import random
import os

csv =  pd.read_csv('贝壳二手房列表-成都38470条.csv',header=None,delimiter=',',error_bad_lines=False)
#原始数据中存在一些错误行，凭空多出了几列，直接对其读取会报错，已经手动将原始数据中的错误修复

label = csv.iloc[0 ,:-1].values
data  = csv.iloc[1:,:-1].values  #去掉最后一列

headers = {
        "User-Agent": "Baiduspider"                                                                                  
}
proxies = {"HTTP": "113.108.242.36:47713"}
counter=0
os.makedirs('ershoufang_pages',exist_ok=True) #创建目录，屏蔽也不报异常
#os.makedirs('xiaoqu_pages',exist_ok=True)

def reptile(urlstring):
    global counter
    counter += 1
    print('c'+str(counter))   
    if urlstring == 'empty':
        return
    time.sleep(random.random())
    sn = urlstring.split(',')[1] #编号
    url = urlstring.split(',')[0] 
    try:
        response = requests.get(url,headers=headers,proxies=proxies)
    except requests.exceptions.RequestException:
        return
    code = response.status_code
    if code != 200:  #请求未成功
        return
    html_data = response.content.decode()
    with open(os.path.join('ershoufang_pages',sn+'.txt'),'w',encoding='utf-8') as f:
        f.write(html_data)


pool = Pool(500)        
url = data[:,2]
for i in range(20000): #给每个链接的后面加上编号
    if type(url[i]) == str:      
        url[i] = url[i]+','+str(i) 
    else:
        url[i] = 'empty'

pool.map(reptile,url) #多线程运行
