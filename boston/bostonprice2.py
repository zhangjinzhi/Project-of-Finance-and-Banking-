#coding=utf8
from sklearn.datasets import load_boston
import numpy as np
boston = load_boston()

from sklearn.model_selection import *
from sklearn.model_selection import train_test_split
# 依然如故，我们对数据进行分割
X_train, X_test, y_train, y_test = train_test_split(boston.data, boston.target, test_size = 0.25, random_state=33)

from sklearn.preprocessing import StandardScaler

# 正规化的目的在于避免原始特征值差异过大，导致训练得到的参数权重不一
scalerX = StandardScaler().fit(X_train)
X_train = scalerX.transform(X_train)
X_test = scalerX.transform(X_test)

scalery = StandardScaler().fit(y_train)
y_train = scalery.transform(y_train)
y_test = scalery.transform(y_test)

def train_and_evaluate(clf, X_train, y_train):
    scores = cross_val_score(clf, X_train, y_train, cv=5)
    print 'Average coefficient of determination using 5-fold cross validation:', np.mean(scores)

from sklearn.svm import SVR
clf_svr_rbf = SVR(kernel='rbf')
# RBF (径向基核更是牛逼！)
train_and_evaluate(clf_svr_rbf, X_train, y_train)


# 再来个更猛的! 极限回归森林，放大招了！！！
from sklearn import ensemble
clf_et = ensemble.ExtraTreesRegressor()
train_and_evaluate(clf_et, X_train, y_train)
# 最后看看在测试集上的表现
clf_et.fit(X_train, y_train)
print clf_et.score(X_test, y_test)