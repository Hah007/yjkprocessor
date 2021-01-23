'''
Descroption:提取盈建科后处理中Wdisp.out数据
Author:hah007
Prompt:code in python3.7 env
'''
import xlsxwriter
import re
#提供抓取数据的文件名及路径
f_name="wdisp.out"

def get_all_info():
    # 读取文件并回传
    f = open(f_name,"r",encoding="gbk")
    return f.read()
def get_block_info(pattern_mode):
    # 根据条件查找文件中内容并回传
    pattern = re.compile(pattern_mode,re.M|re.S)
    info = pattern.findall(get_all_info())
    return info
def data_into_xls(xls_filename,data_filename):
    # 生成excel文件并写入数据
    workbook = xlsxwriter.Workbook("%s.xlsx"%xls_filename)
    worksheet = workbook.add_worksheet()
    f = open("%s.txt"%data_filename,"r",encoding="utf-8")
    lines = f.readlines()
    print("读取中")
    print(lines)
    lines = [i.strip().split() for i in lines]
    title = lines[0]
    data = lines[1:]
    print(title)
    print(data)
    formatter = workbook.add_format()
    formatter.set_border(1)
    formatter.set_align("center")
    title_formatter = workbook.add_format()
    title_formatter.set_border(1)
    title_formatter.set_bg_color('#cccccc')
    title_formatter.set_align('center')
    title_formatter.set_bold()
    ave_formatter = workbook.add_format()
    ave_formatter.set_border(1)
    ave_formatter.set_align('center')
    ave_formatter.set_num_format('0.00')
    worksheet.write_row('A1',title,title_formatter)
    for i in range(2,len(data)+2):
        worksheet.write_row('A{}'.format(i),data[i-2],formatter)
    workbook.close()
    
def get_X_Equivalent_Disp_info(filename,pattern_mode):
    X_E_Dispangle = []
    floor=[]
    info = get_block_info(pattern_mode)
    g = open("%s.txt"%filename,"w",encoding="utf-8")
    g.write(info[0])
    g = open("%s.txt"%filename,"r",encoding="utf-8")
    lines = g.readlines()
    print(lines)
    print("&&&&&&")
    lines = lines[2:]
    lines = lines[:-2]
    del lines[2]
    # X_E_Dispangle=lines[4:6]
    for i in range(len(lines)):
        tt=lines[i]
        stringtemp1 =tt[0:5]
        nostringtemp = ''.join(stringtemp1.split())
        floor.append(nostringtemp)       
        stringtemp =tt[49:55]
        nostringtemp = ''.join(stringtemp.split())
        X_E_Dispangle.append(nostringtemp)
    print("**********")
    print(floor)
    print("**********")      
    print(X_E_Dispangle)       
    print("**********")
    #     if i>1:
    #         lines = i.strip()

    g = open("%s.txt"%filename,"w",encoding="utf-8")
    for i in lines:
        g.write(i+"\n")
    g.close()
    return filename

import time
if __name__ == '__main__':
    data_into_xls("X方向地震作用下的楼层最大位移",get_X_Equivalent_Disp_info("disp_1","X 方向地震作用下的楼层最大位移(.*?)X向最大层间位移角"))
    # data_into_xls("各层构件数量、构件材料和层高",get_num_compon_mater_heig_info("new_2","各层构件数量、构件材料和层高(.*?)保护层"))
    # data_into_xls("混凝土构件",get_concrte_info("new_3","混凝土构件：(.*?)箍筋（墙分布筋）"))
    # # data_into_xls("型钢混凝土构件",get_Shaped_steel_concrete_info("new_4","型钢混凝土构件：(.*?)箍筋"))
    # data_into_xls("箍筋（墙分布筋）",get_Distribution_strirrup_of_wall_reinforcement_info("new_5","箍筋（墙分布筋）：(.*?) X、Y方向剪力墙截面面积"))
    # data_into_xls("X、Y方向剪力墙截面面积",get_Shear_wall_section_area_info("new_6","X、Y方向剪力墙截面面积(.*?)风荷载信息"))
    # data_into_xls("风荷载信息",get_wind_load_info("new_7","风荷载信息\n(.*?)各楼层等效尺寸"))
    # data_into_xls("各楼层等效尺寸",get_Equivalent_dimensions_of_each_floor_info("new_8","各楼层等效尺寸(.*?)各楼层质量、单位面积质量分"))
    # data_into_xls("各楼层质量、单位面积质量分布",get_Unit_area_mass_distribution_info("new_9","各楼层质量、单位面积质量分布(.*?)计算时间"))
    # # data_into_xls("楼层抗剪承载力验算",get_Floor_shear_bearing_capacity_info("new_10","表示本层与上一层的承载力之比(.*?)+$"))
    # data_into_xls("风荷载作用下剪力平衡验算",get_Calculation_hear_balance_under_wind_load_info("new_11","风荷载作用下剪力平衡验算(.*?)楼层抗剪承载力验算"))
    # data_into_xls("恒、活荷载作用下轴力平衡验算",get_Check_the_axial_force_balance_info("new_12","恒、活荷载作用下轴力平衡验算(.*?)风荷载作用下剪力平衡验算"))
    # data_into_xls("结构抗震验算",get_Structural_seismic_checking_info("new_13","结构抗震验算(.*?)风振舒适度验算"))

















