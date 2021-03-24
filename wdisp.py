'''
    Descroption:提取盈建科后处理中Wdisp.out数据
    Author:hah007
    Prompt:code in python3.7 env
'''
import xlsxwriter
import time
import re
import pandas as pd
import matplotlib.pyplot as plt
from icecream import ic
import pretty_errors
plt.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams['font.serif'] = ['KaiTi']
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)
#提供抓取数据的文件名及路径
f_name = "wdisp.out"


def get_all_info():
    # 读取文件并回传
    f = open(f_name, "r", encoding="gbk")
    return f.read()


def get_block_info(pattern_mode):
    # 根据条件查找文件中内容并回传
    pattern = re.compile(pattern_mode, re.M | re.S)
    info = pattern.findall(get_all_info())
    return info


def convert_to_float(frac_str):
    #转换分数或者其他数值为浮点数
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac


def drawing(filename, data):
    file_png = "%s.png" % filename
    file_excel = "%s.xls" % filename
    data.to_excel(file_excel, sheet_name='sheet1')
    plt.figure(figsize=(5, 6), dpi=150)
    plt.title(filename)
    plt.xlabel('位移角')
    plt.ylabel('楼层')
    plt.plot([0.001, 0.001], [1, 31], label='位移角限值')
    plt.plot(data['位移角'], data['楼层'], label='层位移角')
    x = (0.0002, 0.0005, 0.00067, 0.001, 0.00125)
    x_lable = ('1/5000', '1/2000', '1/1500', '1/1000', '1/800')
    # y=(0,5,10,15,20,25,30,35)
    plt.xticks(x, x_lable)
    # plt.yticks(y)
    plt.legend()
    plt.savefig(file_png)
    plt.show()
    return


def drawing2(filename, data):
    file_png = "%s.png" % filename
    file_excel = "%s.xls" % filename
    data.to_excel(file_excel, sheet_name='sheet1')
    plt.figure(figsize=(5, 6), dpi=150)
    plt.title(filename)
    plt.xlabel('位移比')
    plt.ylabel('楼层')
    plt.plot([1.4, 1.4], [1, 31], label='位移比限值1')
    plt.plot([1.5, 1.5], [1, 31], label='位移比限值2')
    # 需要优化楼层信息
    plt.plot(data['层位移比'], data['楼层'], label='层位移比')
    plt.plot(data['层间位移比'], data['楼层'], label='层间位移比')
    x = (1.0, 1.2, 1.4, 1.5, 1.6)
    plt.xticks(x)
    plt.legend()
    plt.savefig(file_png)
    plt.show()
    return


def get_X_Equivalent_Disp_info(filename, pattern_mode):
    X_E_Dispangle = []
    X_E_Dispangle_f = []
    floor = []
    info = get_block_info(pattern_mode)
    # print(info)
    g = open("%s.txt" % filename, "w", encoding="utf-8")
    g.write(info[0])
    g = open("%s.txt" % filename, "r", encoding="utf-8")
    lines = g.readlines()
    # print(lines)
    # print("&&&&&&"*5)
    lines = lines[2:]
    lines = lines[:-2]
    del lines[2]
    for i in range(len(lines)):
        tt = lines[i]
        if i > 1:
            if i % 2 == 1:
                stringtemp = tt[49:55]
                nostringtemp = ''.join(stringtemp.split())
                X_E_Dispangle_f.append(nostringtemp)
                # print(stringtemp)
                nostringtemp = convert_to_float(stringtemp)
                X_E_Dispangle.append(nostringtemp)
            else:
                stringtemp1 = tt[0:5]
                nostringtemp = ''.join(stringtemp1.split())
                # nostringtemp=convert_to_float(nostringtemp)
                floor.append(nostringtemp)
    pd1 = pd.DataFrame(floor, columns=['楼层'])
    pd1 = pd.to_numeric(pd1['楼层'])
    pd2 = pd.DataFrame(X_E_Dispangle, columns=['位移角'])
    pd21 = pd.DataFrame(X_E_Dispangle_f, columns=['分数位移角'])
    pd3 = pd.concat([pd1, pd2, pd21], axis=1)
    ic(pd3)
    drawing(filename, pd3)
    # print('***'*20)
    # print(pd3.dtypes)
    # pd3['楼层']=pd3['楼层'].astype('int64')
    # print(pd3.info())
    # print('123'*5)
    # print(pd3)
    # pd3['位移角'].plot.line(subplots=True)
    # plt.show()
    # time.sleep(1)
    # filepath="%s.xls" %filename
    # pd3.to_excel(filepath,sheet_name='sheet1')

    g = open("%s.txt" % filename, "w", encoding="utf-8")
    for i in lines:
        g.write(i + "\n")
    g.close()
    return filename


def get_X_Wind_Disp_info(filename, pattern_mode):
    X_W_Dispangle = []
    X_W_Dispangle_f = []
    floor = []
    info = get_block_info(pattern_mode)
    # print(info[0])
    g = open("%s.txt" % filename, "w", encoding="utf-8")
    g.writelines(info[0])
    g = open("%s.txt" % filename, "r", encoding="utf-8")
    lines = g.readlines()
    # print("&&&&&&"*5)
    # print(lines)
    # print("&&&&&&"*5)
    lines = lines[5:]
    lines = lines[:-2]
    # print(lines)
    # del lines[2]
    for i in range(len(lines)):
        tt = lines[i]
        if i >= 0:
            if i % 2 == 1:
                stringtemp = tt[55:67]
                nostringtemp = ''.join(stringtemp.split())
                X_W_Dispangle_f.append(nostringtemp)
                nostringtemp = convert_to_float(stringtemp)
                X_W_Dispangle.append(nostringtemp)
            else:
                stringtemp1 = tt[0:5]
                nostringtemp = ''.join(stringtemp1.split())
                # nostringtemp=convert_to_float(nostringtemp)
                floor.append(nostringtemp)
    pd1 = pd.DataFrame(floor, columns=['楼层'])
    pd1 = pd.to_numeric(pd1['楼层'])
    pd21 = pd.DataFrame(X_W_Dispangle, columns=['位移角'])
    pd22 = pd.DataFrame(X_W_Dispangle_f, columns=['分数位移角'])
    pd3 = pd.concat([pd1, pd21, pd22], axis=1)
    ic(pd3)
    # print('***'*20)
    # print(pd3.dtypes)
    drawing(filename, pd3)

    g = open("%s.txt" % filename, "w", encoding="utf-8")
    for i in lines:
        g.write(i + "\n")
    g.close()
    return filename


def get_Equivalent_DispRatio_info(filename, pattern_mode):
    X_DispRatio = []
    X_DispRatio_f = []
    floor = []
    info = get_block_info(pattern_mode)
    # print(info[0])
    g = open("%s.txt" % filename, "w", encoding="utf-8")
    g.writelines(info[0])
    g = open("%s.txt" % filename, "r", encoding="utf-8")
    lines = g.readlines()
    lines = lines[2:]
    lines = lines[:-2]
    del lines[2]
    # ic(lines)
    for i in range(len(lines)):
        tt = lines[i]
        if i > 1:
            if i % 2 == 1:
                stringtemp = tt[49:55]
                nostringtemp = ''.join(stringtemp.split())
                nostringtemp = convert_to_float(nostringtemp)
                X_DispRatio_f.append(nostringtemp)
                # print(stringtemp)
            else:
                stringtemp1 = tt[0:5]
                nostringtemp = ''.join(stringtemp1.split())
                floor.append(nostringtemp)
                stringtemp = tt[49:55]
                nostringtemp = ''.join(stringtemp.split())
                nostringtemp = convert_to_float(nostringtemp)
                # ic(nostringtemp)
                # print('***'*20)
                X_DispRatio.append(nostringtemp)

    pd1 = pd.DataFrame(floor, columns=['楼层'])
    pd1 = pd.to_numeric(pd1['楼层'])
    pd21 = pd.DataFrame(X_DispRatio, columns=['层位移比'])
    pd22 = pd.DataFrame(X_DispRatio_f, columns=['层间位移比'])
    pd3 = pd.concat([pd1, pd21, pd22], axis=1)
    ic(pd3)
    print('***' * 20)
    print(pd3.dtypes)
    drawing2(filename, pd3)

    return filename


if __name__ == '__main__':
    # 位移角获取
    # get_X_Equivalent_Disp_info("X方向地震作用下的楼层最大位移","X 方向地震作用下的楼层最大位移(.*?)X向最大层间位移角")
    # get_X_Equivalent_Disp_info("Y方向地震作用下的楼层最大位移","Y 方向地震作用下的楼层最大位移(.*?)Y向最大层间位移角")
    # get_X_Wind_Disp_info("+X方向风荷载作用下的楼层最大位移","(\+)X 方向风荷载作用下的楼层最大位移(.*?)X向最大层间位移角")
    # get_X_Wind_Disp_info("-X方向风荷载作用下的楼层最大位移","(\-)X 方向风荷载作用下的楼层最大位移(.*?)X向最大层间位移角")
    # get_X_Wind_Disp_info("+Y方向风荷载作用下的楼层最大位移","(\+)Y 方向风荷载作用下的楼层最大位移(.*?)Y向最大层间位移角")
    # get_X_Wind_Disp_info("-Y方向风荷载作用下的楼层最大位移","(\-)Y 方向风荷载作用下的楼层最大位移(.*?)Y向最大层间位移角")

    # 位移比获取
    # get_Equivalent_DispRatio_info("X方向规定水平力作用下的楼层最大位移比","X 方向规定水平力作用下的楼层最大位移(.*?)X方向最大位移与层平均位移的比值")
    # get_Equivalent_DispRatio_info("X+方向规定水平力作用下的楼层最大位移比","X(\+) 偶然偏心规定水平力作用下的楼层最大位移(.*?)X方向最大位移与层平均位移的比值")
    # get_Equivalent_DispRatio_info("X-方向规定水平力作用下的楼层最大位移比","X(\-) 偶然偏心规定水平力作用下的楼层最大位移(.*?)X方向最大位移与层平均位移的比值")
    # get_Equivalent_DispRatio_info("Y方向规定水平力作用下的楼层最大位移比","Y 方向规定水平力作用下的楼层最大位移(.*?)Y方向最大位移与层平均位移的比值")
    get_Equivalent_DispRatio_info(
        "Y+方向规定水平力作用下的楼层最大位移比",
        "Y(\+) 偶然偏心规定水平力作用下的楼层最大位移(.*?)Y方向最大位移与层平均位移的比值")
    # get_Equivalent_DispRatio_info("Y-方向规定水平力作用下的楼层最大位移比","Y(\-) 偶然偏心规定水平力作用下的楼层最大位移(.*?)Y方向最大位移与层平均位移的比值")

    # data_into_xls("X方向地震作用下的楼层最大位移",get_X_Equivalent_Disp_info("disp_1","X 方向地震作用下的楼层最大位移(.*?)X向最大层间位移角"))
    # data_into_xls("Y方向地震作用下的楼层最大位移",get_X_Equivalent_Disp_info("disp_2","Y 方向地震作用下的楼层最大位移(.*?)Y向最大层间位移角"))
    # data_into_xls("+X方向风荷载作用下的楼层最大位移",get_X_Wind_Disp_info("disp_31","(\+)X 方向风荷载作用下的楼层最大位移(.*?)X向最大层间位移角"))
    # data_into_xls("-X方向风荷载作用下的楼层最大位移",get_X_Wind_Disp_info("disp_32","(\-)X 方向风荷载作用下的楼层最大位移(.*?)X向最大层间位移角"))
    # data_into_xls("+Y方向风荷载作用下的楼层最大位移",get_X_Wind_Disp_info("disp_33","(\+)Y 方向风荷载作用下的楼层最大位移(.*?)Y向最大层间位移角"))
    # data_into_xls("-Y方向风荷载作用下的楼层最大位移",get_X_Wind_Disp_info("disp_33","(\+)Y 方向风荷载作用下的楼层最大位移(.*?)Y向最大层间位移角"))
