import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import BaggingRegressor

from sklearn.metrics import mean_squared_error # 均方误差
from sklearn.metrics import mean_absolute_error # 平方绝对误差
from sklearn.metrics import r2_score #决定系数（R2）

csv =  pd.read_csv('数据预处理/processedDataForCalculate.csv',header=None,delimiter=',')

x = csv.iloc[:,0:-1].values
#'区','所处楼层级别','总楼层数','建造年份','面积','朝向','是否近地铁','挂牌年','挂牌月','挂牌日','纬度','经度'
y = csv.iloc[:, -1].values
#'总价'

x_train,x_test,y_train,y_test = train_test_split(
    x,y, test_size = 0.7,random_state = 12)

models=[LinearRegression(),KNeighborsRegressor(),SVR(),Ridge(),Lasso(),MLPRegressor(alpha=20),DecisionTreeRegressor(),ExtraTreeRegressor(),XGBRegressor(),RandomForestRegressor(),AdaBoostRegressor(),GradientBoostingRegressor(),BaggingRegressor()]
models_str=['LinearRegression','KNNRegressor','SVR','Ridge','Lasso','MLPRegressor','DecisionTree','ExtraTree','XGBoost','RandomForest','AdaBoost','GradientBoost','Bagging']
mae_ =[]
mse_ =[]
score_ =[]


for name,model in zip(models_str,models):
    print('开始训练模型：'+name)
    model=model   #建立模型
    model.fit(x_train,y_train)
    y_pred=model.predict(x_test)  
    mae=mean_absolute_error(y_test, y_pred).round(decimals=2)
    mse=mean_squared_error(y_test, y_pred).round(decimals=2)
    score=r2_score(y_test, y_pred).round(decimals=2)
    mae_.append(mae)
    mse_.append(mse)
    score_.append(score)
    print(name +' MAE:'+str(mae)+' MSE:'+str(mse)+' r2_score:'+str(score))


newdata =  np.hstack((np.array(models_str).reshape(-1,1),
                     np.array(mae_).reshape(-1,1),
                     np.array(mse_).reshape(-1,1),
                     np.array(score_).reshape(-1,1)))
newdata = pd.DataFrame(newdata)
newdata.columns = ['模型','MAE','MSE','r2_score']
newdata.to_csv('classifiers.csv',index=False,encoding="utf_8_sig",sep=',')