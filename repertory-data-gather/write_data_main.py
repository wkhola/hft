#!/usr/bin/python
# encoding:utf-8
import datetime
import traceback

from recevice_data import ReceiveMsg, WriteSql, SqlLog


def init():
    """
    项目初始化
    :return:
    """
    sql_log = SqlLog()
    try:
        receive = ReceiveMsg()
        write_sql = WriteSql()
        while True:
            receive.recevie_data(write_sql)
    except Exception, e:
        sql_log.write_log(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "初始化失败")
        sql_log.write_log(traceback.format_exc(e))
    return True
if __name__ == '__main__':
    init()
