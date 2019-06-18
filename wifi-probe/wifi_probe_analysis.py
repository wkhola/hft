#!/usr/bin/python
# encoding:utf-8
import pandas as pd
from pandas import to_datetime  # 日期格式转换
import time

# df = pd.read_csv("./daily/2018-0-19.csv", index_col=False, delimiter=',')
# df2 = pd.read_csv("./daily/2018-0-20.csv", index_col=False, delimiter=',')

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


# 计算给个mac地址停留时长

# i = 0
# start = time.time()
# dfd = df.drop_duplicates(subset=['mac'], keep='first', inplace=False)
# dfd = dfd[dfd['shop_id'] == 110].mac.values
# dfd1 = df2.drop_duplicates(subset=['mac'], keep='first', inplace=False)
# dfd1 = dfd1[dfd1['shop_id'] == 110].mac.values
# for mac in df.drop_duplicates(subset=['mac'], keep='first', inplace=False)[df['shop_id'] == 7].mac.values:
#     for mac2 in df2.drop_duplicates(subset=['mac'], keep='first', inplace=False)[df['shop_id'] == 7].mac.values:
#         if mac == mac2:
#             i += 1

# 回头率
# for mac in dfd:
#     for mac2 in dfd1:
#         if mac == mac2:
#             i += 1
# print i/float(len(df2.drop_duplicates(subset=['mac'], keep='first', inplace=False)))
# print i
# print i / float(len(dfd1))
# # print len(df2)
# print len(dfd)
# print len(dfd1)
# print time.time() - start


# df = df.drop_duplicates(subset=['mac'], keep='first', inplace=False)
# # df = df.drop_duplicates(subset=['mac'], keep='first', inplace=False)[df['shop_id'] == 7]
# # print df
# for shop_id in df.drop_duplicates(subset=['shop_id'], keep='first', inplace=False).shop_id:
#     # print df[df['shop_id'] == q]
#     for mac in df.drop_duplicates(subset=['mac'], keep='first', inplace=False)[df['shop_id'] == shop_id].mac.values:
#         for mac2 in df2.drop_duplicates(subset=['mac'], keep='first', inplace=False)[df['shop_id'] == shop_id].mac.values:
#             if mac == mac2:
#                 i += 1
#     print i / float(len(df2.drop_duplicates(subset=['mac'], keep='first', inplace=False)))

class analysis(object):

    def __init__(self):
        self.store_id = ''

    def passenger_flow(self, store_id):
        """
        统计店铺的客流量
        :return:
        """
        self.store_id = store_id
        df = pd.read_csv("./daily/2018-05-17.csv", index_col=False, delimiter=',')
        df_time = to_datetime(df.time, format='%Y/%m/%d')  # 时间格式化

        # 所有店铺的客流量
        count = len(df.drop_duplicates(subset=['mac'], keep='first', inplace=False))

        # 店铺一天的客流量
        count_day = df.groupby('shop_id').agg({'shop_id': 'max', 'mac': pd.Series.nunique})

        # 按小时计算店铺的客流量
        count_hour = df[df['shop_id'] == store_id].groupby(['shop_id', df_time.dt.hour]) \
            .agg({'mac': pd.Series.nunique, 'time': 'min'}) \
            # .sort_values(['shop_id', 'mac'], ascending=[True, False])

        t = count_hour.time
        count = count_hour.mac
        from pyecharts import Bar, Line
        ts = [str(_).split(':')[0].split('2018-')[1] for _ in t]
        print count_hour
        bar = Line(width="100%")
        bar.add("店铺客流量", ts, count,
                is_datazoom_show=True,
                is_label_show=True)

        bar.render(u"客流量.html")

    def second_glance(self, store_id, date):
        """
        统计店铺回头率
        :return:
        """
        self.store_id = store_id
        df = pd.read_csv("./daily/2018-05-17.csv", index_col=False, delimiter=',')
        df_time = to_datetime(df.time, format='%Y/%m/%d')  # 时间格式化
        count_hour = df[df['shop_id'] == store_id].groupby(['shop_id', df_time.dt.hour]) \
            .agg({'mac': pd.Series.nunique, 'time': 'min'})


analysis().passenger_flow(7)
