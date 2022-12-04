import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('processedDataForVisual.csv')

data = data.iloc[:,1:]

data_corr = data.corr()
plt.figure(figsize=(25,25),dpi=200)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
sns.set(font='SimHei',font_scale=1.5)  # 解决Seaborn中文显示问题并调整字体大小

# 使用mask去掉上半
mask = np.zeros_like(data_corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

sns.heatmap(data_corr,
            mask=mask,
            annot=True,
            vmax=1,
            square=True,
            cmap="Greens")
plt.savefig('./correlation.png')
plt.show()