# data_processing
全过程的数据分析（股票数据）

### 1. 作业过程

#### 1.1 数据分析

作业提供数据为上证A股的数据，即上海机场的股票数据。数据为CSV文件，包含了2003-4至2016-6股票的基本信息，文件中数据存在空值，每一年的数据不一定覆盖全年12个月。

 

#### 1.2 作业要求

（1）读取数据，在列上仅保留：代码、简称，日期，开盘价(元)，收盘价(元)，成交金额(元)。在行上，删除包含空值的行。

（2）对数据进行汇总，获得每个月（按自然月）的平均开盘价（元）和平均收盘价（元），总成交金额（元）。此时获得数据：代码、简称，月份，平均开盘价，平均收盘价，总成交金额。

（3）绘制图形，横坐标是月份，纵坐标是股价，绘制平均开盘价（元）、平均收盘价（元）随月份的变化（两条曲线）。

（4）取所有月份的总成交金额构成的一组数值，判定这组数值是否符合正态分布，并简述回顾正态分布检验的原理。

### 2.代码说明

#### 2.1  文件读取与数据处理

列上仅保留：代码、简称，日期，开盘价(元)，收盘价(元)，成交金额(元)，在行上，把包含空值的行删除，完成作业要求1：

```javascript
data = pd.read_csv('./600004.SH.CSV',encoding='gbk')
save_column = ['代码','简称','日期','开盘价(元)','收盘价(元)','成交金额(元)']
save_data = data.loc[:,save_column]
save_data.dropna(axis=0,how='any',inplace=True)    #删除含空值的行
# save_data.to_csv('./Result1.csv',encoding='utf_8_sig')   #just for test
save_data.index = pd.to_datetime(save_data.日期)      #将日期格式转化为datetime类型并作为标签
```



#### 2.2  数据汇总与保存

按代码、简称，月份，平均开盘价，平均收盘价，总成交金额存储数据并保存到Result.csv文件中：


```javascript
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
```



#### 2.3  图形绘制

绘制平均开盘价和平均收盘价随月份的变化：

```javascript
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
```
![同一张图上绘制两条曲线](https://img-blog.csdnimg.cn/20200525180503582.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzM1MzYxMg==,size_16,color_FFFFFF,t_70)
由于数值差距不大，发现两曲线已经近似重合，为了使效果更加明显，可以采用双Y轴绘制曲线图，将左Y轴设置为[3,22]，右Y轴设置为[2,21]：
```javascript
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

```
![双Y轴绘制曲线图](https://img-blog.csdnimg.cn/20200525180612560.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzM1MzYxMg==,size_16,color_FFFFFF,t_70)


#### 2.4  判定数值是否符合正态分布
##### 2.4.1 简单回顾正态分布检验的原理
正态分布检验就是判断样本所代表的背景总体与理论正态分布是否没有显著差异的检验，python中常用的检验正态分布的方法有：shapiro方法，normaltest方法，kstest方法，anderson方法。这里检验时采用normaltest方法，原理是基于数据的skewness和kurtosis。利用normaltest函数得到该组数据的 pvalue 值，与显著性水平进行比较，对于是否否定原假设做出比较，然后得出结论。

##### 2.4.2 代码实现
```javascript
[statics,pvalue]=stats.normaltest(new_stock['总成交金额(元)'])
if pvalue>0.001:
    print( 'p值为{}，高于显著性水平(0.001),总成交金额（元）服从正态分布'.format(pvalue))
else:
    print('p值为{}，低于显著性水平(0.001),总成交金额（元）不服从正态分布'.format(pvalue))
new_stock['总成交金额(元)'].plot(kind="hist",bins=50)
plt.savefig('假设检验.png', dpi=300)
plt.show()
```


### 3. 结论与可视化结果

#### 3.1 结论

通过用normaltest方法对所有月份的总成交金额构成的一组数值进行正态分布判断，发现总成交金额（元）不服从正态分布。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200525180802911.png)


#### 3.2 可视化结果
![平均开盘价（元）、平均收盘价（元）随月份的变化](https://img-blog.csdnimg.cn/20200525180823778.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzM1MzYxMg==,size_16,color_FFFFFF,t_70)
![假设检验图](https://img-blog.csdnimg.cn/20200525180902339.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzM1MzYxMg==,size_16,color_FFFFFF,t_70)


### 4. 数据处理中的问题与解决

#### 4.1 保存处理后的csv文件出现乱码

##### 4.1.1 问题

希望随时保存中间处理得到的csv文件确保过程按预期进行，使用以下命令直接保存文件出现乱码，尝试加入encoding="utf_8"后仍乱码：
```javascript
new_stock.to_csv('./Resultluanma.csv')   
```
![出现乱码](https://img-blog.csdnimg.cn/20200525181009652.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzM1MzYxMg==,size_16,color_FFFFFF,t_70)

##### 4.1.2 解决方案

保存时编码方式变为encoding="utf_8_sig"即可：

```javascript
new_stock.to_csv(file_name3,encoding="utf_8_sig")  
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/2020052518113523.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzM1MzYxMg==,size_16,color_FFFFFF,t_70)


#### 4.2 Pandas matplotlib 画图无法显示中文字体的问题

##### 4.2.1 问题

直接绘图时显示的图片，会显示中文为方块，查找解决方案时发现Pandas在绘图时,会显示中文为方块,主要原因有二: matplotlib
字体问题；seaborn 字体问题。

![汉字显示为方块](https://img-blog.csdnimg.cn/20200525181210771.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzM1MzYxMg==,size_16,color_FFFFFF,t_70)
##### 4.2.2 解决方案（一）
matplotlib动态修改配置(推荐)

```javascript

import matplotlib as mpl         
mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi'] 
# mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题,或者转换负号为字符串  
```




##### 4.2.3 解决方案（二）
matplotlib设置自定义字体

```javascript       
import numpy as np        
import pylab as pl        
import matplotlib.font_manager as fm       
myfont = fm.FontProperties(fname=r'D:\Fonts\simkai.ttf') # 设置字体         
plt.xlabel('月份',fontproperties=myfont,fontsize=24) 
plt.ylabel('股价',fontproperties=myfont,fontsize=24)         
plt.show()  
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200525181543725.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80MzM1MzYxMg==,size_16,color_FFFFFF,t_70)


#### 4.3 plt.savefig 保存图片时一片空白
##### 4.3.1 问题
采用如下命令时保存图片，结果图片是一片空白：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200525181612108.png)


原因：其实产生这个现象的原因很简单：在 plt.show() 后调用了 plt.savefig() ，在 plt.show() 后实际上已经创建了一个新的空白的图片（坐标轴），这时候你再 plt.savefig() 就会保存这个新生成的空白图片。



##### 4.3.2 解决方案（一）
在 plt.show() 之前调用plt.savefig()：

```javascript    
import matplotlib.pyplot as plt      
""" 一些画图代码 """      
plt.savefig("filename.png")        
plt.show()  

```




##### 4.3.3 解决方案（二）
画图的时候获取当前图像（这一点非常类似于 Matlab 的句柄的概念）：
```javascript
# gcf: Get Current Figure  
fig = plt.gcf()  
plt.show()        
fig.savefig('tessstttyyy.png', dpi=100)  

```


### 5. 参考与致谢

1.https://blog.csdn.net/lvshu_yuan/article/details/80413005

2.https://blog.csdn.net/zhuzuwei/article/details/80890007

3.https://www.jb51.net/article/154380.htm

4.https://www.cnblogs.com/shona/p/12364216.html

5.https://www.cnblogs.com/zgq25302111/p/11334044.html




