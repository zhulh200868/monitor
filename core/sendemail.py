#!/usr/local/python2.7/bin/python
# -*- coding=utf-8 -*-

import json,time,os
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header
import logger

def s_email(host,service,name,num):
    try:
        subject = "zhejiang alter"
        if num == '1':    	
        	content = "On %s ,the %s's %s is Waring!" %(host,service,name) 
        elif num == '2':
    		content = "On %s ,the %s's %s is Critical!" %(host,service,name) 
        elif num == '3':
    		content = "On %s ,the %s's %s is OK!" %(host,service,name) 
        msg = MIMEText(_text=content, _charset='utf-8')
        msg['Subject'] = Header(subject, 'utf-8') 
        #输入Email地址和口令:
        from_addr = 'monitor@v-dream.com'
        password = 'wocaonima!'
        # 输入SMTP服务器地址:
        smtp_server = 'smtp.v-dream.com'
        # 输入收件人地址:
        to_addr = ['zlh10@163.com']
     
        #SMTP协议默认端口是25
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        for i in to_addr:
            server.sendmail(from_addr, i, msg.as_string())
        server.quit()
        print 'email send success,the address is %s' %to_addr
    except Exception,e:
        print e
        print 'email send failed.'  