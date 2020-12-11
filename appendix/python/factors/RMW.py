import pandas as pd
import numpy as np
import xlsxwriter
from datetime import datetime

'''file_path = open("C:/Users/tuxin/Desktop/ff5f_data/ff5f_data/Balance sheet/balance sheet.csv")
data = pd.read_csv(file_path)
data = data[data['Accper'].str.contains('6')]
datalist = data.values.tolist()'''

data1 = pd.read_excel(r"C:/Users/tuxin/Desktop/ff5f_data/ff5f_data/Balance sheet/FS_Combas1.xlsx")
data2 = pd.read_excel('C:/Users/tuxin/Desktop/ff5f_data/ff5f_data/Balance sheet/FS_Combas2.xlsx')
data3 = pd.read_excel('C:/Users/tuxin/Desktop/ff5f_data/ff5f_data/Balance sheet/FS_Combas3.xlsx')

income1 = pd.read_excel(r"C:/Users/tuxin/Desktop/ff5f_data/ff5f_data/Income statement/FS_Comins1.xlsx")
income2 = pd.read_excel('C:/Users/tuxin/Desktop/ff5f_data/ff5f_data/Income statement/FS_Comins2.xlsx')
income3 = pd.read_excel('C:/Users/tuxin/Desktop/ff5f_data/ff5f_data/Income statement/FS_Comins3.xlsx')

#筛选A数据
data1 = data1[data1['Typrep'].str.contains('A')]
data2 = data2[data2['Typrep'].str.contains('A')]
data3 = data3[data3['Typrep'].str.contains('A')]

data1 = data1[~data1['Accper'].str.contains('01-01')]
data2 = data2[~data2['Accper'].str.contains('01-01')]
data3 = data3[~data3['Accper'].str.contains('01-01')]

data1list = data1.values.tolist()
data2list = data2.values.tolist()
data3list = data3.values.tolist()
datalist = data1list + data2list + data3list

income1 = income1[~income1['Accper'].str.contains('01-01')]
income2 = income2[~income2['Accper'].str.contains('01-01')]
income3 = income3[~income3['Accper'].str.contains('01-01')]

#筛选A数据
income1 = income1[income1['Typrep'].str.contains('A')]
income2 = income2[income2['Typrep'].str.contains('A')]
income3 = income3[income3['Typrep'].str.contains('A')]

income1list = income1.values.tolist()
income2list = income2.values.tolist()
income3list = income3.values.tolist()
incomelist = income1list + income2list + income3list

incomepd = pd.DataFrame(incomelist)
incomepd2 = pd.DataFrame(incomepd.values.T, index=incomepd.columns, columns=incomepd.index)
incomepdlist = incomepd2.values.tolist()
#print(incomepdlist[0])

output = np.zeros(len(incomelist))
'''for i in range(1, len(output)):
    for j in range(1, len(datalist)):
        if(incomelist[i-1][0] == incomelist[i][0]):
            if(datalist[j][1] == incomelist[i][0] and (pd.to_datetime(incomelist[i-1][1])-pd.to_datetime(datalist[j][2])).days == 0):
                output[i] = incomelist[i-1][3]/datalist[j][6]
                print(output[i])'''

for i in range(1, len(output)):
    if(incomelist[i-1][0] == incomelist[i][0]):
        output[i] = incomelist[i-1][3]/datalist[i-1][6]



op = np.zeros(3*len(output))
stkcd = np.zeros(3*len(output))
for i in range(0, len(output)):
    op[3*i] = output[i]
    op[3*i+1] = output[i]
    op[3*i+2] = output[i]
    stkcd[3*i] = incomepdlist[0][i] + 1000000
    stkcd[3*i+1] = incomepdlist[0][i] + 1000000
    stkcd[3*i+2] = incomepdlist[0][i] + 1000000

stk1 = incomepdlist[1]
stk2 = incomepdlist[1]
stk3 = incomepdlist[1]
stk = stk1 + stk2 + stk3

for i in range(0, 3*len(output)):
    t = str(stkcd[i])
    stk[i] = t[1:len(t)]


time = np.zeros(3*len(output))
for i in range(0, 12):
    time[i] = 201400 + i + 1
for i in range(12, 54):
    time[i] = time[i-12] + 100
for i in range(54, len(time)):
    time[i] = time[i-54]

workbook = xlsxwriter.Workbook('output.xlsx')
worksheet = workbook.add_worksheet()
headings = ['Stkcd', 'Accper', 'OP']
bold = workbook.add_format({'bold': 1})
worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', stk)
worksheet.write_column('B2', time)
worksheet.write_column('C2', op)
workbook.close()


hml = pd.read_excel('output.xlsx')
hml['Group_OP'] = 'M'
hml.loc[hml['OP'] >= hml['OP'].quantile(0.7), 'Group_OP'] = 'H'
hml.loc[hml['OP'] <= hml['OP'].quantile(0.3), 'Group_OP'] = 'L'

hml2 = pd.DataFrame(hml.values.T, index=hml.columns, columns=hml.index)
hml2list = hml2.values.tolist()

workbook = xlsxwriter.Workbook('OP.xlsx')
worksheet = workbook.add_worksheet()
headings = ['Stkcd', 'Accper', 'OP', 'Group_OP']
bold = workbook.add_format({'bold': 1})
worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', stk)
worksheet.write_column('B2', time)
worksheet.write_column('C2', op)
worksheet.write_column('D2', hml2list[3])
workbook.close()