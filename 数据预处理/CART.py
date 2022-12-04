import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.model_selection import train_test_split
import math
from sklearn.metrics import r2_score

csv =  pd.read_csv('数据预处理/processedDataForCalculate.csv',header=None,delimiter=',')

x = csv.iloc[:,0:-1].values
#'区','所处楼层级别','总楼层数','建造年份','面积','朝向','是否近地铁','挂牌年','挂牌月','挂牌日','纬度','经度'
y = csv.iloc[:, -1].values
#'总价'

x_train,x_test,y_train,y_test = train_test_split(
    x,y, test_size = 0.5,random_state = 12)

cart = tree.DecisionTreeRegressor(random_state = 20,max_depth=5)

cart.fit(x_train,y_train)

'''
lb = [7,2,38,2009,155.79,4,0,2019,10,7,30.655936231979364,104.08961712994609]
lb = np.array(lb).reshape(1,-1)
print(lb)
print(cart.predict(lb))
'''

bias = []
y_predict = cart.predict(x_test)

print(r2_score(y_test, y_predict))
print(cart.score(x_test, y_test)) #都是决定系数（R2）

print('平均绝对误差 MAE = ',end='')
print(np.sum( np.absolute(y_test-y_predict) )/len(y_predict))

print('均方根误差 RMSE = ',end='')
print(np.sqrt(np.sum( (y_test-y_predict)**2 )/len(y_predict)))


import graphviz
import os
from IPython.display import Image  
import pydotplus

features = ['district','floorrank','totalfloor','year','area','ori','subway','hangoutyear','hangoutmonth','hangoutday','latitude','longitude']
#features = ['区','所处楼层级别','总楼层数','建造年份','面积','朝向','是否近地铁','挂牌年','挂牌月','挂牌日','纬度','经度']
classes=[]
# 定义图像
tree_graph_data = tree.export_graphviz(cart,
                    feature_names=features,
                     class_names=classes,
                    filled=True,
                    rounded=True,
                    )
# 绘图：
graph = graphviz.Source(tree_graph_data)
graph.render("tree",directory ='./', format='png')
