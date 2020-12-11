#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 16:36:52 2020

@author: wangtiancheng
"""

import pandas as pd
import numpy as np
import os.path as path

root = path.abspath(".")
rmfile = "/mktmnth/TRD_Cnmont.xlsx"
rmfile1 = "/mktmnth/TRD_Cnmont1.xlsx"
rm = pd.read_excel(root+rmfile)
rm1 = pd.read_excel(root+rmfile1)
rm = rm1.append(rm)

rm = rm[rm['Markettype']==5]

#%%
rm['ym']=rm.Trdmnt.apply(lambda x : int(x[:4])*100 + int(x[-2:]))
#%%
rm = rm[['ym','Cmretwdos']]

#%%
rffile = "/rf/TRD_Nrrate.xlsx"
rf = pd.read_excel(root+rffile)
#%%
rf_0 = rf.iloc[0:1,]
rf = rf[rf['Clsdt'].str.contains('28')]
rf = rf_0.append(rf)
rf['ym']=rf.Clsdt.apply(lambda x : int(x[:4])*100 + int(x[-5:-3]))
#%%
rf = rf[['ym','Nrrmtdt']]
rm_rf = pd.merge(rm,rf,left_on=['ym'],right_on=['ym'])
#%%
rm_rf.columns = ['ym','rm','rf']
rm_rf['rf'] = rm_rf['rf']/100
rm_rf['rm-rf'] = rm_rf['rm']-rm_rf['rf']

#%%
rm_rf.to_excel(root+"/Rm-Rf.xlsx",index=False)
