#!/usr/bin/python
# encoding:utf-8
import datetime
import os
import pickle
import random
import traceback
from multiprocessing import Process

# from _pickle import UnpicklingError
from azure.servicebus import ServiceBusService
from azure.storage.blob import BlockBlobService

# blob Name key container
ACCOUNTNAME = "wifiblob"
ACCOUNTKEY = "7n70mokuZQLKAz1OfD/2UfPAvyZsODWndDcFdDag0LJITEGETZLKaRKKY55lmygaGdG/xMAiqj35O27XQ79s7g=="
CONTAINER = "wifiblob-container"


class WriteBlob():
    def __init__(self, account_name, account_key):
        """
        初始化连接blob
        :param account_name: 连接blob账号
        :param account_key: 连接blob密匙
        """
        self.block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key,
                                                   endpoint_suffix="core.chinacloudapi.cn")

    def startProcessing(self, container, data, sheet_title, sheet_content, ax_name, thread_name):
        """
        1、blob新增探针数据csv文件，按照数据日期设置文件名称
        2、如果传入数据日期，对应在blob里有相应文件则追加数据
        :param container: blob容器名称
        :param data: 探针数据
        :return: 返回是否添加数据成功，成功为True,失败为False
        """
        # 列出所有blob
        re_data = False
        try:
            if data.get("time", False):
                # 创建文件夹
                current_path = os.getcwd()  # 获得当前目录地址
                file_path = os.path.join(current_path, ax_name)  # 添加需要创建的目录名称
                if not os.path.exists(file_path):  # 判断目录是否存在
                    os.mkdir(file_path)  # 不存在创建
                date_time = data.get("time").split(" ")
                time_hour = date_time[1].split(":")[0]  # 获得时间小时
                file_name = date_time[0] + "-" + time_hour + "_" + thread_name + ".csv"
                file_full_name = os.path.join(file_path, file_name)
                if os.path.exists(file_full_name):
                    file = open(file_full_name, 'a')
                    file_data = sheet_content
                    file.write(file_data)
                    file.close()
                    re_data = True
                else:
                    file = open(file_full_name, 'w')
                    new_write_data = sheet_content
                    file.write(new_write_data)
                    file.close()
                    wifilog.write_log(
                        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "创建" + file_name)
                    re_data = True
                    for file in os.listdir(file_path):  # 检索当前文件夹文件
                        if file != file_name:  # 判断文件是否是当前写入的文件，如果不是就上传
                            if file.split("_")[1] == thread_name + ".csv":  # 判断文件是否是本线程的文件，如果是上传
                                generator = self.block_blob_service.list_blobs(container)
                                file_to_blob_name = file
                                for blob in generator:
                                    if blob.name == file:
                                        file_to_blob_name = str(random.randint(1, 1000)) + "-" + file
                                        os.rename(os.path.join(file_path, file),
                                                  os.path.join(file_path, file_to_blob_name))
                                a = self.block_blob_service.create_blob_from_path(container, file_to_blob_name,
                                                                                  os.path.join(file_path,
                                                                                               file_to_blob_name))
                                wifilog.write_log(
                                    str(datetime.datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S")) + "上传" + file_to_blob_name)
                                os.remove(os.path.join(file_path, file_to_blob_name))
                                wifilog.write_log(
                                    str(datetime.datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S")) + "删除本地" + file_to_blob_name)
            return re_data
        except Exception, e:
            wifilog.write_log(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " " + traceback.format_exc())
        return re_data


class ReceiveMsg():
    """
    接收消息队列消息
    """

    def __init__(self):
        # 初始连接listen
        self.bus_service = ServiceBusService(
            service_namespace='sb-test',
            shared_access_key_name='WifiSniffListen',
            shared_access_key_value='VzWU2ayXdk/Q8cqJGcaXbTnUkqYvbsah79FbqGhiR3I=',
            host_base=".servicebus.chinacloudapi.cn"
        )

    def recevie_msg(self, write_blob, thread_name):
        """
        接收消息队列消息，并将消息写入blob，成功写入的消息从消息队列删除
        :param write_blob: blob连接对象
        :return:
        """
        msg = self.bus_service.receive_subscription_message('wifisniff', 'wifisub', peek_lock=False)
        if msg.body is not None:
            try:
                file_data = pickle.loads(msg.body)
                if isinstance(file_data, list):
                    for data in file_data:
                        sheet_title = "shop_id,mac,time" + '\n'
                        sheet_content = str(data.get("shop_id", "0")) + "," + str(data.get("mac", "0")) + "," + str(
                            data.get("time", "0")) + '\n'
                        write_blob.startProcessing(CONTAINER, data, sheet_title, sheet_content, "wifi",
                                                   thread_name)
                else:
                    sheet_title = "shop_id,mac,time" + '\n'
                    sheet_content = str(file_data.get("shop_id", "0")) + "," + str(
                        file_data.get("mac", "0")) + "," + str(
                        file_data.get("time", "0")) + '\n'
                    write_blob.startProcessing(CONTAINER, file_data, sheet_title, sheet_content, "wifi", thread_name)
            except Exception as e:
                wifilog.write_log(
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "-main-" + traceback.format_exc())


class wifilog():
    @classmethod
    def write_log(self, log_msg):
        """
        将错误日志写到日志文件
        :param log_msg: 错误信息
        :return: 无
        """
        with open("wifi_log.log", 'a') as log_file:
            log_file.write(log_msg)


def fac(thread_name):
    try:
        recevie = ReceiveMsg()
        write_blob = WriteBlob(ACCOUNTNAME, ACCOUNTKEY)
        while True:
            recevie.recevie_msg(write_blob, thread_name)
    except Exception as e:
        wifilog.write_log(
            str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "-main-" + traceback.format_exc())
    return fac(thread_name)


if __name__ == '__main__':
    # 创建两个线程
    try:
        t1 = Process(target=fac, args=("Thread-1",))
        t2 = Process(target=fac, args=("Thread-2",))
        t3 = Process(target=fac, args=("Thread-3",))
        t4 = Process(target=fac, args=("Thread-4",))
        t5 = Process(target=fac, args=("Thread-5",))
        t6 = Process(target=fac, args=("Thread-6",))
        t7 = Process(target=fac, args=("Thread-7",))
        t8 = Process(target=fac, args=("Thread-8",))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        t8.start()
    except:
        wifilog.write_log(
            str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "-main-" + traceback.format_exc())
