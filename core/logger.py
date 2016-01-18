#!/usr/local/python2.7/bin/python
# -*- coding=utf-8 -*-

import time,os
import shutil
#pwds = os.getcwd()
#logfile = '%s/monitor.log' % pwds

pwds = os.getcwd()[:-(len(os.getcwd().split('/')[-1]) + 1)]


def record_log(host,service,name,states):
	if os.path.exists('%s/var' %pwds):
		logfile = '%s/var/monitor.log' % pwds
	else:
		os.makedirs('%s/var' %pwds)
		logfile = '%s/var/monitor.log' % pwds
	date = time.strftime("%Y%m%d%H%M%S",time.localtime())
	f_host = host
	f_service = service
	f_name = name
	f_states = states
	record_line = "["+ date +"] CURRENT SERVICE STATE: zhejiang;On "+ f_host +" ,the "+ f_service +"'s " + f_name +" is " + f_states +" !" +"\n"
	f = file(logfile,'a+')
	f.write(record_line)
	f.flush()
	f.close()

def mail_log():
	date = time.strftime("%Y%m%d%H%M%S",time.localtime())
	
def change_logfile():
	today = int(time.strftime("%Y%m%d%H%M%S",time.localtime())[0:8])
	yestoday = today - 1
	hour = (time.strftime("%Y%m%d%H%M%S",time.localtime()))[8:10]
	logfile = '%s/var/monitor.log' % pwds
	if hour == '00':
		if os.path.exists('%s/var/monitor.log.bak%s' %(pwds,yestoday)):
			pass
		else:
			shutil.move(logfile,'%s/var/monitor.log.bak%s' % (pwds,yestoday))
	else:
		pass

