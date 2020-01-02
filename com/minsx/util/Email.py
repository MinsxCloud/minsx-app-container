#! /usr/bin/python
# -*- coding:utf-8 -*-
# Author: Joker
# Copyright (c) 2018 OpenString. All rights reserved.
import smtplib
import datetime
from email.utils import formataddr
from email.mime.text import MIMEText
from email.header import Header
from com.minsx.pycontainer import ConfigManager

emailConfig = ConfigManager.getSoftConfig().get('Email')


def sendEmail(receivedEmail, title, content):
    text = MIMEText(content, 'plain', 'utf-8')
    # text['From'] = Header(emailConfig.get('emailUser'), 'utf-8')
    # text['To'] = Header(emailConfig.get('receivedEmail'), 'utf-8')
    text['From'] = formataddr(["放疗云", emailConfig.get('EmailUser')])
    text['To'] = formataddr(["放疗云", receivedEmail])
    text['Subject'] = Header(title, 'utf-8')
    result = {"isSuccess": False, "reason": None}
    try:
        server = smtplib.SMTP_SSL(emailConfig.get('EmailHost'), 465)
        server.login(emailConfig.get('EmailUser'), emailConfig.get('EmailPass'))
        server.sendmail(emailConfig.get('EmailUser'), emailConfig.get('ReceivedEmail'), text.as_string())
        server.close()
        result['isSuccess'] = True
    except Exception as e:
        reason = "send email catch error: {e}".format(e=e)
        print(reason)
        result['reason'] = reason
    return result


def sendAdviceEmail(error):
    if emailConfig.get('Enable'):
        server = emailConfig.get('ServerName')
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        template = '服务名称: {s}\n通知内容: {e}\n发生时间: {t}\n'
        content = template.format(s=server, e=error, t=time)
        receivedEmails = emailConfig.get('ReceivedEmail')
        for receivedEmail in receivedEmails:
            sendEmail(receivedEmail, '放疗云通知', content)
