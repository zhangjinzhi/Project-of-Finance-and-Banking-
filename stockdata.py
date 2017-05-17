#coding=utf-8
import tushare as ts
import sys
from sqlalchemy import create_engine


def get_hist_data():
    PLICC = ts.get_hist_data(code='601628',start='2014-01-01',end='2017-01-01')

    engine = create_engine('mysql+pymysql://root:zjz4818774@127.0.0.1/tusharedata?charset=utf8')

    try:
        PLICC.to_sql('PLICC_data', engine, if_exists='append')

    except Exception, e:
        print Exception, ":", e


def get_k_data():
    PLICC = ts.get_k_data(code='601318',ktype='D',autype='qfq',start='2015-01-01',end='2017-01-01')

    engine = create_engine('mysql+pymysql://root:zjz4818774@127.0.0.1/tusharedata?charset=utf8')

    try:
        PLICC.to_sql('PingAnInsurance', engine, if_exists='append')

    except Exception, e:
        print Exception, ":", e

def get_stock_basics():
    all_stock = ts.get_stock_basics()

    engine = create_engine('mysql+pymysql://root:zjz4818774@127.0.0.1/tusharedata?charset=utf8')

    try:
        all_stock.to_sql('all_stock', engine, if_exists='append')

    except Exception, e:
        print Exception, ":", e

if __name__ == '__main__':
    get_hist_data()
    # get_k_data()
    # PLICC = ts.get_hist_data(code='601628', start='2017-01-01', end='2017-03-01')
    # print  PLICC
    # get_stock_basics()