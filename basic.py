#! /usr/bin/env python
#coding=utf-8

import math
import cx_Oracle
import numpy as np
import matplotlib.pyplot as plt

print 'step0-开始提取数据'
con = cx_Oracle.connect('system/asz@ASZ')     # 账号名/密码@tns
cur = con.cursor()
sql = "select VO_CDMA_COUNT_M1,MB_ARPU_CDMA_M1 from tydc_data.MONTH_C_ALL_201305 where ci_city='成都' "
try:
    cur.execute(sql.encode('gb2312'))    #注意编码方式的统一
except:
    cur.execute(sql) 
fetch = cur.fetchall()
data1=[i[0] for i in fetch]
data2=[i[1] for i in fetch]
cur.close()
print 'step1-成功提取'+str(len(data1))+','+str(len(data2))+'条数据'

#单变量特征分析（getMedine中位数），（getMean平均值），（getStdev方差）
def getMedine(data):
    data.sort()
    return data[len(data)//2]
def getMean(data):
    mean = sum(data)*1.0/len(data)
    return mean
def getStdev(data):
    var  = ((sum([i**2 for i in data])-sum(data)**2/len(data))/(len(data)-1))**0.5
    return var 
#多变量特征分析
#皮尔逊相似度（线性相关度）
def getPearson(data1,data2):
    sumofxy = float(sum([data1[i]*data2[i] for i in range(len(data1))]))
    sumofx  = float(sum(data1))
    sumofy  = float(sum(data2))
    sumofx2 = float(sum([i**2 for i in data1]))
    sumofy2 = float(sum([i**2 for i in data2]))
    n = len(data1)
    r = (n*sumofxy-sumofx*sumofy)/(((n*sumofx2-sumofx**2)*(n*sumofy2-sumofy**2))**0.5)
    return r
#欧几里得相似度（空间距离）
def getEuclidean(data1,data2):
    r = 1/(1+(sum([(data1[i]-data2[i])**2 for i in range(len(data1))]))**0.5)
    return r
#余弦相似度
def getCosin(data1,data2):
    sumofxy = sum([data1[i]*data[i] for i in range(len(data1))])
    x2 = sum([data1[i]**2 for i in range(len(data1))])
    y2 = sum([data2[i]**2 for i in range(len(data2))])
    r  = sumofxy/((x2*y2)**0.5)
    return r 
def getCumolus(n):
    return reduce(lambda x,y:x+y,range(1,n+1))
def getCumtime(n):
    return reduce(lambda x,y:x*y,range(1,n+1))

plt.hist(data1, 1000, normed=1, facecolor='r', alpha=0.5)
plt.xlabel('churn_rate')
plt.ylabel('Pro')
plt.title('Histogram of IQ')
# plt.text(60, 0.025, r'$\mu=100,\ \sigma=15$')
plt.axis([0, max(data2), 0, 0.01])
plt.grid(False)
plt.show()

