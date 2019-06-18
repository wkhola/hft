#!/usr/bin/python
# encoding:utf-8
import datetime

import service
from azure.servicebus import ServiceBusService
import pickle


class ReceiveMsg(object):
    """
    接收消息队列消息
    """

    def __init__(self):
        self.bus_service = ServiceBusService(
            service_namespace='sb-test',
            shared_access_key_name='RepertorySniffListen',
            shared_access_key_value='Z20KDwxQ1Lbppw3HaP1Wa6PJC94lBIVUEQiuELC7ejs=',
            host_base=".servicebus.chinacloudapi.cn"
        )

    def recevie_data(self, write_sql):
        """
        接收消息队列消息，并将消息插入SQL，成功写入的消息从消息队列删除
        :param write_sql: SQL连接对象
        :return:
        """
        msg = self.bus_service.receive_subscription_message('repertorysniff', 'repertorysub', peek_lock=False)
        if msg.body is not None:
            try:
                if msg.custom_properties['type'] == 'repertory':
                    sql_data = pickle.loads(msg.body)
                    if isinstance(sql_data, list):
                        try:
                            write_sql.write_to_repertory(sql_data)
                        except Exception, e:
                            SqlLog.write_log(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "插入repertory数据库失败" + msg.body)
            except Exception, e:
                SqlLog.write_log(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "插入数据库失败" + msg.body)
                SqlLog.write_log('/n' + str(e))


class WriteSql(object):
    @staticmethod
    def write_to_repertory(data):
        service.insert_repertory_dw(data)


class SqlLog(object):
    @classmethod
    def write_log(self, log_msg):
        """
        将错误日志写到日志文件
        :param log_msg: 错误信息
        :return: 无
        """
        with open("./logs/wifi_log.log", 'a') as log_file:
            log_file.write(log_msg)
