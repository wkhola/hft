#!/usr/bin/python
# encoding:utf-8
import pandas as pd

import common
from warnings import filterwarnings
from common import MySQLdb

filterwarnings('ignore', category=MySQLdb.Warning)

conn = common.conn_mysql
con = common.conn_mysql_datav


def all_sell_detail():
    sql = "select barcode, name, count(Distinct store_id) as counts, SUM(count) as amounts , STD(per_price) as std," \
          "AVG(per_price) as avg from sales_journal where  " \
          "barcode NOT LIKE '9999999%'  AND name <> 'null' AND store_categ='normal' AND  `count`<50 " \
          "and TO_DAYS(NOW()) - TO_DAYS(`operator_time`) > 0 group by barcode having counts >=20 ORDER BY counts DESC"
    result = pd.read_sql(sql, conn)

    columns = ['barcode', 'name', 'counts', 'amounts', 'avg', 'std']
    df = pd.DataFrame(
        dict(barcode=result['barcode'], name=result['name'], counts=result['counts'], amounts=result['amounts'],
             avg=result['avg'], std=result['std']))
    df.to_csv("../templates/all_sell_detail.csv", index=False, sep=',', encoding="utf_8", columns=columns)

    # store_id = list()
    # store_name = list()
    # store_count = list()
    # for barcode in result['barcode']:
    #     base_sql = "select store_id,store_name,sum(count) as store_count, STD(per_price) as std, " \
    #                "AVG(per_price) as avg from sales_journal where barcode= '{}' " \
    #                "AND store_categ='normal' AND  `count`<80  and TO_DAYS(NOW()) - TO_DAYS(`operator_time`) > 0 " \
    #                "group by store_name ORDER BY store_count DESC  limit 1"
    #     barcode_result = pd.read_sql(base_sql.format(barcode), conn)
    #     store_id.append(int(barcode_result['store_id']))
    #     store_name.append(barcode_result['store_name'][0])
    #     store_count.append(int(barcode_result['store_count']))
    # columns = ['barcode', 'name', 'counts', 'amounts', 'std', 'avg', 'store_id', 'store_name', 'store_count']
    # df = pd.DataFrame(
    #     dict(barcode=result['barcode'], name=result['name'], counts=result['counts'], amounts=result['amounts'],
    #          std=result['std'], avg=result['avg'], store_id=store_id, store_name=store_name, store_count=store_count))
    # df.to_csv("../templates/all_sell_detail.csv", index=False, sep=',', encoding="utf_8", columns=columns)

    # 条码是否在条码库中
    # for barcode in result['barcode']:
    #     sql = "select code from barcode where code='{}' ".format(barcode)
    #     sql_result = pd.read_sql(sql, conn)
    #     if len(sql_result) == 0:
    #         print barcode


# all_sell_detail()


def zh_sell_detail():
    sql = "select barcode, name, count(Distinct store_id) as counts, SUM(count) as amounts from sales_journal where " \
          "barcode NOT LIKE '9999999%'  AND name <> 'null' AND store_categ='normal' AND  `count`<80 and city='珠海市' " \
          "group by barcode ORDER BY counts DESC limit 200"
    result = pd.read_sql(sql, conn)

    store_id = list()
    store_name = list()
    store_count = list()
    for barcode in result['barcode']:
        base_sql = "select store_id,store_name,sum(count) as store_count from sales_journal where barcode= {} " \
                   "AND store_categ='normal' AND  `count`<80   " \
                   "group by store_name ORDER BY store_count DESC  limit 1"
        barcode_result = pd.read_sql(base_sql.format(barcode), conn)
        store_id.append(barcode_result['store_id'])
        store_name.append(barcode_result['store_name'])
        store_count.append(barcode_result['store_count'])
    print result['counts']
    columns = ['barcode', 'name', 'counts', 'amounts', 'store_id', 'store_name', 'store_count']
    df = pd.DataFrame(
        dict(barcode=result['barcode'], name=result['name'], counts=result['counts'], amounts=result['amounts'],
             store_id=store_id, store_name=store_name, store_count=store_count))
    df.to_csv("../templates/zh_sell_detail.csv", index=False, sep=',', encoding="utf_8", columns=columns)


# 1、 珠海 选出 5%的店，看一下 有多少是扫码在我们总库没得数据， 有多少商品是我们能提供价格的。
# 以及 店铺订单卖个几单某个商品 但是总库没有 这个商品要加入总库

def check_barcode():
    sql = "select distinct barcode, name from sales_journal where  barcode regexp '^[0-9]+$' " \
          "and barcode NOT LIKE '9999999%' and length(barcode) >7 and length(barcode) <=13"  # store_id in(318,389) and
    result = pd.read_sql(sql, conn)
    checkout_barcode = list()
    checkout_name = list()
    checkout_shopdata_barcode = list()
    checkout_shopdata_name = list()
    for barcode, name in zip(result['barcode'], result['name']):
        sql = "select code,name from barcode where code='{}' ".format(barcode)
        sql_result = pd.read_sql(sql, conn)
        if len(sql_result) == 0:  # 在barcode中是没有条码的
            checkout_barcode.append(barcode)
            checkout_name.append(name)
            # print barcode, name

        # 可以提供价格的条码
        sql = "select code, name from shopdata where code='{}' and affirm_price=1".format(barcode)
        shop_result = pd.read_sql(sql, conn)
        if len(shop_result) > 0:
            checkout_shopdata_barcode.append(barcode)
            checkout_shopdata_name.append(name)
        else:
            # print barcode
            pass

    columns = ['barcode', 'name']
    df = pd.DataFrame({'barcode': result['barcode'], 'name': result['name']})
    df.to_csv("../templates/all_check_barcode.csv", index=False, sep=',', encoding="utf_8", columns=columns)

    # 总库没有条码的商品
    df1 = pd.DataFrame({'barcode': checkout_barcode, 'name': checkout_name})
    df1.to_csv("../templates/all_checkout_barcode.csv", index=False, sep=',', encoding="utf_8", columns=columns)
    # 可以提供价格的条码
    df2 = pd.DataFrame({'barcode': checkout_shopdata_barcode, 'name': checkout_shopdata_name})
    df2.to_csv("../templates/all_checkout_barcode_price.csv", index=False, sep=',', encoding="utf_8", columns=columns)


def find_price():
    """
    查找出可提供商品的所有价格
    :return:
    """
    df = pd.read_csv("../templates/all_checkout_barcode_price.csv")
    # barcode = df['barcode']  # code, name, retail_price
    barcode_set = list()
    price_list = list()
    count = list()
    for barcode in df['barcode']:
        sql = "select code, name, CONVERT(retail_price, DECIMAL(20,2)) as price, count(retail_price) as count from shopdata where code={} " \
              "and affirm_price=1 group by retail_price order by count DESC limit 3 ".format(barcode)
        result = pd.read_sql(sql, conn)
        barcode_set.append(result['code'][0])
        price_list.append(result['retail_price'])
        count.append(result['count'])

    columns = ['barcode', 'price', 'count']
    df = pd.DataFrame({'barcode': barcode_set, 'price': price_list, 'count': count})
    df.to_csv("../templates/barcode_price1.csv", index=False, sep=',', encoding="utf_8", columns=columns)

find_price()
# check_barcode()


# 2、统计店铺卖的 总库没得， 如果加入高级库 对 其他店铺有多少百分百的帮助 减少多少网络请求 （重构高级库  覆盖更多的店铺）

# def

# 3、以及 老高级库对比百服你
#  7735  2460

# 4.  多少种商品 能覆盖店铺50%的销售额
#
# 能覆盖大部分店铺销售额的50% 在percent_50.csv文件中


def cover_fraction():
    sql = "select id, name from store where categ='normal'"
    result = pd.read_sql(sql, conn)
    store_id = list()
    amounts = list()
    for barcode in result['id']:
        base_sql = "select store_id, SUM(receivable) as amounts FROM `order` where store_id = {}".format(barcode)
        base_result = pd.read_sql(base_sql, conn)
        store_id.append(base_result['store_id'][0])
        amounts.append(base_result['amounts'][0])
    columns = ['store_id', 'amounts']
    df = pd.DataFrame({'store_id': store_id, 'amounts': amounts})
    df.to_csv("../templates/store_amounts.csv", index=False, sep=',', encoding="utf_8", columns=columns)


# cover_fraction()
# 5. top10（20，50等） 畅销， 能覆盖100个店铺 1000订单内多少百分比

def top_proportion():
    """
    有售卖top100商品的店铺数
    :return:
    """
    sql = "select barcode from hot_all_sell_total where length(barcode) >7 and barcode NOT LIKE '9999999%' limit 1000"
    result = pd.read_sql(sql, con)
    print result

    barcode_list = list()
    name_list = list()
    count_list = list()
    for barcode in result['barcode']:
        base_sql = "select barcode, trade_name, count(*) as count from hot_per_sell_total where barcode = {}".format(
            barcode)
        base_result = pd.read_sql(base_sql, con)
        barcode_list.append(base_result['barcode'][0])
        name_list.append(base_result['trade_name'][0])
        count_list.append(base_result['count'][0])
    columns = ['store_id', 'name', 'count']
    df = pd.DataFrame({'store_id': barcode_list, 'name': name_list, 'count': count_list})
    df.to_csv("../templates/top_proportion.csv", index=False, sep=',', encoding="utf_8", columns=columns)


# top_proportion()


def read():
    df = pd.read_csv(r'../templates/123.csv')
    barcode_list = list()
    name_list = list()
    count_list = list()
    for barcode in df.values:
        base_sql = "select barcode, trade_name, count(*) as count from hot_per_sell_total where barcode = {} " \
                   "and barcode regexp '^[0-9]+$'".format(barcode[0])
        base_result = pd.read_sql(base_sql, con)
        barcode_list.append(base_result['barcode'][0])
        name_list.append(base_result['trade_name'][0])
        count_list.append(base_result['count'][0])
    columns = ['store_id', 'name', 'count']
    df = pd.DataFrame({'store_id': barcode_list, 'name': name_list, 'count': count_list})
    df.to_csv("../templates/456.csv", index=False, sep=',', encoding="utf_8", columns=columns)


# read()