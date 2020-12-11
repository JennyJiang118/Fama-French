#运行前请修改本机读取文件地址

#--------------------PYTHON文件夹--------------------#

factors是五因子数据获取文件夹：
CMA.py: 获取所有股票在所有时期的CMA分类、inv值
HML.py: 获取所有股票在所有时期的HML分类、bm值
RMW.py: 获取所有股票在所有时期的RMW分类、op值
Size.py: 获取所有股票在所有时期的size值
rm-rf.py：获取所有时期的rm-rf值


factors process是数据处理文件夹：
FAMA.py：获取所有时期的SMB、HML、RMW、CMA、rf、rm-rf值
factor_R.py：所有因子累计收益率可视化


regression是线性回归文件夹：
regression.py: 获取线性回归所得的系数
ptvalues.py：进行统计检验


#------------------IMPORTANT CSV文件夹----------------#

factors.csv：所有时期的五因子值、无风险利率、所有组合的超额收益率
regression.xlsx：线性回归系数
Ri.xlsx: 所有时期的五因子值、无风险利率




