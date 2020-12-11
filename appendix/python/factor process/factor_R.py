#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file = "/Users/osx/Downloads/factors.csv"
data = pd.read_csv(file)

#Ri-Rf=ai+bi*(Rm-Rf)+si*SMB+hi*HML+ri*RMW+ci*CMA+ei

data = data[['ym','SMB','HML','RMW','CMA','rm-rf','rf']]
data_plot = data[['SMB','HML','RMW','CMA','rm-rf','rf']]+1
plt.figure()
plt.plot((data[['SMB','HML','RMW','CMA','rm-rf','rf']]+1).cumprod())
label = ['SMB','HML','RMW','CMA','rm-rf','rf']
plt.legend(label)
plt.xlabel('num of months after 2014.8')
plt.ylabel('accumulated return')
plt.show()

cor = data[['SMB','HML','RMW','CMA','rm-rf']].corr()

