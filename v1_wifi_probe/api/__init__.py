# -*- coding: utf-8 -*-
import boto3
import sys
# s3 = boto3.resource('s3')
# file_obj = s3.Bucket("hft-data-service").delete_objects(
#     Delete={'Objects': [{'Key': "HFT_DATA_SERVICE_TEST/wifi_probe_new/send_msg.py"}]})
# # print file_obj
# s3.Object("hft-data-service", "HFT_DATA_SERVICE_TEST/wifi_probe_new/send_msg.py").upload_file("send_msg.py")
# s3.Object("hft-data-service", "HFT_DATA_SERVICE_TEST/wifi_probe_new/send_msg.py").delete_objects("send_msg.py")

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

while True:
    print raw_input().strip(u"吗？")