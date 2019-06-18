#!/usr/bin/python
# encoding:utf-8
from azure.servicebus import ServiceBusService
import pickle

topic_name = 'odersniff'
subscription_name = 'order-reader2'


class ReceiveMsg(object):
    def __init__(self):
        self.bus_service = ServiceBusService(
            service_namespace='sb-test-demo',
            shared_access_key_name='RootManageSharedAccessKey',
            shared_access_key_value='u9oq3ZdjpzALZ+6xiJO3VPke/w3fe8qogVVb4y7WfSw=',
            host_base=".servicebus.chinacloudapi.cn"
        )

    def receive_msg(self):
        msg = self.bus_service.receive_subscription_message(topic_name, subscription_name, peek_lock=False)
        if msg.body is not None:
            if msg.custom_properties['type'] == 'repertory':
                repertory_data = pickle.loads(msg.body)
                # if msg.custom_properties['num'] == '1':
                #     data = msg.body
                print repertory_data

        if not msg.body:
            dlq_name = self.bus_service.format_dead_letter_subscription_name(subscription_name)
            sb_msg = self.bus_service.receive_subscription_message(topic_name, dlq_name, peek_lock=False)
            print sb_msg.body


if __name__ == '__main__':
    import time

    start = time.time()
    receive = ReceiveMsg()
    while True:
        receive.receive_msg()
        end = time.time()
        print end - start
