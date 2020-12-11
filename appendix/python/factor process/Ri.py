import pandas as pd

#--------------------------read-----------------------#

file1 = '/Users/osx/Downloads/data.xlsx'
file2 = '/Users/osx/Downloads/Ri.xlsx'

data = pd.read_excel(file1, converters = {u'Stkcd':str,u'ym':str})
Ri = pd.read_excel(file2, converters={u'ym':str})

#--------------------------divide-----------------------#

#hml_BH
Ri['hml_BH'] = 0 #1
hml_BH = data[data['portfolio_name_hml']=='B/H'] #2
hml_BH = hml_BH[['Stkcd','ym','ret','mkt']] #2
hml_BH['weight'] = hml_BH['mkt']*hml_BH['ret'] #3


#hml_BM
Ri['hml_BM'] = 0
hml_BM = data[data['portfolio_name_hml']=='B/M']
hml_BM = hml_BM[['Stkcd','ym','ret','mkt']]
hml_BM['weight'] = hml_BM['mkt']*hml_BM['ret']

#hml_BL
Ri['hml_BL'] = 0
hml_BL = data[data['portfolio_name_hml']=='B/L']
hml_BL = hml_BL[['Stkcd','ym','ret','mkt']]
hml_BL['weight'] = hml_BL['mkt']*hml_BL['ret']

#hml_SH
Ri['hml_SH'] = 0
hml_SH = data[data['portfolio_name_hml']=='S/H']
hml_SH = hml_SH[['Stkcd','ym','ret','mkt']]
hml_SH['weight'] = hml_SH['mkt']*hml_SH['ret']

#hml_SM
Ri['hml_SM'] = 0
hml_SM = data[data['portfolio_name_hml']=='S/M']
hml_SM = hml_SM[['Stkcd','ym','ret','mkt']]
hml_SM['weight'] = hml_SM['mkt']*hml_SM['ret']

#hml_SL
Ri['hml_SL'] = 0
hml_SL = data[data['portfolio_name_hml']=='S/L']
hml_SL = hml_SL[['Stkcd','ym','ret','mkt']]
hml_SL['weight'] = hml_SL['mkt']*hml_SL['ret']

#op_BH
Ri['op_BH'] = 0
op_BH = data[data['portfolio_name_op']=='B/H']
op_BH = op_BH[['Stkcd','ym','ret','mkt']]
op_BH['weight'] = op_BH['mkt']*op_BH['ret']

#op_BM
Ri['op_BM'] = 0
op_BM = data[data['portfolio_name_op']=='B/M']
op_BM = op_BM[['Stkcd','ym','ret','mkt']]
op_BM['weight'] = op_BM['mkt']*op_BM['ret']

#op_BL
Ri['op_BL'] = 0
op_BL = data[data['portfolio_name_op']=='B/L']
op_BL = op_BL[['Stkcd','ym','ret','mkt']]
op_BL['weight'] = op_BL['mkt']*op_BL['ret']

#op_SH
Ri['op_SH'] = 0
op_SH = data[data['portfolio_name_op']=='S/H']
op_SH = op_SH[['Stkcd','ym','ret','mkt']]
op_SH['weight'] = op_SH['mkt']*op_SH['ret']

#op_SM
Ri['op_SM'] = 0
op_SM = data[data['portfolio_name_op']=='S/M']
op_SM = op_SM[['Stkcd','ym','ret','mkt']]
op_SM['weight'] = op_SM['mkt']*op_SM['ret']

#op_SL
Ri['op_SL'] = 0
op_SL = data[data['portfolio_name_op']=='S/L']
op_SL = op_SL[['Stkcd','ym','ret','mkt']]
op_SL['weight'] = op_SL['mkt']*op_SL['ret']

#inv_BN
Ri['inv_BN'] = 0
inv_BN = data[data['portfolio_name_inv']=='B/N']
inv_BN = inv_BN[['Stkcd','ym','ret','mkt']]
inv_BN['weight'] = inv_BN['mkt']*inv_BN['ret']


#inv_BA
Ri['inv_BA'] = 0
inv_BA = data[data['portfolio_name_inv']=='B/A']
inv_BA = inv_BA[['Stkcd','ym','ret','mkt']]
inv_BA['weight'] = inv_BA['mkt']*inv_BA['ret']


#inv_BC
Ri['inv_BC'] = 0
inv_BC = data[data['portfolio_name_inv']=='B/C']
inv_BC = inv_BC[['Stkcd','ym','ret','mkt']]
inv_BC['weight'] = inv_BC['mkt']*inv_BC['ret']

#inv_SA
Ri['inv_SA'] = 0
inv_SA = data[data['portfolio_name_inv']=='S/A']
inv_SA = inv_SA[['Stkcd','ym','ret','mkt']]
inv_SA['weight'] = inv_SA['mkt']*inv_SA['ret']

#inv_SN
Ri['inv_SN'] = 0
inv_SN = data[data['portfolio_name_inv']=='S/N']
inv_SN = inv_SN[['Stkcd','ym','ret','mkt']]
inv_SN['weight'] = inv_SN['mkt']*inv_SN['ret']

#inv_SC
Ri['inv_SC'] = 0
inv_SC = data[data['portfolio_name_inv']=='S/C']
inv_SC = inv_SC[['Stkcd','ym','ret','mkt']]
inv_SC['weight'] = inv_SC['mkt']*inv_SC['ret']

#%%
#--------------------------calculate Ri-----------------------#


for i in range(len(Ri)):
    Ri.loc[i, 'hml_BH'] = hml_BH[hml_BH['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'hml_BM'] = hml_BM[hml_BM['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'hml_BL'] = hml_BL[hml_BL['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'hml_SH'] = hml_SH[hml_SH['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'hml_SM'] = hml_SM[hml_SM['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'hml_SL'] = hml_SL[hml_SL['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'op_BH'] = op_BH[op_BH['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'op_BM'] = op_BM[op_BM['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'op_BL'] = op_BL[op_BL['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'op_SH'] = op_SH[op_SH['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'op_SM'] = op_SM[op_SM['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'op_SL'] = op_SL[op_SL['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'op_SH'] = op_SH[op_SH['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'inv_BN'] = inv_BN[inv_BN['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'inv_BA'] = inv_BA[inv_BA['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'inv_BC'] = inv_BC[inv_BC['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'inv_SN'] = inv_SN[inv_SN['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'inv_SA'] = inv_SA[inv_SA['ym'] == Ri.loc[i,'ym']]['weight'].mean()
    Ri.loc[i, 'inv_SC'] = inv_SC[inv_SC['ym'] == Ri.loc[i,'ym']]['weight'].mean()

#%%
Ri = Ri.dropna()
Ri.to_csv('/Users/osx/Downloads/factors.csv')


