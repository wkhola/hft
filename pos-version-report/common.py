# coding:utf8

import ConfigParser
import psycopg2
import MySQLdb
import string
from logger import Logger

__author__ = 'WuKai'
# ROOT_PATH = '/home/hft/daily-report/'
ROOT_PATH = 'D:/DATA/pos-version-report/'
# ROOT_PATH = './'

logger = Logger('common.py')
conf = ConfigParser.ConfigParser()
conf.read(ROOT_PATH + "config.conf")
# conf.read("config.conf")

# Get connection for PostgreSQL
conn_pg = psycopg2.connect(
    host=conf.get('PostgreSQL', 'db_host'),
    port=string.atoi(conf.get('PostgreSQL', 'db_port')),
    user=conf.get('PostgreSQL', 'db_user'),
    password=conf.get('PostgreSQL', 'db_password'),
    database=conf.get('PostgreSQL', 'db_db')
)

conn_mysql = MySQLdb.connect(
    host=conf.get('mysql', 'db_host'),
    port=string.atoi(conf.get('mysql', 'db_port')),
    user=conf.get('mysql', 'db_user'),
    passwd=conf.get('mysql', 'db_password'),
    db=conf.get('mysql', 'db_db'),
    charset='utf8'
)
