#!/usr/bin/python
# encoding:utf-8
import datetime
import pandas as pd
import sys
from pandas import to_datetime  # 日期格式转换
import time

# 日期的抽取
"""
df_time.dt.year
df_time.dt.second
df_time.dt.minute
df_time.dt.hour
df_time.dt.day
df_time.dt.month
df_time.dt.weekday
"""


# 计算每个mac地址停留时长


class analysis(object):
    def __init__(self):
        self.store_id = ''

    def passenger_flow(self, store_id):
        """
        统计店铺的区域整体客流量
        :return:
        """
        self.store_id = store_id
        df = pd.read_csv("./daily/2018-05-27.csv", index_col=False, delimiter=',', low_memory=False)
        df_time = to_datetime(df.time, format='%Y/%m/%d')  # 时间格式化

        # 所有店铺的客流量
        count = len(df.drop_duplicates(subset=['cus_mac'], keep='first', inplace=False))

        # 店铺一天的客流量
        count_day = df.groupby('shop_id').agg({'shop_id': 'max', 'cus_mac': pd.Series.nunique})

        # 按小时计算店铺的客流量
        count_hour = df[df['shop_id'] == store_id].groupby(['shop_id', df_time.dt.hour]) \
            .agg({'cus_mac': pd.Series.nunique, 'time': 'min'}) \
            # .sort_values(['shop_id', 'cus_mac'], ascending=[True, False])
        print df.head(10)
        return count_day
        # t = count_hour.time
        # count = count_hour.cus_mac
        # from pyecharts import Bar, Line
        # ts = [str(_).split(':')[0].split('2018-')[1] for _ in t]
        # print count_hour
        # bar = Line(width="100%")
        # bar.add("店铺客流量", ts, count,
        #         is_datazoom_show=True,
        #         is_label_show=True)
        #
        # bar.render(u"客流量.html")

    def enter_rate(self, store_id):
        """
        进店率
        :param store_id:
        :return:
        """
        sum = 0
        with open("./daily/2018-06-18.csv", "r") as f:
            for l in f.readlines():
                ls = l.split(',')
                nt = ls[-1]
            print("sum=", sum)

    def second_glance(self, store_id):
        """
        统计店铺回头率
        :return:
        """
        self.store_id = store_id
        df = pd.read_csv("./daily/2018-06-18.csv", index_col=False, delimiter=',', low_memory=False)
        df1 = pd.read_csv("./daily/2018-05-17.csv", index_col=False, delimiter=',', low_memory=False)
        df2 = pd.read_csv("./daily/2018-05-19.csv", index_col=False, delimiter=',', low_memory=False)
        df2 = df2.drop_duplicates(subset=['cus_mac'], keep='first', inplace=False)
        df2 = df2[df2['shop_id'] == store_id].cus_mac.values

        df = df.drop_duplicates(subset=['cus_mac'], keep='first', inplace=False)
        df = df[df['shop_id'] == store_id].cus_mac.values
        df1 = df1.drop_duplicates(subset=['cus_mac'], keep='first', inplace=False)
        df1 = df1[df1['shop_id'] == store_id].cus_mac.values
        count = 0
        for mac in df:
            for mac2 in df1:
                if mac == mac2:
                    count += 1
        print count / float(len(df)), count, len(df), len(df1), len(df2)


# analysis().passenger_flow(378)
# analysis().second_glance(200)
# df = pd.read_csv("./daily/2018-05/2018-05-27.csv", index_col=False, delimiter=',', low_memory=False)
# print df.head()
from pandasql import sqldf


def pysqldf(query):
    """
    使用该函数后可以不再添加locals()参数
    """
    return sqldf(query, globals())


# for data in df.values:
#     print data[-1]
#     sys.exit()
# df = pd.read_csv("./daily/2018-05/2018-05-16.csv", index_col=False, delimiter=',', low_memory=False)
# print df.head()

def query_func():
    global df
    locals()
    df = pd.read_csv("./daily/2018-05/2018-05-16.csv", low_memory=False)
    row_list = list()
    for data in df.values:
        row_list.append(data.tolist())
    print len(row_list)
    return row_list

row_list = query_func()
print row_list[1]
for i, j in zip(range(0, len(row_list) - 1), range(1, len(row_list))):
    data1 = row_list[i]
    data2 = row_list[j]
    d1 = datetime.datetime.strptime('{}'.format(data1[-1]), '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime('{}'.format(data2[-1]), '%Y-%m-%d %H:%M:%S')

    if data1[0] == data2[0]:
        if data1[1] == data2[1]:
            print data1[1]
        else:
            print 1
            print data2[1]
            sys.exit()
    else:
        print 0
        sys.exit()
    # delta = d1 - d2
    # if delta.seconds > 60:
    #     print rowlist[i]
    # # a = rowlist[i].split(",")[-1] - rowlist[i].split(",")[-1]
    # # if i == 10:
    # #     sys.exit()
