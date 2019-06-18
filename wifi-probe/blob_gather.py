#!/usr/bin/python
# encoding:utf-8
import os
import sys
import traceback
import zipfile

import pandas as pd
from azure.storage.blob import BlockBlobService
import datetime
import ConfigParser

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class EtlWifiBlob(object):
    def __init__(self):
        """
        初始化连接blob
        """
        self.conf = ConfigParser.ConfigParser()
        self.conf.read("./config.conf")
        self.container = self.conf.get("test_blob", "container")
        self.block_blob_service = BlockBlobService(account_name=self.conf.get("test_blob", "account_name"),
                                                   account_key=self.conf.get("test_blob", "account_key"),
                                                   endpoint_suffix=self.conf.get("test_blob", "endpoint_suffix"))

    def download_blob(self, dfm):
        """
        下载blob数据
        :param dfm:指定日期
        :return:
        """
        # 获取指定日期的所有blob数据
        try:
            generator = self.block_blob_service.list_blobs(self.container)
            for blob in generator:
                if dfm in str(blob.name) and 'zip' not in str(blob.name):
                    # 将数据拷贝到本地
                    full_path_to_file2 = os.path.join("./data/{}".format(blob.name))
                    self.block_blob_service.get_blob_to_path(self.container, blob.name, full_path_to_file2)
        except Exception, e:
            traceback.format_exc(e)

    def delete_blob(self, date):
        """
        删除前四天的blob数据  14号删除10号数据
        :param date: 指定日期
        :return:
        """
        generator = self.block_blob_service.list_blobs(self.container)
        for blob in generator:
            # 获取指定日期的所有数据
            if date in str(blob.name):
                self.block_blob_service.delete_blob(self.container, blob.name)

    def zip_write_blob(self, date, file_path='./daily'):
        """
        将本地文件压缩后上传
        :param date: 指定日期
        :param file_path: 本地文件
        :return:
        """
        file_list = []
        zip = ''
        for filename in os.listdir(file_path):
            if date in str(filename):
                if "zip" not in str(filename):  # 判断是否有zip文件,避免压缩死循环
                    filename = os.path.join(file_path, filename)
                    file_list.append(str(filename))
        try:
            zip = zipfile.ZipFile(os.path.join(file_path, date) + ".zip", 'w')
            for file in file_list:
                zip.write(file, compress_type=zipfile.ZIP_DEFLATED)
        except Exception, e:
            print traceback.format_exc(e)
        finally:
            zip.close()

        try:
            flag = False
            file_to_blob_name = date + ".zip"
            generator = self.block_blob_service.list_blobs(self.container)
            for blob in generator:
                if str(blob.name) == str(file_to_blob_name):
                    flag = True
                    break
            if not flag:
                self.block_blob_service.create_blob_from_path(
                    self.container, file_to_blob_name, os.path.join(file_path, file_to_blob_name))
        except Exception, e:
            print traceback.format_exc(e)


class LocalFileEtl(object):
    """
    本地文件处理
    """

    def __init__(self):
        self.data_dir = './data'
        self.result_dir = './result'
        self.daily_dir = './daily'

    def __fmt_msg(self, dfm):
        """
        合并文件的一个内部方法
        :param dfm:
        :return:
        """
        # 将指定日期的数据合并在一个每小时文件
        files = []
        for filename in os.listdir(self.data_dir):
            if dfm in str(filename):  # 当前路径下所有非目录子文件
                files.append(pd.read_csv("{}/{}".format(self.data_dir, filename),
                                         delimiter=',', names=["shop_id", 'mac', 'time']))
        df = pd.concat(files).sort_values(by=['shop_id', 'mac', 'time'])  # 合并blob文件

        # 数据标准格式化
        shop_id = list()  # 店铺ID
        cus_mac = list()  # 顾客mac
        sen_mac = list()  # 第二个mac
        frame_big = list()  # Frame大类
        frame_little = list()  # Frame小类
        channel = list()  # 信道
        intensity = list()  # 型号强度
        times = list()  # 探针返回的时间
        for i, _ in enumerate(df.values):
            cus_mac_id = str(df.mac.values[i]).split('|')[0]
            sen_mac_id = str(df.mac.values[i]).split('|')[1]
            if len(cus_mac_id) == 17 and len(sen_mac_id) == 17 and len(df.mac.values[i].split('|')) == 6:
                # print str((df.mac.values[i].split('|')[4] if df.mac.values[i].split('|')[4] else 0))
                shop_id.append((df.shop_id.values[i] if df.shop_id.values[i] else 0))
                cus_mac.append(cus_mac_id)
                sen_mac.append(sen_mac_id)
                frame_big.append(str(df.mac.values[i].split('|')[2] if df.mac.values[i].split('|')[2] else 0))
                frame_little.append(str(df.mac.values[i].split('|')[3] if df.mac.values[i].split('|')[3] else 0))
                channel.append(str(df.mac.values[i].split('|')[4] if df.mac.values[i].split('|')[4] else 0))
                intensity.append(str(df.mac.values[i].split('|')[5] if df.mac.values[i].split('|')[5] else 0))
                times.append(df.time.values[i])

        df = pd.DataFrame(
            {'cus_mac': cus_mac, 'shop_id': shop_id, 'intensity': intensity, 'time': times,
             'sen_mac': sen_mac, 'frame_big': frame_big, 'frame_little': frame_little, 'channel': channel})
        columns = ['shop_id', 'cus_mac', 'sen_mac', 'frame_big', 'frame_little', 'channel', 'intensity', 'time']
        df = df.sort_values(by=['shop_id', 'cus_mac', 'time'])
        df = df.drop_duplicates(subset=['shop_id', 'cus_mac', 'time'], keep='last')  # 去除重复项

        df.to_csv('{}/{}.csv'.format(self.result_dir, dfm), index=False, sep=',', columns=columns)

        # 将合并后的本地初始文件删除
        for filename in os.listdir(self.data_dir):
            if dfm in str(filename):
                # print filename
                os.remove(os.path.join(self.data_dir, filename))

    def mer_msg(self, date):
        for i in range(24):
            try:
                if i <= 9:
                    self.__fmt_msg(date + "-0{0}".format(i))
                elif 9 < i <= 19:
                    self.__fmt_msg(date + "-{0}".format(i))
                else:
                    self.__fmt_msg(date + "-{0}".format(i))
            except Exception, e:
                print e

    def mer_daily_data(self, dfm):
        """
        合并今天所有时间的数据成一个文件
        :param dfm: 指定日期
        :return:
        """
        files = []
        for filename in os.listdir(self.result_dir):
            if dfm in str(filename) and 'zip' not in str(filename):
                # print filename  # 当前路径下所有非目录子文件
                files.append(
                    pd.read_csv("{}/{}".format(self.result_dir, filename),  # header=0 这个参数在合并的时候去掉表头
                                delimiter=',', header=0,
                                names=["shop_id", 'cus_mac', 'sen_mac', 'frame_big', 'frame_little', 'channel',
                                       'intensity', 'time']))

        df = pd.concat(files)
        df = df.drop_duplicates()  # 去除重复项
        columns = ['shop_id', 'cus_mac', 'sen_mac', 'frame_big', 'frame_little', 'channel', 'intensity', 'time']
        df = df.sort_values(by=['shop_id', 'cus_mac', 'time'])
        df.to_csv('{}/{}.csv'.format(self.daily_dir, dfm), index=False, sep=',', encoding="utf_8", columns=columns)


if __name__ == '__main__':
    today = datetime.date.today()
    one_day = datetime.timedelta(days=3)
    four_days = datetime.timedelta(days=6)
    yesterday = str(today - one_day)
    four_days = str(today - four_days)

    etl_wifi_blob = EtlWifiBlob()
    local_file_blob = LocalFileEtl()
    # 下载blob
    # etl_wifi_blob.download_blob(yesterday)
    # 删除blob
    etl_wifi_blob.delete_blob(four_days)
    # 合并文件成小时文件
    # local_file_blob.mer_msg(yesterday)
    # # 合并文件成一天一个大文件
    # local_file_blob.mer_daily_data(yesterday)
    # # 上传本地压缩文件到blob
    # etl_wifi_blob.zip_write_blob(yesterday)
