import pandas as pd
from pylab import mpl
import datetime as dt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from collections import defaultdict

import jieba
import jieba.analyse
import numpy as np
import seaborn as sns




#===============================================================================


#===============================================================================

# t='''
# Wed Jan  1 01:12:26 2020
# Sat Jan 11 00:52:52 2020
# '''

#===============================================================================
sns.set(style='whitegrid')

mpl.rcParams['font.sans-serif']='SimHei'
df = pd.read_excel(r'/Users/chuhsinan/Downloads/專題/Report fin.xlsx')

df['CVS'] = df['CVS'].astype('category')
# df.info()

for i in df['Review']:
    imp = jieba.analyse.textrank(i, topK=3, withWeight=True)
    print(imp)


