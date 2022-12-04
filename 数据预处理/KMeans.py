import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from sklearn import preprocessing

csv =  pd.read_csv('数据预处理/processedDataForCalculate.csv',header=None,delimiter=',')

data = csv.values

for i in range(19998):
    data[i][12] = data[i][12]/data[i][4]  #单价

kmeans = KMeans(n_clusters=11)
kmeans.fit(data)
y = kmeans.fit_predict(data)

plt.rcParams['font.sans-serif'] = ['SimHei']	# 显示中文
plt.rcParams['axes.unicode_minus'] = False		# 显示负号
'''
fig = plt.figure(figsize=(10,10))
ax= Axes3D(fig)
ax.scatter(data[:,4],data[:,12],data[:,5],c=y,marker='*')
ax.set_xlabel("面积")
ax.set_ylabel("单价")
ax.set_zlabel("总楼层数")

ax.set_xlim(0,300)
ax.set_ylim(0,7)
plt.show()
'''

fig = plt.figure(figsize=(10,10))
ax=fig.add_subplot(1,1,1)
plt.scatter(data[:,4],data[:,12],c=y,marker='*')
ax.set_xlabel("面积")
ax.set_ylabel("单价")

ax.set_xlim(0,300)
ax.set_ylim(0,7)
plt.show()