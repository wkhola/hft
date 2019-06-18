#!/usr/bin/python
# encoding:utf-8
import sys, MySQLdb, traceback
import time


class ConnectMysql(object):
    def __init__(self, connection):
        self.connection = connection
        self.conn = None
        self._conn()

    def _conn(self):
        try:
            self.conn = self.connection
            return True
        except:
            return False

    def _reConn(self, num=28800, stime=3):  # 重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()  # cping 校验连接是否异常
                _status = False
            except:
                if self._conn():  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    def select(self, sql=''):
        try:
            self._reConn()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.cursor.close()
            return result
        except MySQLdb.Error, e:
            return False

    def query(self, sql=''):
        try:
            self._reConn()
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute("set names utf8")  # utf8 字符集
            result = self.cursor.execute(sql)
            self.conn.commit()
            self.cursor.close()
            return True, result
        except MySQLdb.Error, e:
            return False

    def close(self):
        self.conn.close()
