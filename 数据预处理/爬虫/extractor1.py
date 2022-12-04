import re
import os
import numpy as np
import pandas as pd

hangoutdate = [[] for i in range(3)]
for i in range(20000):
    filename = 'ershoufang_pages\\'+str(i)+'.txt'
    if os.path.exists(filename):
        with open(filename,'r',encoding='utf-8') as f:
            string = f.read()
            obj = re.search(r'挂牌时间</span>(\d+)年(\d+)月(\d+)日', string)
            if obj != None:
                hangoutdate[0].append(obj.group(1))
                hangoutdate[1].append(obj.group(2))
                hangoutdate[2].append(obj.group(3))
                #print(i)
            else:
                hangoutdate[0].append(-1)
                hangoutdate[1].append(-1)
                hangoutdate[2].append(-1)
    else:
        hangoutdate[0].append(-1)
        hangoutdate[1].append(-1)
        hangoutdate[2].append(-1)
        
hangoutdate = np.array(hangoutdate)
hangoutdate = pd.DataFrame(hangoutdate)
hangoutdate.to_csv('hangoutdate.csv',index=False,header=False,encoding="utf_8_sig")

#提取挂牌时间
