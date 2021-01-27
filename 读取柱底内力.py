import re
import os

#当前需要生成的计算结果文件
fileList=["J1","J2"]
#fileList=["J1"]
#生成目标文件
resutlPath='柱底内力\Resut.txt'
resultFile=open(resutlPath,"w")

#遍历工作文件夹下的计算结果文件
for fileItem in fileList:
    filePath=".\柱底内力\%s.out" %fileItem
    #打开计算结果文件
    file=open(filePath,"r")
    fileContent=file.readlines()

    writeTag=False
    startLineID=0
    #读取计算结果文件
    for lineID, lineItem in  enumerate(fileContent):
        #定位荷载组合
        if lineItem.find("五、各组合设计内力")>=0:
            writeTag=True
            startLineID=lineID
        if lineItem.find("六、各组合分项系数")>=0:
            writeTag=False
        if writeTag and lineID>=startLineID+3:
            #print("ss")
            #通过正则提取组合内力
            lineList=re.findall(r"-?\d+\.?\d*", lineItem)
            print(lineList)
            print(lineID,startLineID)
            print('*'*30)
            #将内力写入txt文档
            if len(lineList)>5:
                resultFile.write(lineList[0]+" "+lineList[6]+" "+lineList[4]+
                                 " "+lineList[5]+" "+lineList[2]+" "+lineList[3]+"\n")
            #print(lineList)
    file.close()
resultFile.close()