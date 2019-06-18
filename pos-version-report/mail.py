# coding:utf8

import smtplib
import datetime as dt
from email.mime.multipart import MIMEMultipart  # 导入MIMEMultipart类
from email.mime.text import MIMEText  # 导入MIMEText类
from logger import Logger

__author__ = 'CaoYu'
logger = Logger('mail.py')


def send_mail(subject, mail_message, recipients):
    """
    发送邮件方法
    :param subject:     邮件主题
    :param mail_message:    邮件主题内容html代码
    :param recipients:      收件人list数组
    :return:    None
    """
    host = "smtp.exmail.qq.com"  # 定义smtp主机
    mail_from = "no.reply@esmart365.com"  # 定义邮件发件人

    msg_root = MIMEMultipart('mixed')  # 创建MIMEMultipart对象,如果邮件中含有附件，那邮件的Content-Type域定义mixed类型
    msg_text = MIMEText(mail_message, "html", "utf-8")  # <img>标签的src属性是通过Content-ID来引用的
    msg_root.attach(msg_text)  # MIMEMultipart对象附加MIMEText的内容
    msg_root['Subject'] = subject  # 邮件主题
    msg_root['From'] = mail_from  # 邮件发件人,邮件头部可见
    msg_root['To'] = ','.join(recipients)
    # msg_root['To'] = recipients

    try:
        server = smtplib.SMTP()  # 创建一个SMTP()对象
        server.connect(host, "25")  # 通过connect方法连接smtp主机
        server.starttls()  # 启动安全传输模式
        server.login("no.reply@esmart365.com", "dF7afHrQChf2mk4A")  # 邮箱账号登录校验
        server.sendmail(mail_from, recipients, msg_root.as_string())  # 邮件发送
        server.quit()  # 断开smtp连接
        for to in recipients:
            logger.info(str(dt.datetime.now()) + ("邮件发送成功！" + to))
    except Exception, e:
        logger.error(str(dt.datetime.now()) + ("邮件发送失败：" + str(e) + " 收件人为: " + str(recipients)))
        logger.exception(e)
