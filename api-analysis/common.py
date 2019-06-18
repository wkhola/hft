# coding:utf8

import ConfigParser
import pymysql
import string

__author__ = 'WuKai'

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


