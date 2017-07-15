import easygui as g
import numpy as np
import sys

"""
@Toolname: Channel Number\Frequency convert to each other
@Version: v0.5
@Author: apstusb
@Mail: apstusb@163.com
######################分割线##########################
#E-UTRA频点转频率计算公式
FDL = FDL_low + 0.1*(NDL – NOffs-DL)
FUL = FUL_low + 0.1*(NUL – NOffs-UL)

#E-UTRA频率转频点计算公式
NDL = 10*（FDL - FDL_low） + NOffs-DL
NUL = 10*（FUL - FUL_low） + NOffs-UL

#NB-IOT频率转频点计算公式
FDL = FDL_low + 0.1*(NDL – NOffs-DL) + 0.0025*(2MDL+1)
FUL = FUL_low + 0.1*(NUL – NOffs-UL) + 0.0025*(2MUL)

"""
#LTE中心频点字典
#every row stand for: band:Fdl_low[Mhz],Noffs-DL,Range of Ndl,Ful_low[Mhz],Noffs-UL,Range of Nul.(3GPP 36141v14)  
EARFCN = {
    1:[2110,0,range(600),1920,18000,range(18000,18600)],
    2:[1930,600,range(600,1200),1850,18600,range(18600,19200)],  
    3:[1805,1200,range(1200,1950),1710,19200,range(19200,19950)],  
    4:[2110,1950,range(1950,2400),1710,19950,range(19950,20400)],  
    5:[869,2400,range(2400,2650),824,20400,range(20400,20650)],  
    6:[875,2650,range(2650,2750),830,20650,range(20650,20750)],  
    7:[2620,2750,range(2750,3450),2500,20750,range(20750,21450)],  
    8:[925,3450,range(3450,3800),880,21450,range(21450,21800)],  
    9:[1844.9,3800,range(3800,4150),1749.9,21800,range(21800,22150)],  
    10:[2110,4150,range(4150,4750),1710,22150,range(22150,22750)],  
    11:[1475.9,4750,range(4750,4950),1427.9,22750,range(22750,22950)],  
    12:[729,5010,range(5010,5180),699,23010,range(23010,23180)],  
    13:[746,5180,range(5180,5280),777,23180,range(23180,23280)],  
    14:[758,5280,range(5280,5380),788,23280,range(23280,23380)],
    17:[734,5730,range(5730,5850),704,23730,range(23730,23850)],  
    18:[860,5850,range(5850,6000),815,23850,range(23850,24000)],  
    19:[875,6000,range(6000,6150),830,24000,range(24000,24150)],  
    20:[791,6150,range(6150,6450),832,24150,range(24150,24450)],  
    21:[1495.9,6450,range(6450,6600),1447.9,24450,range(24450,24600)],  
    22:[3510,6600,range(6600,7400),3410,24600,range(24600,25400)],  
    23:[2180,7500,range(7500,7700),2000,25500,range(25500,25700)],  
    24:[1525,7700,range(7700,8040),1626.5,25700,range(25700,26040)],  
    25:[1930,8040,range(8040,8690),1850,26040,range(26040,26690)],  
    26:[859,8690,range(8690,9040),814,26690,range(26690,27040)],  
    27:[852,9040,range(9040,9209),807,27040,range(27040,27210)],  
    28:[758,9210,range(9210,9660),703,27210,range(27210,27660)],
    30:[2350,9770,range(9770,9870),2305,27660,range(27660,27760)],
    31:[462.5,9870,range(9870,9920),452.5,27760,range(27760,27810)],
    33:[1900,36000,range(36000,36200),1900,36000,range(36000,36200)],  
    34:[2010,36200,range(36200,36350),2010,36200,range(36200,36350)],  
    35:[1850,36350,range(36350,36950),1850,36350,range(36350,36950)],  
    36:[1930,36950,range(36950,37550),1930,36950,range(36950,37550)],  
    37:[1910,37550,range(37550,37750),1910,37550,range(37550,37750)],  
    38:[2570,37750,range(37750,38250),2570,37750,range(37750,38250)],  
    39:[1880,38250,range(38250,38650),1880,38250,range(38250,38650)],  
    40:[2300,38650,range(38650,39650),2300,38650,range(38650,39650)],  
    41:[2496,39650,range(39650,41590),2496,39650,range(39650,41590)],  
    42:[3400,41590,range(41590,43590),3400,41590,range(41590,43590)],  
    43:[3600,43590,range(43590,45590),3600,43590,range(43590,45590)],  
    44:[703,45590,range(45590,46590),703,45590,range(45590,46590)],
    47:[215,60000,range(60000,60401),215,60000,range(60000,60401)],
    48:[430,57240,range(57240,57440),430,57240,range(57240,57440)],
    49:[1755,57440,range(57440,57740),1755,57440,range(57440,57740)],
    52:[2170,57900,range(57900,58200),1980,57600,range(57600,57900)],
    53:[778,64000,range(64000,64200),778,64000,range(64000,64200)],
    54:[450,59780,range(59780,59980),450,59780,range(59780,59980)],
    55:[5850,64600,range(64600,65000),5850,64600,range(64600,65000)],
    56:[336,65400,range(65400,65480),336,65400,range(65400,65480)],
    57:[3300,58700,range(58700,59000),3300,58700,range(58700,59000)],
    58:[380,58200,range(58200,58700),380,58200,range(58200,58700)],
    59:[610,62100,range(62100,64000),610,62100,range(62100,64000)],
    60:[710,61100,range(61100,62000),610,60100,range(60100,61000)],
    61:[1447,65000,range(65000,65200),1447,65000,range(65000,65200)],
    62:[1785,65200,range(65200,65400),1785,65200,range(65200,65400)],
    63:[526,58260,range(58260,59780),526,58260,range(58260,59780)],
    64:[558,64200,range(64200,64600),558,64200,range(64200,64600)]
    }

Band_list = []
for key in EARFCN.keys():
    Band_list.append(key)

D = [] #存放下行频率
U = [] #存放上行频率

def number_freq_downlink(Band):
    #下行频点范围
    #for N in EARFCN[Band][2]:
        #NFD.append(N)
    NFD = list(EARFCN[Band][2])
    return NFD

def number_freq_uplink(Band):
    #上行频点范围
    #for N in EARFCN[Band][5]:
        #NFU.append(N)
    NFU = list(EARFCN[Band][5])
    return NFU

def down_freq(Band):
    #下行频率范围
    DLow=(EARFCN[Band][0]+0.1*(EARFCN[Band][2][0]-EARFCN[Band][1]))
    print("DLow is %s: " % DLow)
    DHigh=(EARFCN[Band][0]+0.1*(EARFCN[Band][2][-1]-EARFCN[Band][1]))
    print("DHigh is: ",DHigh)
    D_array = np.arange(DLow, (DHigh+0.1), 0.1)
    #tolist()函数对array数组对象进行list转换会出现精度问题
    #np.arange生成的数组对象进行精度处理
    for d in D_array:
        d = round(float(d),1)
        D.append(d)
    return D
    #print(D)

def up_freq(Band):
    #上行频率范围
    ULow=(EARFCN[Band][3]+0.1*(EARFCN[Band][5][0]-EARFCN[Band][4]))
    print("ULow is: ",ULow)
    UHigh=(EARFCN[Band][3]+0.1*(EARFCN[Band][5][-1]-EARFCN[Band][4]))
    print("UHigh is: ",UHigh)
    U_array =np.arange(ULow, (UHigh+0.1), 0.1)
    #tolist()函数对array数组对象进行list转换会出现精度问题
    #np.arange生成的数组对象进行精度处理
    for u in U_array:
        u = round(float(u),1)
        U.append(u)
    return U

#Frequency convert to NumberFrequency
def frequency_to_numfreq(Band,F):
    
    if Band in Band_list:
        
        #需转换的频率在下行范围内
        if F in D:
            NDL = 10*(F - EARFCN[Band][0]) + EARFCN[Band][1]
            return NDL
        #需转换的频率在上行范围内
        if F in U:
            NUL = 10*(F - EARFCN[Band][3]) + EARFCN[Band][4]
            return NUL

#NumberFrequency convert to Frequency
def numfreq_to_frequency(Band,N):
    if Band in Band_list:
        if N in EARFCN[Band][2]:
            FDL = EARFCN[Band][0] + 0.1*(N - EARFCN[Band][1])
            return float(FDL)
        
        if N in EARFCN[Band][5]:
            FUL = EARFCN[Band][3] + 0.1*(N - EARFCN[Band][4])
            return float(FUL)

    
def main():
    FNNF = g.buttonbox("请选择转换方式", 'EARFCN', choices=('F2N','N2F'))

    while True: #使用while循环方便多次查询
        if FNNF == 'F2N':
		    #进行频率到频点的转换
            F2N = g.multenterbox('请输入各项参数','Frequency convert',('Bandnum(例 38)',
                                                                'Frequency(例 2595.0)'))
            #Band为空时提示用户输入
            if F2N[0] == '':
                g.msgbox('Please input Bandnum(例 38)!',ok_button='ok')
                continue
            
            #频率为空时提示用户输入
            if F2N[1]=='':
                g.msgbox('Please input Frequency(例 2595.0)!',ok_button='ok')
                continue
            Band=int(F2N[0])  #输入不为空时执行
            F=float((F2N[1]))  #输入不为空时执行
            
            if Band in Band_list:
                D=down_freq(Band)#调用下行频点函数
                U=up_freq(Band)#调用上行频点函数
                DU = D + U
                if float(F2N[1]) not in DU:
                    g.msgbox('The frequency is out of range. Please re-enter!(例 2595.0)',ok_button='ok')
                    continue                 
            else:
                g.msgbox('Bandnum is out of range. Please re-enter!(例 38)',ok_button='ok')
                continue
            
            N=frequency_to_numfreq(Band,F) #调用F2N转换函数

            g.msgbox('NumberFrequency ' + str(N)) #提示用户转换结果
            
        if FNNF == 'N2F':
		    #进行频点到频率的转换
            N2F = g.multenterbox('请输入各项参数','Frequency convert',('Bandnum(例 38)','Numfreq(例 38000)'))
            if N2F[0]=='':
                g.msgbox('Please input Bandnum(例 38)!',ok_button='ok')
                continue
            if N2F[1]=='':
                g.msgbox('Please input Numfreq(例 38000)!',ok_button='ok')
                continue
 
            if int(N2F[0]) in Band_list:
                Band=int(N2F[0])
                NFD=number_freq_downlink(Band)
                NFU=number_freq_uplink(Band)
                NF=NFD+NFU
                if int(N2F[1]) not in NF:
                    print('yes','EARFCN[Band][2]:',EARFCN[Band][2],'EARFCN[Band][5]',EARFCN[Band][2])
                    g.msgbox('The Numfreq is out of range. Please re-enter!(例 2595.0)',ok_button='ok')
                    continue
                else:
                    N = int(N2F[1])
            else:
                g.msgbox('Bandnum is out of range. Please re-enter!(例 2595.0)',ok_button='ok')
                continue
            
            F=numfreq_to_frequency(Band,N)

            g.msgbox('NumberFrequency ' + str(F))
    
main()

