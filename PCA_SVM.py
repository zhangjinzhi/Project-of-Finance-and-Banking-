# coding=utf-8
import sys
import tushare as ts
import numpy as np
import MySQLdb
import pandas as pd
import matplotlib.pyplot as plt
###########################################################
#动态散点图

# plt.axis([0, 100, 0, 1])
# plt.ion()
#
# for i in range(100):
#     y = np.random.random()
#     plt.scatter(i, y)
#     plt.pause(0.1)
##########################################################
reload(sys)
sys.setdefaultencoding('utf8')

# 打开数据库连接
db =MySQLdb.connect(host='127.0.0.1',user='root',passwd='zjz4818774',db='tusharedata',port=3306,charset='utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()


# SQL 查询语句
# sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
# sql = 'select * from PLICC_data'
sql1 = 'select date,open,high,close,low,volume,ma5,ma10,ma20,price_change from PLICC_data  order by date asc'
sql2 = 'select date,open,high,close,low from PingAnInsurance  order by date asc'

try:
    cursor.execute(sql1)

    rows = cursor.fetchall()
    #获取连接对象的描述信息
    # desc = cursor.description
    # print 'cursor.description:',desc

    # #打印表头，就是字段名字
    # print "%s %3s" % (desc[0][0], desc[1][0])

    # for row in rows:
    #     print row

except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])

# 关闭数据库连接
db.close()

# price_data = [[-1, -1], [-2, -1], [1, 1], [2, 1]]
price_data = []
# tag = [1, 1, 2, 2]
tag = []

line_num = 0
for row in rows:
    line_num += 1

    if line_num < 402:

        col = []
        for i in range(1,9):
           col.append(row[i])

        price_data.append(col)

        if row[9] > 0 :
           tag.append(1)
        else:
           tag.append(0)


price_data = price_data[:-1]
tag  =  tag[1:]

X = np.array(price_data)
Y = np.array(tag)
###########################################
from AutoNorm import *
X = AutoNorm(X)
print X
#########################################
from sklearn.decomposition import PCA
pca=PCA(n_components='mle')
X_train=pca.fit_transform(X)
print X_train[0]
# print pca.n_components
##########################################
from sklearn import svm
from sklearn.svm import NuSVC
# clf = NuSVC()
# clf.fit(X_train, Y)

clf_linear  = svm.SVC(kernel='linear').fit(X_train, Y)
#clf_linear  = svm.LinearSVC().fit(X_train, Y)
clf_poly    = svm.SVC(kernel='poly', degree=3).fit(X_train, Y)
clf_rbf     = svm.SVC().fit(X_train, Y)
clf_sigmoid = svm.SVC(kernel='sigmoid').fit(X_train, Y)

clf = clf_rbf

######################################
predict_price_data = []
real_tag = []
line_num = 0
for row in rows:
    line_num += 1
    if line_num > 400 and line_num < 440:
        predict_col = []
        for i in range(1, 9):
            predict_col.append(row[i])
        predict_price_data.append(predict_col)

        if row[9] > 0 :
            real_tag.append(1)
        else:
            real_tag.append(0)

# print real_tag
# print predict_price_data
predict_price_data = predict_price_data[:-1]
real_tag = real_tag[1:]

X_ = np.array(predict_price_data)
Y_ = np.array(real_tag)
#####################################
X_ = AutoNorm(X_)
######################################
X_test=pca.transform(X_)
print X_test[0]
######################################
correct = 0.0
i = 0
for price_list in X_test:
    # print price_list
    print clf.predict([price_list])
    if clf.predict([price_list]) == real_tag[i]:
        correct += 1
    i += 1

print "test accuracy is :"
print clf.score(X_test,Y_)

print "predict correct rate is : " + str(correct/len(real_tag))
##################用于随机抽取训练集合和测试集合
# X_train, X_test, y_train, y_test = cross_validation.train_test_split(train_data, train_target, test_size=0.4, random_state=0)