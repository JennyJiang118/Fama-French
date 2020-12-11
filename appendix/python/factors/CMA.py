'''
计算“投资风格”(INV)
用第t - 1
年末相对于第t - 2
年末的总资产增加额，除以第t - 2
年末的总资产
现有2014 - 2017
年
12.31
日年末数据
因此可以计算2016 - 2018
年
"投资风格"

因为年度数据不足，现用季度数据替代年，月度数据用年填充
'''

#%%
#导入数据
import pandas as pd



file1 = "/Users/osx/Downloads/ff5f_data/Balance sheet/FS_Combas1.xlsx"
file2 = "/Users/osx/Downloads/ff5f_data/Balance sheet/FS_Combas2.xlsx"
file3 = "/Users/osx/Downloads/ff5f_data/Balance sheet/FS_Combas3.xlsx"

df1 = pd.read_excel(file1)
df2 = pd.read_excel(file2)
df3 = pd.read_excel(file3)
#合成一个dataframe
df=pd.concat([df1, df2, df3],ignore_index=True)

#%%
#数据归约
#剔除母公司报表数据
df=df[df['Typrep']=='A']
#剔除权益合计、负债合计
df=df.drop(columns=['tptal_liability','total_equity'])
#剔除1月1日数据
df=df[~df['Accper'].str.contains('01-01')]
#加入年份月份
df['ym']=df.Accper.apply(lambda x : int(x[0:4])*100 + int(x[5:7]))
df['Year']=df.Accper.apply(lambda x : int(x[0:4]))


#%%
#calculate INV
ymlist=df['ym'].tolist()
assetlist=df['total_assets'].tolist()
INVlist=[0.03]*len(ymlist)
for x in range(2,len(ymlist)):
    #每只股票的前两个季度数据无法计算，因为不存在t-1和t-2
    if ymlist[x]==201403 or ymlist[x]==201406:
         continue
    if ymlist[x]%100==9 or ymlist[x]%100==12:
        if ymlist[x-1]==ymlist[x]-3 and ymlist[x-2]==ymlist[x]-6:
            INVlist[x]=(assetlist[x-1]-assetlist[x-2])/assetlist[x-2]
    elif ymlist[x]%100==6:
        if ymlist[x-1]==ymlist[x]-3 and ymlist[x-2]==ymlist[x]-94:
            INVlist[x]=(assetlist[x-1]-assetlist[x-2])/assetlist[x-2]
    elif ymlist[x]%100==3:
        if ymlist[x-1]==ymlist[x]-91 and ymlist[x-2]==ymlist[x]-94:
            INVlist[x]=(assetlist[x-1]-assetlist[x-2])/assetlist[x-2]




#%%
#另存为INV dataframe
df['inv']=INVlist
INV=df[['Stkcd','ym','inv']]
INV['tag'] = (INV['ym'].astype(int)/3).astype(int)
INV = INV[['Stkcd','inv','tag']]

#%%
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
size = size[['Stkcd', 'Msmvosd','ym', 'tag']]

INV_merge = pd.merge(size, INV, how = 'inner', left_on=['Stkcd', 'tag'], right_on=['Stkcd', 'tag'])



#%%
#保留有效的INV数值,-1为无效值
#INV=INV[INV['INV']!=-1]
#INV.reset_index(drop=True, inplace=True)

#打上C/N/A标签,代表投资风格激进，居中，稳健
INV_merge['group_INV'] = 'N'

INV_merge.loc[INV_merge['inv']>=INV_merge['inv'].quantile(0.7), 'group_INV'] = 'C'
INV_merge.loc[INV_merge['inv']<=INV_merge['inv'].quantile(0.3), 'group_INV'] = 'A'

#%%
INV_merge.to_csv("/Users/osx/Downloads/INV.csv")
