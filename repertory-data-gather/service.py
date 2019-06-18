# coding:utf8
import datetime

import common
import sys
from logger import Logger
from connect_mysql import ConnectMysql

__author__ = 'WuKai'
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
_logger = Logger("service.py")


def query_repertory():
    """
    查询条码信息, from barcode总表
    :return: all barcode list
    """
    all_repertories = []
    try:
        conn_mysql_repertory = common.conn_mysql_repertory
        last_update_repertory = common.get_last_update_repertory()
        select_mysql = ConnectMysql(conn_mysql_repertory)
        sql = "SELECT id, shop_id, code, product_name, in_price, selling_price, quantity, physics_quantity, " \
              "loss, warning_stock, stock_date, warehouse_id, reserved_qty " \
              "FROM repertory WHERE stock_date > '" + last_update_repertory + "' order by stock_date limit 1000"
        result = select_mysql.select(sql)
        for single_repertory_info in result:
            single_repertory_info_dict = dict()

            single_repertory_info_dict['id'] = (single_repertory_info[0] if single_repertory_info[0] else 0)
            single_repertory_info_dict['shop_id'] = (single_repertory_info[1] if single_repertory_info[1] else 0)
            single_repertory_info_dict['code'] = (single_repertory_info[2] if single_repertory_info[2] else '')
            single_repertory_info_dict['product_name'] = (single_repertory_info[3] if single_repertory_info[3] else '')
            single_repertory_info_dict['in_price'] = (single_repertory_info[4] if single_repertory_info[4] else 0.0)
            single_repertory_info_dict['selling_price'] = (
                single_repertory_info[5] if single_repertory_info[5] else 0.0)
            single_repertory_info_dict['quantity'] = (single_repertory_info[6] if single_repertory_info[6] else 0.0)
            single_repertory_info_dict['physics_quantity'] = (
                single_repertory_info[7] if single_repertory_info[7] else 0.0)
            single_repertory_info_dict['loss'] = (single_repertory_info[8] if single_repertory_info[8] else 0.0)
            single_repertory_info_dict['warning_stock'] = (single_repertory_info[9] if single_repertory_info[9] else 0)
            single_repertory_info_dict['stock_date'] = (single_repertory_info[10] if single_repertory_info[10] else
                                                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            single_repertory_info_dict['warehouse_id'] = (single_repertory_info[11] if single_repertory_info[11] else 0)
            single_repertory_info_dict['reserved_qty'] = (
                single_repertory_info[12] if single_repertory_info[12] else 0.0)

            all_repertories.append(single_repertory_info_dict)

        _logger.info("查询repertory信息成功, id: " + last_update_repertory +
                     "开始, 查询出: " + str(len(all_repertories)) + "条库存信息.")

        # select_mysql.close()
    except Exception, e:
        _logger.error(e)
    return all_repertories


def insert_repertory_dw(all_repertories):
    conn_mysql_dw = common.conn_mysql_datawarehouse
    insert_mysql = ConnectMysql(conn_mysql_dw)
    count = 0
    max_last_update = ''
    last_run_update = ''
    if all_repertories is not None:
        try:
            for single_repertories_info_dict in all_repertories:
                id = single_repertories_info_dict['id']
                shop_id = single_repertories_info_dict['shop_id'] if \
                    single_repertories_info_dict['shop_id'] else 0
                code = single_repertories_info_dict['code'].replace("'", "").replace("\\", "") if \
                    single_repertories_info_dict['code'] else ''
                product_name = single_repertories_info_dict['product_name'].replace("'", "").replace("\\", "") if \
                    single_repertories_info_dict['product_name'] else ''
                in_price = single_repertories_info_dict['in_price'] if \
                    single_repertories_info_dict['in_price'] else 0.0
                selling_price = single_repertories_info_dict['selling_price'] if \
                    single_repertories_info_dict['selling_price'] else 0.0
                quantity = single_repertories_info_dict['quantity'] if \
                    single_repertories_info_dict['quantity'] else 0.0
                physics_quantity = single_repertories_info_dict['physics_quantity'] if \
                    single_repertories_info_dict['physics_quantity'] else 0.0
                loss = single_repertories_info_dict['loss'] if \
                    single_repertories_info_dict['loss'] else 0.0
                warning_stock = single_repertories_info_dict['warning_stock'] if \
                    single_repertories_info_dict['warning_stock'] else 0
                stock_date = single_repertories_info_dict['stock_date'] if \
                    single_repertories_info_dict['stock_date'] else datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")
                warehouse_id = single_repertories_info_dict['warehouse_id'] if \
                    single_repertories_info_dict['warehouse_id'] else 0
                reserved_qty = single_repertories_info_dict['reserved_qty'] if \
                    single_repertories_info_dict['reserved_qty'] else 0.0

                if str(stock_date) > max_last_update:
                    max_last_update = str(stock_date)

                sql = "REPLACE INTO `repertory`(id, shop_id, code, product_name, in_price, selling_price, quantity, " \
                      "physics_quantity, loss, warning_stock, stock_date, warehouse_id, reserved_qty) VALUES({},{},'{}'," \
                      "'{}',{},{},{},{},{},{},'{}',{},{})".format(id, shop_id, code, product_name, in_price,
                                                                  selling_price,
                                                                  quantity, physics_quantity,
                                                                  loss, warning_stock, stock_date, warehouse_id,
                                                                  reserved_qty)
                insert_mysql.query(sql)
                count += 1
                _logger.info(str(count) + ", 插入一条repertory信息到数据仓库, id: " + str(id) + ", name: " + product_name)
                last_run_update = stock_date
        except Exception, e:
            _logger.error("准备数据并插入数据到数据仓库出错(barcode) "
                          "写入上一条执行的最后更新id到缓存中:  " + str(last_run_update))
            _logger.exception(str(e))
            common.write_last_update_repertory(last_run_update)
            return False
        common.write_last_update_repertory(max_last_update)
        return True
    else:
        return False
