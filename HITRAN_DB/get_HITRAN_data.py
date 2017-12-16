# -*- coding:utf-8 -*-

# 这是用hapi接口从HITRAN数据库下载数据的脚本

import json
from hapi import *
import matplotlib.pyplot as plt

def get_data():
    path = 'E:\\Software-Docs\\Matlab_docs\\HITRAN_data\\'
    db_begin(path)

    #getHelp(fetch)
    
    # fetch函数从服务器下载数据，selct函数用于筛选通过fetch函数下载的气体吸收线数据
    Cond = ('AND', ('BETWEEN','nu',6800,7420), ('>=','sw',1E-22))
    fetch('H2O', 1, 1, 6800, 7420) # 第一个参数表示抓取的物质名称（保存数据的表名），第二和第三个参数分别表示分子编号和同位素编号,第四和第五个参数表述波数范围
    data = select('H2O', ParameterNames=('nu', 'sw', 'gamma_air', 'gamma_self', 'elower'), Conditions=Cond, File='HITRAN_DB\\data.json') # 选择打印波数、线强(296K)、低跃迁态能量
    
    #TT, PartSum = partitionSum(1,1,[296,1000],step=0.1) # 水的配分函数的计算
    #print(PartSum)
    '''
    plt.figure('test', figsize=(12,6))
    plt.plot(TT, PartSum, color='blue')
    plt.title('test')
    plt.legend(['test',])
    plt.show()
    '''
    plt.figure('波数—线强图', figsize=(12,6))
    x, y = getStickXY('H2O')
    plt.plot(x, y, color='b')
    plt.title('Stick plot for $^{1}H_{2}^{16}O$')
    plt.show()

def data_sorting():
    with open('E:\\Software-Docs\\python_documents\\HITRAN_DB\\data.json', 'r') as f:
        all_data = f.readlines()

    all_data = [all_data[i].split() for i in range(len(all_data))]
    all_data = [[10**7/float(all_data[i][0]), float(all_data[i][1][0:9]), float('0'+all_data[i][1][9:14]), \
                float(all_data[i][1][14:]), float(all_data[i][2])] for i in range(len(all_data))]
    all_data_ls = sorted(all_data, key=lambda all_data: all_data[1], reverse=True) # 按照线强降序排列
    all_data_wl = sorted(all_data, key=lambda all_data: all_data[0]) # 按照波长升序排列
    return all_data_ls, all_data_wl

def save_data(path, all_data):
    with open(path, 'w+') as f:
        f.writelines(['Wavelength\t\t', 'Linestrength\t', '  Gamma_air\t', ' Gamma_self', '   Elower', '\n'])
        for i in range(len(all_data)):
            r0 = '{:>10.6f}'.format(all_data[i][0])
            r1 = '{:>10.6E}'.format(all_data[i][1])
            r2 = '{:>10.6f}'.format(all_data[i][2])
            r3 = '{:>10.6f}'.format(all_data[i][3])
            r4 = '{:>10.6f}'.format(all_data[i][4])
            f.writelines([r0+'\t\t', r1+'\t', r2+'\t', r3+'\t', r4, '\n']) # writelines接收的参数为字符串序列

if __name__ == '__main__':
    all_data_ls, all_data_wl = data_sorting()
    path = 'E:\\Software-Docs\\python_documents\\HITRAN_DB\\'
    get_data()
    save_data(path+'ans_ls.json', all_data_ls)
    save_data(path+'ans_wl.json', all_data_wl)