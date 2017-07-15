###Version 0.2###
import re
#从原始log中筛选出需要进行统计分析的数据
filepath = 'D:/Python34/Python_Zen/datapro/tracet.log'
filepathww = 'D:/Python34/Python_Zen/datapro/traceww.txt'

with open(filepath,'r', encoding='gbk', errors='ignore') as f:
    for line in f.readlines():
        strl = 'MC: throughput = '
        if strl in line:
            step1 = re.split(r'[\:\,\(]+', line) #第一次筛选
            step2 = re.split(r'[\s\=]+', step1[3]) #第二次筛选
            del step2[0]
            with open(filepathww,'a') as fww:
                fww.write(str(step2)+'\n')
                fww.flush()
                print(step2)

                
            
