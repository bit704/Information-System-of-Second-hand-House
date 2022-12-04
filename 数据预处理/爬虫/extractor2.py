import re
import os
import numpy as np
import pandas as pd

location = []
for i in range(20000):
    filename = 'xiaoqu_pages\\'+str(i)+'.txt'
    if os.path.exists(filename):
        with open(filename,'r',encoding='utf-8') as f:
            string = f.read()
            obj = re.search(r'<div class="sub">\n\s+\((.*?)\)\n\s+(.*?)\n',string)
            if obj != None:
                streetnumber = obj.group(2)
                streetnumber = streetnumber.split(",")[0]
                streetnumber = streetnumber.split("（")[0]
                streetnumber = streetnumber.split("(")[0]
                site = obj.group(1)+"区"+streetnumber
                #print(site)
                location.append(site)
            else:
                location.append(-1)
    else:
        location.append(-1)
 
location = np.array(location)
hd = pd.DataFrame(location)
hd.to_csv('location.csv',index=False,header=False,encoding="utf_8_sig")

#提取小区的地址
