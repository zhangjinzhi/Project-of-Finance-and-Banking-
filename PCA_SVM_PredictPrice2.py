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

price_data = []
tag = []

line_num = 0
for row in rows:
    line_num += 1

    if line_num < 401:

        col = []
        for i in range(1,9):
           col.append(row[i])

        price_data.append(col)

        # if row[9] > 0 :
        #    tag.append(1)
        # else:
        #    tag.append(0)
        tag.append(row[3])


price_data = price_data[:-1]
# print price_data
tag  =  tag[1:]
# print tag

X = np.array(price_data)
Y = np.array(tag)

###########################################
# from AutoNorm import *
# X_AutoNorm= AutoNorm(X)
# print X[0]

#########################################
from sklearn.decomposition import PCA
pca=PCA(n_components='mle')
X_PCA=pca.fit_transform(X)

# print pca.n_components
##########################################
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# 同样是分割数据 25%用于测试
X_train, X_test, y_train, y_test = train_test_split(X_PCA, Y, test_size=0.25, random_state=0)
#########################################
# import AutoNorm
# origin_average = AutoNorm.GetAverage(y_test)
# origin_var = AutoNorm.GetAverage(origin_average,y_test)
##########################################
from sklearn.preprocessing import StandardScaler

# 正规化的目的在于避免原始特征值差异过大，导致训练得到的参数权重不一
scalerX = StandardScaler().fit(X_train)
X_train = scalerX.transform(X_train)
X_test = scalerX.transform(X_test)

scalery = StandardScaler().fit(y_train)
y_train = scalery.transform(y_train)
y_test = scalery.transform(y_test)
##############################################
from sklearn.model_selection import *


def train_and_evaluate(clf, X_train, y_train):
    scores = cross_val_score(clf, X_train, y_train, cv=5)
    print scores
    print 'Average coefficient of determination using 5-fold cross validation:', np.mean(scores)

from sklearn.svm import SVR
clf_svr_rbf = SVR(kernel='rbf')
# RBF (径向基核更是牛逼！)
train_and_evaluate(clf_svr_rbf, X_train, y_train)

##############################
clf_rbf = SVR(kernel='rbf')
clf_rbf.fit(X_train, y_train)
print clf_rbf.score(X_test, y_test)

# OriginPredictData = clf_rbf.predict(X_test)
# print OriginPredictData

# predict_closing_price = OriginPredictData*origin_var + origin_average
# print predict_closing_price


#
#
# data_train = X_train
# target_train=y_train
# data_test = X_test
# target_test=y_test
#
# from sklearn import model_selection
# from sklearn.naive_bayes import GaussianNB
# from sklearn import tree
# from sklearn.ensemble import RandomForestClassifier
# from sklearn import svm
# import datetime
# estimators = {}
# estimators['bayes'] = GaussianNB()
# estimators['tree'] = tree.DecisionTreeClassifier()
# estimators['forest_100'] = RandomForestClassifier(n_estimators = 100)
# estimators['forest_10'] = RandomForestClassifier(n_estimators = 10)
# estimators['svm_c_rbf'] = svm.SVC()
# estimators['svm_c_linear'] = svm.SVC(kernel='linear')
# estimators['svm_linear'] = svm.LinearSVC()
# estimators['svm_nusvc'] = svm.NuSVC()
#
# for k in estimators.keys():
#     start_time = datetime.datetime.now()
#     print '----%s----' % k
#     estimators[k] = estimators[k].fit(data_train, target_train)
#     pred = estimators[k].predict(data_test)
#     print pred
#     print("%s Score: %0.2f" % (k, estimators[k].score(data_test, target_test)))
#     scores = model_selection.cross_val_score(estimators[k], data_test, target_test, cv=5)
#     print("%s Cross Avg. Score: %0.2f (+/- %0.2f)" % (k, scores.mean(), scores.std() * 2))
#     end_time = datetime.datetime.now()
#     time_spend = end_time - start_time
#     print("%s Time: %0.2f" % (k, time_spend.total_seconds()))