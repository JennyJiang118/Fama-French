import pandas as pd
import numpy as np
import xlsxwriter
import numpy as np
from sklearn import datasets, linear_model

file_path = open("C:/Users/tuxin/Documents/Tencent Files/1351064726/FileRecv/hml_7.csv")
data = pd.read_csv(file_path)
datalist = data.values.tolist()

file_path = open("C:/Users/tuxin/Documents/Tencent Files/1351064726/FileRecv/factors.csv")
data2 = pd.read_csv(file_path)
data22 = pd.DataFrame(data2.values.T, index=data2.columns, columns=data2.index)
data22list = data22.values.tolist()

X = datalist

number = np.zeros(18)
ai = np.zeros(18)
bi = np.zeros(18)
si = np.zeros(18)
hi = np.zeros(18)
ri = np.zeros(18)
ci = np.zeros(18)

# 训练数据
for i in range(7, 25):
    regr = linear_model.LinearRegression()
    Y = data22list[i]
    regr.fit(X, Y)
    #print(len(regr.coef_))
    #print(type(regr.intercept_))
    print("第", i-6, "组回归结果：")
    print('bi、si、hi、ri、ci分别为：', regr.coef_)
    print('ai为：', regr.intercept_)
    ai[i - 7] = regr.intercept_
    bi[i - 7] = regr.coef_[0]
    si[i - 7] = regr.coef_[1]
    hi[i - 7] = regr.coef_[2]
    ri[i - 7] = regr.coef_[3]
    ci[i - 7] = regr.coef_[4]



for i in range(0, 18):
    number[i] = i + 1
workbook = xlsxwriter.Workbook('regression.xlsx')
worksheet = workbook.add_worksheet()
headings = ['number', 'ai', 'bi', 'si', 'hi', 'ri', 'ci']
bold = workbook.add_format({'bold': 1})
worksheet.write_row('A1', headings, bold)
worksheet.write_column('A2', number)
worksheet.write_column('B2', ai)
worksheet.write_column('C2', bi)
worksheet.write_column('D2', si)
worksheet.write_column('E2', hi)
worksheet.write_column('F2', ri)
worksheet.write_column('G2', ci)
workbook.close()