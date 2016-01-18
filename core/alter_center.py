#!/usr/local/python2.7/bin/python
# -*- coding=utf-8 -*-

import global_setting
#from conf import hosts_init
import redis_connector as redis
import json,time
import logger
import py_mysql
import urllib2



#critical列表
critical_list = []
#已经发过邮件的critical列表
C_list = []
#恢复的列表
well_list = []
#已经发过邮件的well列表
G_list = []
host_name = {}
def alter_center():
	#py_mysql.W_mysql('insert into test values(1);')
	critical_list = json.loads(redis.r['critical::list'])
	well_list = json.loads(redis.r.get('well::list'))
	#判断是否需要发critical的邮件
	if len(redis.r.get('critical::list')) > 2 :
		for i in list(set(critical_list).difference(set(C_list))):
			#print 'i===',i
			host,service,name= i.split(':')
			logger.record_log(host,service,name,'Critical')
			'''
			#sendemail.s_email(host,service,name,'2')
			'''
			C_list.append(i)
			times = time.strftime("%Y%m%d%H%M%S",time.localtime())
			#cmd = 'insert into web_monitor_critical (hostname,service_name,time) values(' +"'"+host+"',"+"'"+service+"',"+"'"+times+"');"
			service_name = service+':'+name
			num = 'C'
			py_mysql.W_mysql(host,service_name,times,num)
			if i in G_list:
				G_list.remove(i)
	#判断是否需要发well的邮件
	if len(redis.r.get('well::list')) > 2 :
		for i in list(set(well_list).difference(set(G_list))):
			host,service,name= i.split(':')
			logger.record_log(host,service,name,'OK')
			'''
			#sendemail.s_email(host,service,name,'3')
			'''
			G_list.append(i)
			#将critical数据插入mysql的well表中
			times = time.strftime("%Y%m%d%H%M%S",time.localtime())
			service_name = service+':'+name
			num = 'W'
			py_mysql.W_mysql(host,service_name,times,num)
			if i in C_list:
				C_list.remove(i)
	

	
	redis.r['f_critical::list'] = json.dumps(C_list)
	redis.r['f_well::list'] = json.dumps(G_list)
	print '=============================================='
	print 'critical_list===>',critical_list
	print 'well_list===>',well_list
	print 'C_list===>',C_list
	print 'G_list===>',G_list

'''
def TO_mysql(sql_cmd,num):
	try:
		conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='s6monitor2',unix_socket='/tmp/mysql_3308.sock',port=3308)
		cur = conn.cursor()
		cur.execute(sql_cmd)
		if num == 1:  
			res = cur.fetchall()		   
			for line in res:
				num = str(line[0]).strip('L')
				host_name[num] = line[1]
		cur.close()
		conn.close()
		return host_name
	except MySQLdb.Error,e:
		print 'Mysql Error Msg:',e
'''
			
if __name__ == '__main__':	
	counter = 0
	if 'f_critical::list' not in redis.r.keys():
		redis.r['f_critical::list'] = []	
	else:
		C_list = json.loads(redis.r.get('f_critical::list'))
	if 'f_well::list' not in redis.r.keys():
		redis.r['f_well::list'] = []	
	else:
		G_list = json.loads(redis.r.get('f_well::list'))

	while True:
		try:
			if counter > 10:
				host_name = py_mysql.S_mysql('SELECT id,hostname FROM web_host',num=1)
				for host_id in host_name.keys():
					#url_str = "http://10.73.143.203:9000/api/configuration/"+host_id+"/?format=json"
					url_str = "http://192.168.2.100:9000/api/configuration/"+host_id+"/?format=json"
					req = urllib2.urlopen(url_str)
					result = req.read()
					configs= json.loads(result)
					#在下面的for循环中如果status_monitor_on为false的话，将不会监控
					if configs is not None:
						if configs.get('status_monitor_on') is True:
							pass
						else:
							for i in C_list:
								if i.find(host_name[host_id]) != -1:
									keys = host_name[host_id]+i[len(host_name[host_id]):len(i)]
									#critical_list.remove(keys)
									#for remove the keys in C_list
									C_list.remove(keys)
									#for delete the keys in mysql
									service_name = keys.split(':')[1]+':'+keys.split(':')[2]
									host = str(keys.split(':')[0])
									num = 'W'
									times = time.strftime("%Y%m%d%H%M%S",time.localtime())
									py_mysql.W_mysql(host,service_name,times,num)
							for k in G_list:
								if k.find(host_name[host_id]) != -1:
									keys = host_name[host_id]+k[len(host_name[host_id]):len(k)]
									#well_list.remove(keys)
									#for remove the keys in C_list
									G_list.remove(keys)
									#for delete the keys in mysql
									service_name = keys.split(':')[1]+':'+keys.split(':')[2]
									host = str(keys.split(':')[0])
									num = 'W'
									times = time.strftime("%Y%m%d%H%M%S",time.localtime())
									py_mysql.W_mysql(host,service_name,times,num)
					else:
						pass				
			counter = 0
							
			alter_center()
			time.sleep(5)
			counter +=1
		except urllib2.URLError,e:
			print 'URLError Error Msg:',e


