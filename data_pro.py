#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Yihao Wu
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

'''文件读取与数据处理'''
data = pd.read_csv('./600004.SH.CSV',encoding='gbk')
save_column = ['代码','简称','日期','开盘价(元)','收盘价(元)','成交金额(元)']
save_data = data.loc[:,save_column]
save_data.dropna(axis=0,how='any',inplace=True)    #删除含空值的行
# save_data.to_csv('./Result1.csv',encoding='utf_8_sig')   #just for test
save_data.index = pd.to_datetime(save_data.日期)      #将日期格式转化为datetime类型并作为标签

'''按代码、简称，月份，平均开盘价，平均收盘价，总成交金额存储数据并保存到Result.csv文件中'''
new_stock = save_data.loc[:,['开盘价(元)','收盘价(元)']].resample('M').apply(np.mean)
new_stock['总成交金额(元)'] = save_data.loc[:,'成交金额(元)'].resample('M').apply(np.sum)
new_stock.rename(columns={'开盘价(元)':'平均开盘价(元)','收盘价(元)':'平均收盘价(元)'},inplace=True)
index=list(new_stock.index)
date=[str(i).split('-')[0]+'-'+str(i).split('-')[1] for i in index]   #取日期的年和月
new_stock.insert(0,'代码','600004.SH')
new_stock.insert(1,'简称','白云机场')
new_stock.insert(2,'日期',date)
new_stock.index = range(1,len(new_stock) + 1)    #将index的datetime变为序号
#new_stock.to_csv('./Result.csv',encoding='utf_8_sig')

'''绘制平均开盘价和平均收盘价随月份的变化'''
plt.rcParams['font.sans-serif']=['FangSong']
plt.plot(new_stock.index,new_stock['平均开盘价(元)'], color='red',label='平均开盘价(元)')
plt.plot(new_stock.index,new_stock['平均收盘价(元)'], color='green',label='平均收盘价(元)',alpha=0.8)
plt.xlabel('月份')
plt.ylabel('股价')
plt.xticks(new_stock.index[::10],new_stock['日期'][::10])
plt.xticks(rotation=-45)
plt.legend()
plt.savefig('平均开盘价和平均收盘价随月份的变化.png', dpi=300)
plt.show()

'''双Y轴绘制平均开盘价和平均收盘价随月份的变化'''
fig = plt.figure()
ax1 = fig.add_subplot(111)
lns1 = ax1.plot(new_stock.index,new_stock['平均开盘价(元)'])
ax1.set_ylabel('Y values for 平均开盘价(元)')
ax1.set_title("平均开盘价和平均收盘价随月份的变化")
ax1.set_ylim([3,22])
ax2 = ax1.twinx()  # this is the important function
lns2 = ax2.plot(new_stock.index,new_stock['平均收盘价(元)'], 'r')
ax2.set_ylim([2,21])
ax2.set_ylabel('Y values for 平均收盘价(元)')
ax2.set_xlabel('月份 ')
plt.xticks(new_stock.index[::18],new_stock['日期'][::18])
lns = lns1 +lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns,labs,loc=0)
plt.xticks(rotation=-45)
plt.savefig('双Y轴绘制曲线图.png', dpi=300)
plt.show()

'''检验总成交额是否服从正态分布,显著性水平设为0.001'''
[statics,pvalue]=stats.normaltest(new_stock['总成交金额(元)'])
if pvalue>0.001:
    print( 'p值为{}，高于显著性水平(0.001),总成交金额（元）服从正态分布'.format(pvalue))
else:
    print('p值为{}，低于显著性水平(0.001),总成交金额（元）不服从正态分布'.format(pvalue))
new_stock['总成交金额(元)'].plot(kind="hist",bins=50)
plt.savefig('假设检验.png', dpi=300)
plt.show()