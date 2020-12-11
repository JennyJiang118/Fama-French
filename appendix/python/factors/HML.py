#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd


#%%
#---------------------------size------------------------#
file1 = "/Users/osx/Downloads/ff5f_data/stockmnth/TRD_Mnth0.xlsx"
file2 = "/Users/osx/Downloads/ff5f_data/stockmnth/TRD_Mnth1.xlsx"
file3 = "/Users/osx/Downloads/ff5f_data/stockmnth/TRD_Mnth2.xlsx"

data1 = pd.read_excel(file1,converters = {u'Stkcd':int, u'Trdmnt':str})
data2 = pd.read_excel(file2,converters = {u'Stkcd':int, u'Trdmnt':str})
data3 = pd.read_excel(file3,converters = {u'Stkcd':int, u'Trdmnt':str})


size = pd.DataFrame(data1.append(data2))
size = size.append(data3)
size = size.sort_values(['Trdmnt','Stkcd'], ascending=[True, True])

size['ym']=size.Trdmnt.apply(lambda x : int(x[:4])*100 + int(x[-2:]))
size ['tag'] = (size['ym'].astype(int) / 3).astype(int)
size = size[['Stkcd', 'Msmvosd', 'ym', 'tag']]


#%%
#----------------------------equity--------------------------#
file_1 = "/Users/osx/Downloads/ff5f_data/Balance sheet/FS_Combas1.xlsx"
file_2 = "/Users/osx/Downloads/ff5f_data/Balance sheet/FS_Combas2.xlsx"
file_3 = "/Users/osx/Downloads/ff5f_data/Balance sheet/FS_Combas3.xlsx"


data_1 = pd.read_excel(file_1,converters = {u'Accper':str})
data_2 = pd.read_excel(file_2,converters = {u'Accper':str})
data_3 = pd.read_excel(file_3,converters = {u'Accper':str})

equity = pd.DataFrame(data_1.append(data_2))
equity = equity.append(data_3)
equity = equity[equity["Typrep"].str.contains("A")]

# ym
equity['ym'] = equity.Accper.apply(lambda x : int(x[:4])*100 + int(x[5:7]))
equity['tag'] = (equity['ym'].astype(int) / 3).astype(int)
equity = equity[['Stkcd', 'total_equity', 'tag']]

#%%
# 补全每个月的equity
# tag相同的共享equity

bm_merge = pd.merge(size, equity, how = 'inner', left_on=['Stkcd', 'tag'], right_on=['Stkcd', 'tag'])
bm_merge = bm_merge.sort_values(['ym','Stkcd'], ascending=[True, True])


#%%
#-----------------------------bm-----------------------#
# “账面市值比”(BM)是用第t-1年末的“账面价值/股票i的流通市值”
bm_merge['bm'] = 100


bm_merge = bm_merge.sort_values(['Stkcd','ym'], ascending=[True, True])
tmp = pd.DataFrame(bm_merge[['total_equity']])
tmp['total_equity'] = tmp['total_equity'].shift()
tmp.loc[0,'total_equity'] = tmp.loc[1, 'total_equity']
bm_merge['bm'] = tmp['total_equity']/bm_merge['Msmvosd']




#%%
#----------------------------HML----------------------#
hml = bm_merge[['Stkcd','ym','bm']]
hml['group_BM'] = 'M'

hml.loc[hml['bm']>=hml['bm'].quantile(0.7), 'group_BM'] = 'H'
hml.loc[hml['bm']<=hml['bm'].quantile(0.3), 'group_BM'] = 'L'

#hml['Stkcd'] = str(hml['Stkcd']+1000000)[1:]

for i in range(len(hml)):
    hml.loc[i,'Stkcd']=str(int(hml.loc[i,'Stkcd'])+1000000)[1:]

hml.to_csv('/Users/osx/Downloads/hml.csv')



