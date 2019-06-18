#!/usr/bin/python
# encoding:utf-8
from azure.servicebus import ServiceBusService, Message


class SendReceiveMsg():
    def __init__(self):
        self.bus_service = ServiceBusService(
            service_namespace='sb-test',
            shared_access_key_name='WifiSniffSend',
            shared_access_key_value='23SmfgRdqHHTn7o38hG1wLDYskIF3T+DL29g54W/fhE=',
            host_base=".servicebus.chinacloudapi.cn"
        )

    def send_msg(self, data):
        msg = Message(data)
        self.bus_service.send_topic_message('wifisniff', msg)
