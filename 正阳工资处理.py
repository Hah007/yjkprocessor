'''
    Descroption:提取excel社保数据并进行筛选
    Author:hah007
    Prompt:code in python3.7 env
'''
import pandas as pd

def pros_excel(filename):
    pd_list = pd.read_excel('二分院员工名单.xlsx', sheet_name='Sheet1')
    pd11 = pd.read_excel(filename, sheet_name='Sheet2')
    pd22 = pd11.groupby('姓名', as_index=False)['姓名', '单位应缴金额', '单位应缴划入金额',
                                              '个人应缴金额', '个人应缴划入金额'].sum()
    pd33 = pd22[pd22['姓名'].isin(pd_list['姓名'])]
    print(pd33)
    return


if __name__ == '__main__':
    # file_month为本月社保导出的excel文件
    file_month = '2021.1.12养老汇总.xlsx'
    pros_excel(file_month)
