from urllib.parse import quote

from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
import pandas as pd
from sklearn import tree
import os
import datetime
from urllib.request import urlopen
import json


def getCoordinate(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = '4zOe4FEzuYr4M6VagaegLzRvxeZKRe9M'  # 浏览器端密钥
    address = quote(address)  # 由于地址变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)

    lat = temp['result']['location']['lat']
    lng = temp['result']['location']['lng']
    return lat, lng


def CART(parameters):
    csv = pd.read_csv('static/data/processedDataForCalculate.csv',
                      header=None, delimiter=',')
    x = csv.iloc[:, 0:-1].values
    # '区','所处楼层级别','总楼层数','建造年份','面积','朝向','是否近地铁','挂牌年','挂牌月','挂牌日','纬度','经度'
    y = csv.iloc[:, -1].values
    # '总价'
    cart = tree.DecisionTreeRegressor(random_state=20, max_depth=10)
    cart.fit(x, y)
    parameters = np.array(parameters).reshape(1, -1)
    return cart.predict(parameters)


def dataFilter(condition):
    csv = pd.read_csv('static/data/processedDataForVisual.csv',
                      header=None, delimiter=',')
    data = csv.iloc[1:, :].values
    result = []
    for i in range(19998):
        if condition[0] != -1 and int(data[i][2]) != condition[0]:  # 区
            continue
        if condition[1] != -1 and data[i][3] != condition[1]:  # 房型
            continue
        if condition[2] != -1 and int(data[i][4]) != condition[2]:  # 所处楼层级别
            continue
        if condition[3] != -1 and int(data[i][5]) < condition[3]:  # 总楼层数下限
            continue
        if condition[4] != -1 and int(data[i][5]) > condition[4]:  # 总楼层数上限
            continue
        if condition[5] != -1 and int(data[i][6]) < condition[5]:  # 建造年份下限
            continue
        if condition[6] != -1 and int(data[i][6]) > condition[6]:  # 建造年份上限
            continue
        if condition[7] != -1 and float(data[i][7]) < condition[7]:  # 面积下限
            continue
        if condition[8] != -1 and float(data[i][7]) > condition[8]:  # 面积上限
            continue
        if condition[9] != -1 and int(data[i][8]) != condition[9]:  # 朝向
            continue
        if condition[10] != -1 and int(data[i][11]) != condition[10]:  # 是否近地铁
            continue
        if condition[11] != -1 and float(data[i][12]) < condition[11]:  # 面积下限
            continue
        if condition[12] != -1 and float(data[i][12]) > condition[12]:  # 面积上限
            continue
        if condition[13] != -1 and float(data[i][16]) < condition[13]:  # 面积下限
            continue
        if condition[14] != -1 and float(data[i][16]) > condition[14]:  # 面积上限
            continue
        newdata = data[i]
        result.append(newdata)
    return result


def home(request):
    return render(request, "home.html")


def forecast(request):
    ctx = {'points': []}
    if request.POST:
        try:
            location = request.POST['位置']
            la, lo = getCoordinate(request.POST['位置'])
        except:
            la = 104.23726561721571  # 所有二手房的均值
            lo = 30.520141715355887
            location = "不明"
        keys = ['区', '所处楼层级别', '总楼层数', '建造年份', '面积', '朝向', '是否近地铁']
        parameters = []
        for i in range(7):
            value = request.POST[keys[i]]
            if value == "":
                parameters.append(-1)
            elif i == 4:
                parameters.append(float(value))
            else:
                parameters.append(int(value))
        parameters.extend([datetime.datetime.now().year, datetime.datetime.now().month,
                           datetime.datetime.now().day, la, lo])
        ctx['预测价格'] = CART(parameters)[0].round(decimals=2)
        ctx['points'] = json.dumps([{"lng": lo, "lat": la, "name": location}])  # 避免被转义

    return render(request, "forecast.html", ctx)


def recommend(request):
    ctx = {'points': []}
    if request.POST:
        keys = ['区', '房型', '所处楼层级别', '总楼层数下限', '总楼层数上限', '建造年份下限', '建造年份下限',
                '面积下限', '面积上限', '朝向', '是否近地铁', '单价下限', '单价上限', '总价下限', '总价上限']
        condition = []
        for i in range(15):
            value = request.POST[keys[i]]
            if value == "":
                condition.append(-1)
            elif i == 1:
                condition.append(value)
            elif i in [0, 2, 3, 4, 5, 6, 9, 10]:
                condition.append(int(value))
            else:
                condition.append(float(value))
        houselist = dataFilter(condition)
        newhouselist = []
        for house in houselist:
            house = np.delete(house, [0, 2, 9, 10, 13, 14, 15, 17, 18], axis=0)
            house[1] = str(house[1].split("|")[0]) + "室" + str(house[1].split("|")[1]) + "厅"
            house[2] = {0: "地下室", 1: "低楼层", 2: "中楼层", 3: "高楼层"}[int(house[2])]
            house[6] = {1: "北", 2: "东北", 3: "东", 4: "东南", 5: "南", 6: "西南", 7: "西", 8: "西北"}[int(house[6])]
            house[7] = {0: "不是", 1: "是"}[int(house[7])]
            for i in range(len(house)):
                if house[i] == "-1":
                    house[i] = "无"
            newhouselist.append(house)
        ctx['list'] = newhouselist
        points = []
        for i in houselist:
            points.append({"lng": float(i[18]), "lat": float(i[17]), "name": i[1]})
        ctx['points'] = json.dumps(points)
    return render(request, "recommend.html", ctx)


def visualization(request):
    ctx = {}
    return render(request, "visualization.html", ctx)


'''
py manage.py runserver 0.0.0.0:8000
'''
