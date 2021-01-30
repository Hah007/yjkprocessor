import pandas as pd

pd_list=pd.read_excel('二分院员工名单.xlsx',sheet_name='Sheet1')
pd11=pd.read_excel('2021.1.12养老汇总.xlsx',sheet_name='Sheet2')
pd22=pd11.groupby('姓名',as_index = False)['姓名','单位应缴金额','个人应缴金额'].sum()

print(pd_list['姓名'])
pd33=pd.DataFrame(columns=['姓名', '单位应缴金额','个人应缴金额'])
for name in pd_list['姓名']:
    pd33=pd33.append(pd22.loc[pd22['姓名'] ==name, ['姓名', '单位应缴金额','个人应缴金额']])
print(pd33)
pd33.to_excel('筛选结果.xlsx',sheet_name='sheet1')
