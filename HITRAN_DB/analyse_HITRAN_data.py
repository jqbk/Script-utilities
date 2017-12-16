# -*- coding:utf-8 -*-

import json
from hapi import *
import matplotlib.pyplot as plt

path = 'E:\\Software-Docs\\Matlab_docs\\HITRAN_data\\'
db_begin(path)

fetch('H2O', 1, 1, 7290, 7300)
# 利用福伊特线型计算吸收系数并作图
nu1, coef1 = absorptionCoefficient_Voigt([(1,1,)], 'H2O', \
           Environment={'p':1,'T':296.}, OmegaStep=0.01, GammaL='gamma_self', HITRAN_units=False) # False表示纵轴单位为cm-1
nu2, coef2 = absorptionCoefficient_Voigt([(1,1,)], 'H2O', \
           Environment={'p':1,'T':500.}, OmegaStep=0.01, GammaL='gamma_self', HITRAN_units=False)
nu3, coef3 = absorptionCoefficient_Voigt([(1,1,)], 'H2O', \
           Environment={'p':1,'T':1000.}, OmegaStep=0.01, GammaL='gamma_self', HITRAN_units=False)

plt.figure('吸收系数—波数', figsize=(12,6))
plt.plot(nu1, coef1, 'r', nu2, coef2, 'g', nu3, coef3, 'b')
plt.title('吸收系数')
plt.legend(['296K','500K','1000K'], loc='upper left')
plt.show()

# 计算吸收光谱并作图
nu, absorp = absorptionSpectrum(nu1, coef1, Environment={'l': 1000}) # 吸收长度为l，单位为cm
plt.figure('吸收光谱', figsize=(12,6))
plt.plot(nu, absorp, color='green')
plt.title('吸收光谱')
plt.legend(['H2O',], loc='upper left')
plt.show()