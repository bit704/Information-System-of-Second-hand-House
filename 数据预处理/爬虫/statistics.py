import numpy as np
import pandas as pd

temp_csv =  pd.read_csv('latitude.csv',header=None,delimiter=',',error_bad_lines=False)
temp = temp_csv.iloc[:].values


print(temp)
temp = temp.flatten()

u = []

for i in range(20000):
    if temp[i] != -1:
        u.append(temp[i])

u=np.array(u)
print(u.mean())
    