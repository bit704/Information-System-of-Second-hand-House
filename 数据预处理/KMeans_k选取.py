import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from matplotlib import pyplot as plt

csv =  pd.read_csv('数据预处理/processedDataForCalculate.csv',header=None,delimiter=',')

data = csv.values

k_range = range(2,15)
sc = [] #轮廓系数 silhouette coefficient
sse = [] #误差平方和 sum of the squared errors

for k in k_range:
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(data)
    sse.append(kmeans.inertia_) #误差平方和
    predict = kmeans.fit_predict(data)
    sc.append(silhouette_score(data, predict) ) #轮廓系数

plt.rcParams['font.sans-serif'] = ['SimHei']	# 显示中文
plt.rcParams['axes.unicode_minus'] = False		# 显示负号

fig = plt.figure(figsize=(15,5))
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2) 
ax1.plot(k_range,sc)  
ax1.set(title ="轮廓系数",xlabel="k",ylabel="silhouette coefficient" )
ax2.plot(k_range,sse)       
ax2.set(title ="肘方法",xlabel="k",ylabel="sum of the squared errors")  
fig.suptitle("选取合适k值")                                                       
plt.show()



