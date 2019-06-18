#!/usr/bin/python
# encoding:utf-8
import pickle
import sys

import datetime

import service
from send_data import SendReceiveMsg
from recevice_data import SqlLog
import traceback


class RepertoryAdd(object):
    @staticmethod
    def get_data():
        try:
            data = service.query_repertory()
            send_receive = SendReceiveMsg()
            data_size = sys.getsizeof(data) / 1024
            if data_size <= 250:
                send_receive.send_data(pickle.dumps(data), "repertory")
            else:
                pass
        except Exception, e:
            SqlLog.write_log(traceback.format_exc(e))
            SqlLog.write_log(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "获取数据失败\n")


RepertoryAdd.get_data()
