# coding:utf8

import ConfigParser
import MySQLdb
import pymysql
from flask import Flask
import string

app = Flask(__name__)

__author__ = 'WuKai'
# ROOT_PATH = '/home/caoyu/wukai/shop_detail_info_echarts/hft_echarts/'
# ROOT_PATH = 'D:/code/pythoncopy_echarts/hft_echarts/'
ROOT_PATH = './'

conf = ConfigParser.ConfigParser()
conf.read(ROOT_PATH + "config.conf")
# conf.read("config.conf")

# Get connection for mysql
conn_mysql = pymysql.connect(
    host=conf.get('mysql', 'db_host'),
    port=string.atoi(conf.get('mysql', 'db_port')),
    user=conf.get('mysql', 'db_user'),
    passwd=conf.get('mysql', 'db_password'),
    db=conf.get('mysql', 'db_db'),
    charset='utf8'
)
conn_mysql_datav = MySQLdb.connect(
    host=conf.get('mysql-datav', 'db_host'),
    port=string.atoi(conf.get('mysql-datav', 'db_port')),
    user=conf.get('mysql-datav', 'db_user'),
    passwd=conf.get('mysql-datav', 'db_password'),
    db=conf.get('mysql-datav', 'db_db'),
    charset='utf8'
)
