import numpy as np
import pandas as pd


csv =  pd.read_csv('数据预处理/processedDataForVisual.csv',header=None,delimiter=',')
data = csv.iloc[1:,:].values

condition = [7,'2|1',1,1,6,1900,1998,10.0,63.0,4,0,100,11587.3,10,73.0]
'''
'区','房型','所处楼层级别','总楼层数下限','总楼层数上限'，'建造年份下限','建造年份下限',
'面积下限','面积上限','朝向','是否近地铁','单价下限','单价上限','总价下限','总价上限'
-1代表缺省
'''
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
    result.append(data[i])

print(result)
        
        
    
    
