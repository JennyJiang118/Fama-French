#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 14:21:16 2020

@author: wangtiancheng
"""
#%%
import pandas as pd
import numpy as np


import os.path as path
root = path.abspath(".")

file1 = "/stockmnth/TRD_Mnth0.xlsx"
file2 = "/stockmnth/TRD_Mnth1.xlsx"
file3 = "/stockmnth/TRD_Mnth2.xlsx"

data1 = pd.read_excel(root+file1,converters = {u'Stkcd':str, u'Trdmnt':str})
data2 = pd.read_excel(root+file2,converters = {u'Stkcd':str, u'Trdmnt':str})
data3 = pd.read_excel(root+file3,converters = {u'Stkcd':str, u'Trdmnt':str})
#%%
size = pd.DataFrame(data1.append(data2))
size = size.append(data3)
size = size.sort_values(['Trdmnt','Stkcd'], ascending=[True, True])
#%%
size['ym']=size.Trdmnt.apply(lambda x : int(x[:4])*100 + int(x[-2:]))
#%%
#筛选6月数据

#size_6 = size.loc[size.ym % 10 ==6].copy()

#size_6 = size[['Stkcd','Trdmnt','Msmvosd']]

#%%
#根据6月市值分组
def split_SIZE(x):
    x.loc[x['Msmvosd'] >= x['Msmvosd'].mean(),'group_SIZE']='B'
    return x

size['group_SIZE'] = 'S'
size=size.groupby('Trdmnt').apply(split_SIZE).reset_index(drop=True)
# size_6['group_SIZE']='S'
# size_6=size_6.groupby('Trdmnt').apply(split_SIZE).reset_index(drop=True)
#%%
#输出
size_output = size[['Stkcd','ym','Mretwd','Msmvosd','group_SIZE']]
size_output.columns = ['Stkcd','ym','ret','mkt','group_SIZE']
#%%
size_output.to_excel(root+"/group_size.xlsx",index=False)
#%%
# 将ym重新命名为portfolio_dates,指按SIZE标记所对应的分组月
# size_6.rename(columns={'ym':'portfolio_dates'},inplace=True)
#%%
# 上述工作只完成了每只股票在每年6月的标记，其在接下来每年7月到下一年6月标记不变
# 每年6月到次年6月则为一个周期，在此期间，两个因子分组结果不变

# # 首先在原始数据上生成一个对应的portfolio_dates，同一周期内该值不变
# size['portfolio_dates']=size['Trdmnt'].apply(lambda x:int(x[:4])*100+6 if int(x[-2:])>6 else (int(x[:4])-1)*100+6)

# #%%
# # 使用pandas.merge()函数几个将标记与原始数据对应上
# # 注：按道理此处应当使用外连接，但是由于可能有股票是7月以后为第一个月的交易数据，
# # 没有6月的数据，则在当年6月无法生成对应标记，在未来一个周期则会标记缺失，此处避免缺失使用内连接
# size_6_merge = size_6[['Stkcd','portfolio_dates','group_SIZE']]
# size_merge=pd.merge(size,size_6_merge,how='inner',left_on=['Stkcd','portfolio_dates'],right_on=['Stkcd','portfolio_dates'])


# #%%
# # 将每个月按SIZE分组，计算组内各支股票收益率市值加权综合收益率
# port_ret=size_merge.groupby(['Trdmnt','group_SIZE']).apply(lambda x: (x['Mretwd']*x['Msmvosd']).sum()/x.Msmvosd.sum())
# port_ret=port_ret.reset_index()
# port_ret.rename(columns={port_ret.columns[-1]:'ret'},inplace=True) #重命名一下

# port_ret=size.groupby(['Trdmnt','group_SIZE']).apply(lambda x: (x['Mretwd']*x['Msmvosd']).sum()/x.Msmvosd.sum())
# port_ret=port_ret.reset_index()
# port_ret.rename(columns={port_ret.columns[-1]:'ret'},inplace=True) #重命名一下

# #%%
# # 改变一下表格形式，使用透视表功能
# port_ret=port_ret.pivot(index='Trdmnt',columns='group_SIZE',values='ret')
# port_ret.head()

# #%%
# #构造smb因子
# port_ret['SMB']=port_ret['S']-port_ret['B']

#%%
# 输出SMB因子
#port_ret.to_excel(root+"SMB.xlsx")

