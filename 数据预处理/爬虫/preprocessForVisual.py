import numpy as np
import pandas as pd
import re

csv =  pd.read_csv('贝壳二手房列表-成都38470条.csv',header=None,delimiter=',',error_bad_lines=False)
#原始数据中存在一些错误行，凭空多出了几列，直接对其读取会报错，已经手动将原始数据中的错误修复

label = csv.iloc[0 ,:-1].values
data  = csv.iloc[1:,:-1].values  #去掉最后一列

row = len(data)
column = len(label)

district = data[:,0] #区
district_dict = {}
i=0
for item in np.unique(district):
    district_dict[item] = i
    i += 1
for i in range(row):
    district[i] = district_dict[district[i]]

houseinfo = data[:,6]

floorrank = [] #所处楼层级别
totalfloor = [] #总楼层数
year = [] #建造年份
area = [] #面积
ori = [] #朝向
housetype = [] #户型

for i in range(row):
    string = houseinfo[i]
    if type(string) == str: 
        
        floorrank_string = string[0]
        if(floorrank_string == '高'):
            floorrank.append(3)
        elif(floorrank_string == '中'):
            floorrank.append(2)
        elif(floorrank_string == '低'):
            floorrank.append(1)
        elif(floorrank_string == '地'):
            floorrank.append(0)
        else:
            floorrank.append(-1)
        
        totalfloor_string = re.search(r'(?<=共)[0-9]*(?=层)', string)
        if(totalfloor_string == None):
            totalfloor.append(-1)
        else:
            if totalfloor_string.group() == '' : #为地下室
                totalfloor.append(0)           
            else:
                totalfloor.append(int(totalfloor_string.group()))
        
        year_string = re.search(r'\d+(?=年)',string)
        if year_string == None :
            year.append(-1)
        else:
            year.append(int(year_string.group()))
        
        area_string = re.search(r'[0-9]*(\.)?[0-9]*(?=平米)',string)        
        if area_string == None :
            area.append(-1)
        else:
            area.append(float(area_string.group()))
        
        ori_string = string.split('|')[-1]
        
        ori_dict = {'北':1,'东北':2,'东':3,'东南':4,'南':5,'西南':6,'西':7,'西北':8}
        ori.append(ori_dict.get(ori_string.strip(),-1)) #如果没有，则给默认值-1
        
        housetype_obj = re.search(r'(\d+)室(\d+)厅',string)
        if housetype_obj != None:
            housetype.append(housetype_obj.group(1)+"|"+housetype_obj.group(2))
        else:
            housetype.append(-1)
    else:
        #print(i)
        floorrank.append(-1)
        totalfloor.append(-1)
        year.append(-1)
        area.append(-1)
        ori.append(-1)
        housetype.append(-1)

floorrank = np.array(floorrank)
totalfloor = np.array(totalfloor)
year = np.array(year)
area = np.array(area)
ori = np.array(ori)
housetype = np.array(housetype)
  
att = data[:,7]
for i in range(row):
    string = str(att[i])
    att_string = re.search(r'[0-9]+(?=人)',string)
    if att_string == None :
            att[i]=-1
    else:
        att[i] = int(att_string.group())

isvrfuturehome = data[:,8]
for i in range(row):
    if type(isvrfuturehome[i]) == str:
        if isvrfuturehome[i].strip() == "VR房源":
            isvrfuturehome[i] = 1
        else:
            isvrfuturehome[i] = 0
    else:
        isvrfuturehome[i]=0

subway = data[:,9]
for i in range(row):
    if type(subway[i]) == str:
        if subway[i].strip() == "近地铁":
            subway[i] = 1
        else:
            subway[i] = 0
    else:
        subway[i]=0

taxfree = data[:,10]
for i in range(row):
    if type(taxfree[i]) == str:
        if taxfree[i].strip() == "满五年":
            taxfree[i] = 1
        else:
            taxfree[i] = 0
    else:
        taxfree[i]=0

     
totalprice = data[:,11] #总价
for i in range(row):
    if type(totalprice[i]) == str:
        totalprice[i] = float(totalprice[i])
    else:
        totalprice[i] = -1

unitprice = data[:,12]  #单价
for i in range(row):
    string = unitprice[i]
    if type(string) == str:
       unitprice[i] = float(string[2:][:-4])  #去掉前2个字符和后4个字符  
    else:
        unitprice[i] = -1


hangoutdate_csv =  pd.read_csv('hangoutdate.csv',header=None,delimiter=',')
hangoutdate = hangoutdate_csv.iloc[:].values
hangoutyear = hangoutdate[0]
hangoutmonth = hangoutdate[1]
hangoutday = hangoutdate[2]

location_csv = pd.read_csv('location.csv',header=None,delimiter=',')
location = location_csv.iloc[:].values

latitude_csv = pd.read_csv('latitude.csv',header=None,delimiter=',')
latitude = latitude_csv.iloc[:].values
longitude_csv = pd.read_csv('longitude.csv',header=None,delimiter=',')
longitude = longitude_csv.iloc[:].values

ID = np.arange(20000)
newdata = np.hstack((ID.reshape(-1,1),
                     location.reshape(-1,1),
                     district.reshape(-1,1),
                     housetype.reshape(-1,1),
                     floorrank.reshape(-1,1),
                     totalfloor.reshape(-1,1),
                     year.reshape(-1,1),
                     area.reshape(-1,1),
                     ori.reshape(-1,1),
                     att.reshape(-1,1),
                     isvrfuturehome.reshape(-1,1),
                     subway.reshape(-1,1),
                     unitprice.reshape(-1,1),
                     hangoutyear.reshape(-1,1),
                     hangoutmonth.reshape(-1,1),
                     hangoutday.reshape(-1,1),
                     totalprice.reshape(-1,1),
                     latitude.reshape(-1,1),
                     longitude.reshape(-1,1)))

newdata = np.delete(newdata,[15774,13398],axis=0)

df = pd.DataFrame(newdata)

#df.columns = ['district','floorrank','totalfloor','year','area','ori','att','isvrfuturehome','subway','unitprice','totalprice']
df.columns = ['编号','位置','区','房型','所处楼层级别','总楼层数','建造年份','面积','朝向','关注数','是否有VR房源','是否近地铁','单位价格',
              '挂牌年','挂牌月','挂牌日','总价','纬度','经度']

df.to_csv('processedDataForVisual.csv',index=False,encoding="utf_8_sig",sep=',')  #不需要加列号，防止乱码


