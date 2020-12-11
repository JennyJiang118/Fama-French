#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 19:11:35 2020

@author: wangtiancheng
"""

import pandas as pd
import numpy as np
import os.path as path

root = path.abspath(".")

sizefile = "/size.xlsx"
hmlfile = "/hml.csv"
opfile = "/OP.xlsx"
invfile = "/INV.csv"
#%%
f = pd.read_excel(root+sizefile,converters ={u'Stkcd':str})

hml = pd.read_csv(root+hmlfile)
hml = hml[['Stkcd','ym','group_BM']]

op = pd.read_excel(root+opfile,converters ={u'Accper':int})
op.columns = ['Stkcd','ym','op','group_OP']
op = op[['Stkcd','ym','group_OP']]

inv = pd.read_csv(root+invfile)
inv = inv[['Stkcd','ym','group_INV']]

#%%
op.Stkcd = op.Stkcd.apply(lambda x :int(x))
op.Stkcd = op.Stkcd.apply(lambda x : str(x+1000000)[-6:])
hml.Stkcd = hml.Stkcd.apply(lambda x: str(x+1000000)[-6:])
inv.Stkcd = inv.Stkcd.apply(lambda x: str(x+1000000)[-6:])

#%%
# 因子合并
f = pd.merge(f,hml,how='inner',left_on=['Stkcd','ym'],right_on=['Stkcd','ym'])
f = pd.merge(f,op,how='inner',left_on=['Stkcd','ym'],right_on=['Stkcd','ym'])
f = pd.merge(f,inv,how='inner',left_on=['Stkcd','ym'],right_on=['Stkcd','ym'])


#%%
# 将SIZE与其余三个因子列合并为新的一列代表其属性

f['portfolio_name_hml']=f['group_SIZE']+'/'+f['group_BM']
f['portfolio_name_op']=f['group_SIZE']+'/'+f['group_OP']
f['portfolio_name_inv']=f['group_SIZE']+'/'+f['group_INV']
#%%
#f.to_excel(root+"/Ri.xlsx",index=False)

#%%
# 构造HML因子(第一个2*3):将每个月按SIZE和BM分组，计算组内各支股票收益率市值加权综合收益率
port_ret_hml=f.groupby(['ym','portfolio_name_hml']).apply(lambda x: (x['ret']*x['mkt']).sum()/x.mkt.sum())
port_ret_hml=port_ret_hml.reset_index()
port_ret_hml.rename(columns={port_ret_hml.columns[-1]:'ret'},inplace=True) #重命名一下
port_ret_hml=port_ret_hml.pivot(index='ym',columns='portfolio_name_hml',values='ret')

# SMB_bm = （SL + SM +SH）/3 -(BL + BM +BH)/3
port_ret_hml['SMB_bm']=(port_ret_hml['S/L']+port_ret_hml['S/M']+port_ret_hml['S/H'])/3-(port_ret_hml['B/L']+port_ret_hml['B/M']+port_ret_hml['B/H'])/3
# HML = (SH + BH)/2 - (SL + BL)/2
port_ret_hml['HML']=(port_ret_hml['S/H']+port_ret_hml['B/H'])/2-(port_ret_hml['S/L']+port_ret_hml['B/L'])/2
port_ret_hml.to_excel(root+"/HML因子.xlsx",index = True)

#%%
# 构造RMW因子
port_ret_op=f.groupby(['ym','portfolio_name_op']).apply(lambda x: (x['ret']*x['mkt']).sum()/x.mkt.sum())
port_ret_op=port_ret_op.reset_index()
port_ret_op.rename(columns={port_ret_op.columns[-1]:'ret'},inplace=True) #重命名一下
port_ret_op=port_ret_op.pivot(index='ym',columns='portfolio_name_op',values='ret')
#%%
port_ret_op['SMB_op']=(port_ret_op['S/L']+port_ret_op['S/M']+port_ret_op['S/H'])/3-(port_ret_op['B/L']+port_ret_op['B/M']+port_ret_op['B/H'])/3
# RMW = (SH + BH)/2 - (SL + BL)/2
port_ret_op['RMW']=(port_ret_op['S/H']+port_ret_op['B/H'])/2-(port_ret_op['S/L']+port_ret_op['B/L'])/2
port_ret_op.to_excel(root+"/RMW因子.xlsx",index = True)

#%%
# 构造CMA因子
port_ret_inv=f.groupby(['ym','portfolio_name_inv']).apply(lambda x: (x['ret']*x['mkt']).sum()/x.mkt.sum())
port_ret_inv=port_ret_inv.reset_index()
port_ret_inv.rename(columns={port_ret_inv.columns[-1]:'ret'},inplace=True) #重命名一下
port_ret_inv=port_ret_inv.pivot(index='ym',columns='portfolio_name_inv',values='ret')

#%%
port_ret_inv=port_ret_inv.fillna(0)
port_ret_inv['SMB_inv']=(port_ret_inv['S/C']+port_ret_inv['S/N']+port_ret_inv['S/A'])/3-(port_ret_inv['B/C']+port_ret_inv['B/N']+port_ret_inv['B/A'])/3

port_ret_inv['CMA']=(port_ret_inv['S/C']+port_ret_inv['B/C'])/2-(port_ret_inv['S/A']+port_ret_inv['B/A'])/2
port_ret_inv.to_excel(root+"/CMA因子.xlsx",index = True)

#%%
# 构造SMB
ret_hml = port_ret_hml[['SMB_bm','HML']]
ret_op = port_ret_op[['SMB_op','RMW']]
ret_inv = port_ret_inv[['SMB_inv','CMA']]

#%%


#%%
factor = pd.merge(ret_hml,ret_op,left_index=True,right_index=True)
factor = pd.merge(factor,ret_inv,left_index=True,right_index=True)
factor['SMB'] = (factor['SMB_bm'] + factor['SMB_op'] + factor['SMB_inv'])/3
factor = factor[['SMB','HML','RMW','CMA']]


#%%
# 
rm_rf = pd.read_excel(root+"/Rm-Rf.xlsx")
rm_rf.index = rm_rf['ym']
factor = pd.merge(factor,rm_rf,left_index=True,right_index=True)

factor = factor.drop(['ym','rm'],axis = 1)
#%%
factor.to_excel(root+"/五因子序列最终版.xlsx")

#%%
import seaborn as sns
sns.heatmap(factor[['SMB','HML','RMW','CMA','rm-rf']].corr(),cmap="Reds")
