#!/usr/bin/python
# encoding:utf-8
# import pandas as pd
import sys
import common
import mail

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

conn = common.conn_pg
con = common.conn_mysql

recipients_str = common.conf.get('common', 'recipients')
recipients = list()
for event in recipients_str.split(','):
    recipients.append(event)


def pos_version():
    sql = """
    SELECT "launcher_versionName" as version, count(*) as counts from shop_pos_app_version
    group by "launcher_versionName"
    """
    sql = "select id, name from store where categ='normal'"
    # result = pd.read_sql(sql, conn)
    cursor = con.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    message = '<html><body>'
    message += '<table border="1" cellspacing="1" cellpadding="1" style="display: inline-block; vertical-align:top; ' \
               'margin:10px 10px"><caption>店铺pos机版本使用情况</caption>' \
               '<tr><td>版本号</td><td>店铺数</td></tr>'
    for r in result:
        # version = str(r[1])
        version = r[0]
        counts = r[1]
        message += '<tr><td>' + str(version) + '</td><td>' + counts + '</td></tr>'
        # print version, counts

    message += '</table>'
    message += '</body></html>'
    return message


def send():
    message = pos_version()
    mail.send_mail(u"店铺pos机版本使用情况", message, recipients)


send()
