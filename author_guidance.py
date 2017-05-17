#coding=utf-8
# from sqlalchemy import create_engine
# import tushare as ts
#
# df = ts.get_tick_data('600848', date='2014-12-22')
# engine = create_engine('mysql://root:zjz4818774@127.0.0.1/tusharedata?charset=utf8')
#
# #存入数据库
# df.to_sql('tick_data',engine)
#
# #追加数据到现有表
# #df.to_sql('tick_data',engine,if_exists='append')


import tushare as ts
import sys
from sqlalchemy import create_engine

def industrytodb():
    #获取sina行业分类信息
    industry_sina = ts.get_industry_classified("sina")
    #获取申万行业分类信息
    industry_sw = ts.get_industry_classified("sw")

    engine = create_engine('mysql+pymysql://root:zjz4818774@127.0.0.1/tusharedata?charset=utf8')
    industry_sina.to_sql('industry_sina_data',engine,if_exists='append')
    industry_sw.to_sql('industry_sw_data',engine,if_exists='append')
    # industry_sina.to_sql('industry_sina_data',engine)
    # industry_sw.to_sql('industry_sw_data',engine)





if __name__ == '__main__':
    # 获取sina和申万行业分类信息
    industrytodb()