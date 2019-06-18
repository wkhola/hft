#!/usr/bin/python
# encoding:utf-8
import time
from azure.servicebus import ServiceBusService, Message


class SendReceiveMsg(object):
    def __init__(self):
        self.bus_service = ServiceBusService(
            service_namespace='sb-test',
            shared_access_key_name='RepertorySniffSend',
            shared_access_key_value='h64zPhep/+8Aocl9DM+sm7AtkzzTDbzIqHW65iGIul0=',
            host_base=".servicebus.chinacloudapi.cn"
        )

    # def __init__(self):
    #     self.bus_service = ServiceBusService(
    #         service_namespace='sb-test',
    #         shared_access_key_name='adsniff',
    #         shared_access_key_value='wrUBhluj4k1Nw2L/RVK+GYQg7H1qiwFLCXFpkFsbwnI=',
    #         host_base=".servicebus.chinacloudapi.cn"
    #     )

    def send_msg(self):
        for i in range(10):
            if i % 2:
                msg = Message('Msg {0}'.format(i).encode('utf-8'), custom_properties={'num': '1'})
            else:
                msg = Message('Msg {0}'.format(i).encode('utf-8'), custom_properties={'num': '2'})
            self.bus_service.send_topic_message('repertorysniff', msg)
            # self.bus_service.send_topic_message('adsniff', msg)


start = time.time()
SendReceiveMsg().send_msg()
end = time.time()
print end - start
