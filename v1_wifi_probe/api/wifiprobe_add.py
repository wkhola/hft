#!/usr/bin/python
# encoding:utf-8
# -*- coding: utf-8 -*-

from flask import current_app, g

from . import Resource
import time
import traceback, pickle
from .send_msg import SendReceiveMsg
from datetime import datetime
import sys


class WifiprobeAdd(Resource):
    @property
    def post(self):
        try:
            mac_addr = g.json
            shop_id = g.args['shop_id']
            send_receive = SendReceiveMsg()
            put_data = []
            data_size = sys.getsizeof(mac_addr) / 1024
            if data_size <= 250:
                for mac in mac_addr:
                    in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    try:
                        v_time = time.strptime(mac.get("time", "0"), "%Y-%m-%d %H:%M:%S")
                        if 3600 >= (time.time() - time.mktime(v_time)) >= 0:
                            in_time = mac.get("time")
                    except Exception as e:
                        pass
                    put_data.append({"shop_id": shop_id, "mac": mac['mac'], "time": in_time})
                send_receive.send_msg(pickle.dumps(put_data))
            else:
                v_size = (data_size // 250) + 1
                single_size = (len(mac_addr) - 1) // v_size
                for index, mac in enumerate(mac_addr):
                    in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    try:
                        v_time = time.strptime(mac.get("time", "0"), "%Y-%m-%d %H:%M:%S")
                        if 3600 >= (time.time() - time.mktime(v_time)) >= 0:
                            in_time = mac.get("time")
                    except Exception as e:
                        pass
                    put_data.append(
                        {"shop_id": shop_id, "mac": mac['mac'], "time": in_time})
                    if index == single_size:
                        send_receive.send_msg(pickle.dumps(put_data))
                        put_data = []
                        single_size += index
                    elif index == len(mac_addr) - 1:
                        send_receive.send_msg(pickle.dumps(put_data))
            return {"message": "successful"}, 200, None
        except Exception as e:
            pass
        return None, 500, None
