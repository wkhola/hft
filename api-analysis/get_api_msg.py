#!/usr/bin/python
# encoding:utf-8

import common
import pandas as pd

conn = common.conn_mysql


def read_mysql_from_dw():
    sql = "select * from `order` where date >= '2018-11-27' and date <= '2019-01-27' and store_id = 333"
    result = pd.read_sql(sql, conn)

    a = result.groupby(['project', 'module', 'method']).count()

    print a


read_mysql_from_dw()
