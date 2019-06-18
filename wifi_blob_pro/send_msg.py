#!/usr/bin/python
# encoding:utf-8
import json
import time
from azure.servicebus import ServiceBusService, Message


class SendReceiveMsg(object):
    # def __init__(self):
    #     self.bus_service = ServiceBusService(
    #         service_namespace='sb-test',
    #         shared_access_key_name='ordersniff',
    #         shared_access_key_value='FJGJ6dVsg4eaTMJt1eBMOTi2TSCBy42TRQ+dTaMpUII=',
    #         host_base=".servicebus.chinacloudapi.cn"
    #     )

    def __init__(self):
        self.bus_service = ServiceBusService(
            service_namespace='sb-test',
            shared_access_key_name='adsniff',
            shared_access_key_value='wrUBhluj4k1Nw2L/RVK+GYQg7H1qiwFLCXFpkFsbwnI=',
            host_base=".servicebus.chinacloudapi.cn"
        )

    def send_msg(self):
        msg = "abc"
        # self.bus_service.send_topic_message('odersniff', msg)
        self.bus_service.send_topic_message('adsniff', msg)


start = time.time()
SendReceiveMsg().send_msg()
end = time.time()
print end - start
