#!/usr/bin/python
# encoding:utf-8
import json

from azure.servicebus import ServiceBusService
import pickle


class ReceiveMsg(object):
    def __init__(self):
        self.bus_service = ServiceBusService(
            service_namespace='sb-test',
            shared_access_key_name='testorder-hureader',
            shared_access_key_value='TgD2yvEdveW20KNEpsNQX+Eq2RTlBFrTM43Cmf+aAqc=',
            host_base=".servicebus.chinacloudapi.cn"
        )

    def recevie_msg(self):
        msg = self.bus_service.receive_subscription_message('odersniff', 'testorder-reader', peek_lock=True)
        if msg.body is not None:
            # if msg.custom_properties['num'] == '1':
            data = json.loads(msg.body)
            # data = msg.body
            # if msg.custom_properties['num'] == '1':
            #     data = msg.body
            print data
        msg.delete()


if __name__ == '__main__':
    import time

    start = time.time()
    recevie = ReceiveMsg()
    while True:
        recevie.recevie_msg()
        end = time.time()
        print end - start

