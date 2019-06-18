#!/usr/bin/python
# encoding:utf-8
from azure.servicebus import ServiceBusService, Message


class SendReceiveMsg(object):
    def __init__(self):
        self.bus_service = ServiceBusService(
            service_namespace='sb-test',
            shared_access_key_name='RepertorySniffSend',
            shared_access_key_value='h64zPhep/+8Aocl9DM+sm7AtkzzTDbzIqHW65iGIul0=',
            host_base=".servicebus.chinacloudapi.cn"
        )

    def send_data(self, data, name):
        msg = Message(data, custom_properties={'type': name})
        self.bus_service.send_topic_message('repertorysniff', msg)

