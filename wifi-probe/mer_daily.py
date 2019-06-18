#!/usr/bin/python
# encoding:utf-8
import os

import datetime
import time
import pandas as pd


def msg(dfm):
    # 将今天的数据合并在一个文件
    files = []
    count = 0
    for filename in os.listdir(r'./result'):
        if dfm in str(filename) and 'zip' not in str(filename):
            print filename  # 当前路径下所有非目录子文件
            files.append(pd.read_csv("./result/{}".format(filename),  # header=0 这个参数在合并的时候去掉表头
                                     delimiter=',', header=0, names=["shop_id", 'mac', 'time']))
        count += 1
    df = pd.concat(files)  # 合并文件

    # 合并后格式化数据并去重
    i = 0
    mac = list()
    shop_id = list()
    times = list()
    for _ in df.values:
        mac_id = str(df.mac.values[i]).split('|')[0]
        if len(mac_id) == 17:
            mac.append(mac_id)
            shop_id.append(df.shop_id.values[i])
            times.append(df.time.values[i])
        i += 1

    df = pd.DataFrame(
        {'mac': mac, 'shop_id': shop_id, 'time': times})
    columns = ['shop_id', 'mac', 'time']
    df = df.drop_duplicates()  # 去除重复项
    df = df.sort_values(by=['shop_id', 'mac', 'time'])
    df.to_csv('./daily/{}.csv'.format(dfm), index=False, sep=',', encoding="utf_8", columns=columns)

    # df.to_csv('./daily/{}.csv'.format(dfm), index=False, sep=',', delimiter=',')


def count_mac():
    df = pd.read_csv("./daily/2018-05-17.csv")

    # mac = list()
    shop_id = list()
    times = list()
    # 记录mac第一次出现的时间 和 最后一次出现的时间
    id = df[df["mac"] == "00:00:00:00:74:F1"].iloc[[0]].shop_id.values[0]

    mac = df[df["mac"] == "00:00:00:00:74:F1"].iloc[[0]].mac.values[0]

    # 时间差
    first_time = df[df["mac"] == "00:00:00:00:74:F1"].iloc[[0]].time.values[0]
    first = time.strptime(first_time, "%Y-%m-%d %H:%M:%S")
    first = datetime.datetime(first[0], first[1], first[2], first[3], first[4], first[5])

    end_time = df[df["mac"] == "00:00:00:00:74:F1"].iloc[[-1]].time.values[0]
    end = time.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    end = datetime.datetime(end[0], end[1], end[2], end[3], end[4], end[5])
    print (end - first).seconds

    # 记录mac的出现次数
    count = df[df["mac"] == "00:00:00:00:74:F1"].mac.count()
    start = time.time()
    i = 0
    # for mac in df.values:
    #     i += 1
    #
    #     print mac, df.time[0]

    # for i, mac in df.iterrows():
    #     # if i > 2 :
    #     #     break
    #     print i, mac.values[2]
    end = time.time()
    print end - start
    # print id, mac, first_time, end_time, count


class MacEtl(object):

    def __init__(self):
        pass

    def mac_etl(self):
        pass

if __name__ == '__main__':
    today = datetime.date.today()
    oneday = datetime.timedelta(days=5)
    yesterday = today - oneday
    yesterday = str(yesterday)
    # msg(yesterday)
    count_mac()
