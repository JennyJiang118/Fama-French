#!/usr/bin/env python
# coding: utf-8

# In[35]:


import statsmodels.api as sm
import pandas as pd
import numpy as np
import os.path as path

root = path.abspath(".")


# In[36]:


file = "/factors.csv"
data = pd.read_csv(root+file)


# In[24]:


data.head()


# In[37]:


data.index = data.ym
data.head()


# In[38]:


data['Intercept']=1
x=data[['SMB','HML','RMW','CMA','rm-rf','Intercept']]
x.head()


# In[39]:


# 建立列表储存回归系数和R方
r2=[]
betas=[]
t=[]
p=[]


# In[40]:


data = data.drop(['ym','rf','rm-rf','SMB','HML','RMW','CMA','Intercept'],axis=1)
data.head()


# In[41]:


for i in range(18):
    y=data.loc[:,data.columns[i]]
    mod=sm.OLS(y,x).fit()
    
    r2.append([data.columns[i],mod.rsquared])
    betas.append([data.columns[i]]+list(mod.params))
    t.append([data.columns[i]]+list(mod.tvalues))
    p.append([data.columns[i]]+list(mod.pvalues))


# In[42]:


p=pd.DataFrame(p,columns=['group','SMB','HML','RMW','CMA','mkt_rf','Intercept'])
t=pd.DataFrame(t,columns=['group','SMB','HML','RMW','CMA','mkt_rf','Intercept'])
betas=pd.DataFrame(betas,columns=['group','SMB','HML','RMW','CMA','mkt_rf','Intercept'])
r2=pd.DataFrame(r2,columns=['group','r2'])


# In[43]:


betas


# In[44]:


t


# In[45]:


r2


# In[46]:


p


# In[49]:


f5 = pd.read_excel(root+"/五因子序列最终版.xlsx")
f5.head()


# In[ ]:




