#-*- coding: utf-8 -*- 
import numpy as np
import re
import linecache
import pandas as pd

#---------------------------------------------------------------------------
#分割文本
def fileParse(inputfile):
    fp = open(inputfile, 'r',encoding='utf-8')
 
    number =[]
    lineNumber = 1
    keyword = '地震波各时刻'              ##输入你要切分的关键字
    outfilename = 'user_out'     ##输出文件名，如out.txt则写out即可，后续输出的文件是out0.txt,out1.txt...
    outfilepath_list=[]
 
    for eachLine in fp:        
        m = re.search(keyword, eachLine) ##查询关键字
        # print (eachLine)
        if m is not None:
            number.append(lineNumber) #将关键字的行号记录在number中
            print (number)
        lineNumber = lineNumber + 1
    number.append(2*number[-1]-number[-2])
    size = int(len(number))
    for i in range(0,size-1):
        start = number[i]
        end = number[i+1]
        destLines = linecache.getlines(inputfile)[start-1:end-2] #将行号为start-2到end-1的文件内容截取出来
        outpath=outfilename + str(i)+'.txt'
        fp_w = open(outpath,'w') #将截取出的内容保存在输出文件中
        outfilepath_list.append(outpath)
        for key in destLines:
            fp_w.write(key)
        fp_w.close()
    
    return outfilepath_list

#---------------------------------------------------------------------------
#从文本中获取数据并分别输出到文件
def Getdata(path):
    # data_list=[]
    # i=0
    # for file_url in file_list:
    # data = np.loadtxt(path,skiprows=10,encoding='gb2312')
    file_input=open(path,'r')
    file_test=open('test.out','w')
    datalist_disp=[]
    datalist_force=[]

    for eachline in file_input:
        linelist=eachline.split()
        # file_test.write(str(linelist))
        if len(linelist)!=0 and len(linelist)!=4: 
            if linelist[0].isdigit():
                if '/' in linelist[5]:
                    datalist_disp.append(linelist)
                else:
                    datalist_force.append(linelist)
    floor_number=int(len(datalist_disp)/4)
    # print(len(datalist_force))
    # for i in datalist_force:
        # file_test.write(str(datalist_force))
    
    #位移和内力数据分别分方向存储为列表
    displist_x1,displist_x2,displist_y1,displist_y2=datalist_disp[0:floor_number],datalist_disp[floor_number:2*floor_number],datalist_disp[2*floor_number:3*floor_number],datalist_disp[3*floor_number:4*floor_number+1]
    forlist_x1,forlist_x2,forlist_y1,forlist_y2=datalist_force[0:floor_number],datalist_force[floor_number:2*floor_number],datalist_force[2*floor_number:3*floor_number],datalist_force[3*floor_number:4*floor_number+1]
    
    #结果文件数组初始化
    array_x1_dis1=np.zeros(floor_number)
    array_x1_dis2=np.zeros(floor_number)
    array_y1_dis1=np.zeros(floor_number)
    array_y1_dis2=np.zeros(floor_number)
    array_x1_for1=np.zeros(floor_number)
    array_x1_for2=np.zeros(floor_number)
    array_y1_for1=np.zeros(floor_number)
    array_y1_for2=np.zeros(floor_number)
    output_list=[array_x1_dis1,array_y1_dis1,array_x1_dis2,array_y1_dis2,array_x1_for1,array_y1_for1,array_x1_for2,array_y1_for2]

    for i,val in enumerate(displist_x1):
        array_x1_dis1[i]=(val[3])
        array_x1_dis2[i]=(eval(val[5]))
    for i,val in enumerate(displist_y1):
        array_y1_dis1[i]=(val[3])
        array_y1_dis2[i]=(eval(val[5]))
        
    for i,val in enumerate(forlist_x1):
        # print(val)
        array_x1_for1[i]=(val[2])
        array_x1_for2[i]=(eval(val[4]))
    for i,val in enumerate(forlist_y1):
        array_y1_for1[i]=(val[2])
        array_y1_for2[i]=(eval(val[4]))
    
    #创建或打开文本文件
    # file_x1_dis1=open(path[0:-4]+'.x1dis1','w')
    # file_x1_dis2=open(path[0:-4]+'.x1dis2','w')
    # file_y1_dis1=open(path[0:-4]+'.y1dis1','w')
    # file_y1_dis2=open(path[0:-4]+'.y1dis2','w')

    # file_x1_for1=open(path[0:-4]+'.x1for1','w')
    # file_x1_for2=open(path[0:-4]+'.x1for2','w')     
    # file_y1_for1=open(path[0:-4]+'.y1for1','w')
    # file_y1_for2=open(path[0:-4]+'.y1for2','w') 

    #输出到文本文件
    # for i in displist_x1:
        # file_x1_dis1.write(i[3]+'\n')
        # file_x1_dis2.write(str(eval(i[5]))+'\n')
    # for i in displist_y1:
        # file_y1_dis1.write(i[3]+'\n')
        # file_y1_dis2.write(str(eval(i[5]))+'\n')
        
    # for i in forlist_x1:
        # file_x1_for1.write(i[2]+'\n')
        # file_x1_for2.write(str(eval(i[4]))+'\n')
    # for i in forlist_y1:
        # file_y1_for1.write(i[2]+'\n')
        # file_y1_for2.write(str(eval(i[4]))+'\n')
        
    #仅供测试
    # file_x2_dis1=open(path[0:-4]+'.x2dis1','w')
    # for i in displist_x2:
        # file_x2_dis1.write(i[3]+'\n')   
    # file_y2_dis1=open(path[0:-4]+'.y2dis1','w')
    # for i in displist_y2:
        # file_y2_dis1.write(i[3]+'\n')    
            
    return output_list
         

def ToExcel(datalist,ExcelName='pkpm_output.xlsx',SheetName='计算结果'):
    
    writer = pd.ExcelWriter(ExcelName)
    # x = np.array([x]).T
    # y = np.array([y]).T
    
    for i ,j in enumerate(datalist):
        data_col = pd.DataFrame(j)
    
        # # change the index and column name
        # data_df.columns = ['A','B','C','D','E','F','G','H','I','J']
        # data_df.index = ['a','b','c','d','e','f','g','h','i','j']
        # ExcelName='Save_Excel.xlsx'
    
        data_col.to_excel(writer,SheetName,float_format='%.8f', columns=None, header=False, index=False, startrow=0, startcol=i, engine='xlsxwriter', merge_cells=True, encoding=None, inf_rep='inf', verbose=True) # float_format 控制精度

        
# ###########################################################################
if __name__ == "__main__":
    result=[]
    x_dis1=[]
    y_dis1=[]
    x_dis2=[]
    y_dis2=[]
    x_for1=[]
    y_for1=[]
    x_for2=[]
    y_for2=[]
    excel_data=[x_dis1,y_dis1,x_dis2,y_dis2,x_for1,y_for1,x_for2,y_for2]    
    originfile='WDYNA.OUT'
    inputfile_list=fileParse(originfile)
    for i,j in enumerate(inputfile_list):
        result.append(Getdata(j))
        x_dis1.append(Getdata(j)[0])
        y_dis1.append(Getdata(j)[1])
        x_dis2.append(Getdata(j)[2])
        y_dis2.append(Getdata(j)[3])
        x_for1.append(Getdata(j)[4])
        y_for1.append(Getdata(j)[5])
        x_for2.append(Getdata(j)[6])
        y_for2.append(Getdata(j)[7])
    for i,j in enumerate(excel_data):
        ToExcel(j,'pkpm_output%s.xlsx'%i)
    for i,j in enumerate(result):
        print("地震波%s基底剪力:x方向%s  y方向%s"%(i,j[4].max(),j[5].max()))