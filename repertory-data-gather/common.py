# coding:utf8

import MySQLdb
import ConfigParser
import string
import os
from logger import Logger

"""
公共组件文件, 包含所有公共方法供使用
"""
__author__ = 'WuKai'

logger = Logger('common.py')

conf = ConfigParser.ConfigParser()
# conf.read("/home/hft/odoo-gather-python/barcode-gather/config.conf")
conf.read("./config.conf")
last_update_repertory_file_path = conf.get('common', 'last_update_repertory_file_path')

# Get connection for mysql
conn_mysql_repertory = MySQLdb.connect(
    host=conf.get('mysql-repertory', 'db_host'),
    port=string.atoi(conf.get('mysql-repertory', 'db_port')),
    user=conf.get('mysql-repertory', 'db_user'),
    passwd=conf.get('mysql-repertory', 'db_password'),
    db=conf.get('mysql-repertory', 'db_db'),
    charset='utf8'
)

# Get connection for postgresql
conn_mysql_datawarehouse = MySQLdb.connect(
    host=conf.get('mysql-datawarehouse', 'db_host'),
    port=string.atoi(conf.get('mysql-datawarehouse', 'db_port')),
    user=conf.get('mysql-datawarehouse', 'db_user'),
    passwd=conf.get('mysql-datawarehouse', 'db_password'),
    db=conf.get('mysql-datawarehouse', 'db_db'),
    charset='utf8'
)


def close_all_connection():
    """
    Close all config connection
    :return: None
    """
    conn_mysql_repertory.close()
    conn_mysql_datawarehouse.close()


def init():
    """
    初始化
    :return:
    """
    if not os.path.exists(last_update_repertory_file_path):
        open(last_update_repertory_file_path, 'a')
        logger.info("缓存上次查询的缓存文件: " + last_update_repertory_file_path + " 不存在, 创建...")


def get_last_update_repertory():
    """
    获得上次查询到的update barcode
    :return: 0 第一次, 非第一次返回store_id
    """
    last_update_repertory_file_r = open(last_update_repertory_file_path, 'r')
    last_update_repertory = last_update_repertory_file_r.readline()
    if not last_update_repertory:
        logger.info("查询上次查询的更新id(repertory)方法: 这是第一次查询, 返回为0")
        return '0'
    else:
        logger.info("查询上次查询的更新id(repertory)方法: 从文件中取得last_update为: " + str(last_update_repertory))
        return str(last_update_repertory).strip()


def write_last_update_repertory(last_update):
    """
    写上次查询到的last_update repertory到文件中, 每次都清空文件.
    :param last_update:
    :return: None
    """
    if str(last_update):
        logger.info("写last_update(repertory)到缓存文件中, 当前last_update为: " +
                    str(get_last_update_repertory()) + ", 当前写入: " + str(last_update))
        last_update = str(last_update)
        last_update_repertory_file_w = open(last_update_repertory_file_path, 'w')
        last_update_repertory_file_w.write(last_update)


init()
