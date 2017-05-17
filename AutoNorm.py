#coding=utf-8
from __future__ import division

############################
# （1）去噪算法：根据概率论的知识，如果一组数据服从正态分布，我们设均值是n，方差是v，那么对于每个离散数值有百分之九十二以上的概率会在（n-3*v,n+3*v）的区间内。所以这里的去噪功能主要是实现如果超出了区间就将这个值标记为区间所能容忍最大值。
#
# （2）归一化：找到输入队列最大值max，最小值min。对任意一个自变量x，它的归一化数值为(x-min/max-min)。
#####################
# 库的实现：输入矩阵mat
# GetAverage(mat)：返回均值
#
# GetVar(average,mat)：返回方差
#
# DenoisMat(mat)：去噪
#
# AutoNorm(mat)：归一化矩阵
#####################
def GetAverage(mat):
    n = len(mat)
    m = width(mat)
    num = [0] * m
    for j in range(0, m):
        for i in mat:
            num[j] = num[j] + i[j]
        num[j] = num[j] / n
    return num


def width(lst):
    i = 0
    for j in lst[0]:
        i = i + 1
    return i


def GetVar(average, mat):
    ListMat = []
    for i in mat:
        ListMat.append(list(map(lambda x: x[0] - x[1], zip(average, i))))

    n = len(ListMat)
    m = width(ListMat)
    num = [0] * m
    for j in range(0, m):
        for i in ListMat:
            num[j] = num[j] + (i[j] * i[j])
        num[j] = num[j] / n
    return num


def DenoisMat(mat):
    average = GetAverage(mat)
    variance = GetVar(average, mat)
    section = list(map(lambda x: x[0] + x[1], zip(average, variance)))

    n = len(mat)
    m = width(mat)
    num = [0] * m
    denoisMat = []
    for i in mat:
        for j in range(0, m):
            if i[j] > section[j]:
                i[j] = section[j]
        denoisMat.append(i)
    return denoisMat


def AutoNorm(mat):
    n = len(mat)
    m = width(mat)
    MinNum = [9999999999] * m
    MaxNum = [0] * m
    for i in mat:
        for j in range(0, m):
            if i[j] > MaxNum[j]:
                MaxNum[j] = i[j]

    for p in mat:
        for q in range(0, m):
            if p[q] <= MinNum[q]:
                MinNum[q] = p[q]

    section = list(map(lambda x: x[0] - x[1], zip(MaxNum, MinNum)))
    # print section
    NormMat = []

    for k in mat:
        distance = list(map(lambda x: x[0] - x[1], zip(k, MinNum)))
        value = list(map(lambda x: x[0] / x[1], zip(distance, section)))
        NormMat.append(value)
    return NormMat


if __name__ == '__main__':
    mat = [[1, 42, 512], [4, 5, 6], [7, 8, 9], [2, 2, 2], [2, 10, 5]]
    a = GetAverage(mat)
    b = GetVar(a, mat)
    print a
    print b
    print DenoisMat(mat)

    #     print list(map(lambda x: x[0]-x[1], zip(v2, v1)))
    print AutoNorm(mat)
# 库的实现：输入矩阵mat
# GetAverage(mat)：返回均值
#
# GetVar(average,mat)：返回方差
#
# DenoisMat(mat)：去噪
#
# AutoNorm(mat)：归一化矩阵