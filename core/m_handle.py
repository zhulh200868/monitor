#!/usr/local/python2.7/bin/python
# -*- coding=utf-8 -*-

import redis_connector as redis
import json,time
import urllib2
import MySQLdb


critical_list = []
well_list = []
host_name = {}
well_temp_list = []
critical_temp_list = []
operators = {'1':'gt','2':'lt','3':'eq'}
host_service = {}
def fetch_monitored_list(host_name,start_time):
    '''      
    for host_id in host_name.keys():
        monitor_list = []
        service = {} 
        #url_str = 'http://10.73.143.201:9000/api/configuration/%s/?format=json' %host_id
        #url_str = 'http://10.73.143.201:9000/api/configuration/2/?format=json'
        url_str = "http://192.168.2.100:9000/api/configuration/"+host_id+"/?format=json"
        req = urllib2.urlopen(url_str)
        result = req.read()
        configs= json.loads(result)
        #在下面的for循环中如果status_monitor_on为false的话，将不会监控
        if configs.get('status_monitor_on') is True:
            for template in configs.get('template_list'):
                monitor_list +=template['service_list']
                #graph_list = configs.get('template_list')['graph_list']
                #print graph_list
    '''
    if host_service is not None:                
        for host in host_service.keys():
            service = {}
            monitor_list = []
            monitor_list =  host_service[host]    
            for i in range(len(monitor_list)):
                #print str(monitor_list[i]['conditons'][0]['name']).split('.')[-1]
                #取页面中的监控项名
                #print monitor_list
                key = host+'::'+ str(monitor_list[i]['conditons'][0]['name']).split('.')[-1]
                #print key
                #取redis中的key
                redis_key = host+'::'+monitor_list[i]['service']['name']
                #print redis_key
                #取监控项的阀值
                service[key] = str(monitor_list[i]['conditons'][0]['threshold']).split('.')[-1]
                #取"name":"LinuxTemplate.linux.salt.salt_pg"中salt_pg
                zhulh = str(monitor_list[i]['conditons'][0]['name']).split('.')[-1]
                #取"name":"LinuxTemplate.linux.salt.salt_pg"中salt
                service_name = str(str(monitor_list[i]['conditons'][0]['name']).split('.')[2:-1]).strip("['']")
                #print len(str(monitor_list[i]['conditons'][0]['name']).split('.')),str(monitor_list[i]['conditons'][0]['name']).split('.')[2:-1]
                #取redis中的数据
                service_data = redis.r.get(redis_key)
                print service_data
                #取运算符            
                operators_num = str(monitor_list[i]['conditons'][0]['operator'])
                
                if service_data is not None:
                    service_data = json.loads(service_data)
                    time_pass_since_last_recv = time.time() - float(service_data['time_stamp'])
                    interval = int(monitor_list[i]['check_interval'])
                    new_zhulh = host+':'+service_name+':'+zhulh
                    if time_pass_since_last_recv > 4*interval:
                        print "\033[41;1mService %s has no data for %ss\033[0m" %(new_zhulh,(time_pass_since_last_recv))                       
                        if new_zhulh not in critical_list:
                            critical_list.append(new_zhulh)
                            if new_zhulh in well_list:                                        
                                well_list.remove(new_zhulh)
                        #print critical_list
                        
                    #else:
                        #if time.time() >= interval + float(service_data['time_stamp']) -10: 
                    elif eval(service_data['data'])['status'] == 0:
                        if operators[operators_num] == 'gt':
                            '''
                            #在这里eval是将service_data['data']字符串转换成dict
                            #eval(service_data['data'])[zhulh]
                            '''
                            if float(service[key]) > float(eval(service_data['data'])[zhulh]):
                                print "\033[32;1mService %s crossed OK ,current val is %s\033[0m" %(new_zhulh,eval(service_data['data'])[zhulh])
                                W_to_list(new_zhulh)
    
                            else:
                                print "\033[32;1mService %s crossed Critical ,current val is %s\033[0m" %(new_zhulh,eval(service_data['data'])[zhulh])
                                C_to_list(new_zhulh)
    
                        elif operators[operators_num] == 'lt':
                            if float(service[key]) < float(eval(service_data['data'])[zhulh]):
                                print "\033[32;1mService %s crossed OK ,current val is %s\033[0m" %(new_zhulh,eval(service_data['data'])[zhulh])
                                W_to_list(new_zhulh)
    
                            else:
                                print "\033[32;1mService %s crossed Critical ,current val is %s\033[0m" %(new_zhulh,eval(service_data['data'])[zhulh])
                                C_to_list(new_zhulh)
    
                        elif operators[operators_num] == 'eq':
                            if float(service[key]) == float(eval(service_data['data'])[zhulh]):
                                print "\033[32;1mService %s crossed OK ,current val is %s\033[0m" %(new_zhulh,eval(service_data['data'])[zhulh])
                                W_to_list(new_zhulh)
                            else:
                                print "\033[32;1mService %s crossed Critical ,current val is %s\033[0m" %(new_zhulh,eval(service_data['data'])[zhulh])
                                C_to_list(new_zhulh)
    
                        #print eval(service_data['data'])[zhulh]                        
                        new_service_data = {"service_name": service_data['service_name'], "hostname": service_data['hostname'], "data": "{'status': 1, '%s': '%s'}" %(zhulh,eval(service_data['data'])[zhulh]), "time_stamp": service_data['time_stamp']}
                         
                        #print json.dumps(new_service_data)
                        redis.r[redis_key] = json.dumps(new_service_data)
                        #print 'well_temp_list:',well_temp_list
                        #print 'critical_temp_list:',critical_temp_list
                        new_service = service_name+'_'+zhulh
                        num = eval(service_data['data'])[zhulh]
                        cmd_sql = "insert into web_monitor_meg(hostname,service_name,num,time) values('"+host+"','"+new_service+"','"+num+"','"+ service_data['time_stamp']+"')"
                        #W_mysql(cmd_sql,num=2)
                    else:
                        pass
                else:
                    pass
                '''
        else:
            #清理redis中的数据
            #new_f_critical_list = []
            #new_f_well_list = []
            for i in redis.r.keys():
                if i.find(host_name[host_id]) != -1:
                    keys = host_name[host_id]+i[len(host_name[host_id]):len(i)]
                    redis.r.delete(keys)
            for i in critical_list:
                if i.find(host_name[host_id]) != -1:
                    keys = host_name[host_id]+i[len(host_name[host_id]):len(i)]
                    critical_list.remove(keys)
            for i in well_list:
                if i.find(host_name[host_id]) != -1:
                    keys = host_name[host_id]+i[len(host_name[host_id]):len(i)]
                    well_list.remove(keys)
                '''
            '''
            for i in json.loads(redis.r['f_critical::list']):
                if i.find(host_name[host_id]) == -1:
                    new_f_critical_list.append(i)
            redis.r['f_critical::list'] = json.dumps(new_f_critical_list)
                    #keys = host_name[host_id]+i[len(host_name[host_id]):len(i)]
                    #critical_list.remove(keys)
            for i in json.loads(redis.r['f_well::list']):
                if i.find(host_name[host_id]) == -1:
                    #keys = host_name[host_id]+i[len(host_name[host_id]):len(i)]
                    new_f_well_list.append(i)
            redis.r['f_critical::list'] = json.dumps(new_f_well_list)
            '''
    else:
        pass                      
    redis.r['critical::list'] = json.dumps(critical_list)
    redis.r['well::list'] = json.dumps(well_list)
    print 'The well_list is:','\033[37m%s\033[0m' %well_list
    print 'The critical_list is:','\033[31m%s\033[0m' %critical_list

def W_to_list(new_zhulh):
    
    if new_zhulh in critical_list or new_zhulh not in well_list:
        well_temp_list.append(new_zhulh)
        #if zhulh not in well_list and cross_well_count >= 3:
        if new_zhulh not in well_list and well_temp_list.count(new_zhulh) >= 3:
            for i in range(well_temp_list.count(new_zhulh)):
                well_temp_list.remove(new_zhulh)
            well_list.append(new_zhulh)
            if new_zhulh in critical_list:                                    
                critical_list.remove(new_zhulh)   


def C_to_list(new_zhulh):
    if new_zhulh in critical_list:
        for i in range(critical_temp_list.count(new_zhulh)):
            critical_temp_list.remove(new_zhulh)
    else:
        critical_temp_list.append(new_zhulh)
        if critical_temp_list.count(new_zhulh) >= 3:                                        
            critical_list.append(new_zhulh)
            if new_zhulh in well_list:                                        
                well_list.remove(new_zhulh)

def W_mysql(sql_cmd,num):
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

def fetch_redis_data():
    if 'critical::list' not in redis.r.keys():
        redis.r['critical::list'] = 0
    else:
        if len(redis.r.get('critical::list')) > 2:
            for i in json.loads(redis.r.get('critical::list')):
                zhulh = i.split(':')[0]+':'+i.split(':')[1]+':'+i.split(':')[2]
                zhulh = str(zhulh).strip("[u'']")
                critical_list.append(zhulh)   
    if 'well::list' not in redis.r.keys():
        redis.r['well::list'] = 0
    else:
        if len(redis.r.get('well::list')) > 2:
            for i in json.loads(redis.r.get('well::list')):
                zhulh = i.split(':')[0]+':'+i.split(':')[1]+':'+i.split(':')[2]
                zhulh = str(zhulh).strip("[u'']")
                well_list.append(zhulh)
                
def get_host_service(host_name):
    try:
        host_service = {}
        for host_id in host_name.keys():
            #print host_name.keys()
            monitor_list = []
            #service = {} 
            url_str = 'http://10.73.143.197:9000/api/configuration/%s/?format=json' %host_id
            #url_str = 'http://10.73.143.201:9000/api/configuration/2/?format=json'
            #url_str = "http://192.168.2.100:9000/api/configuration/"+host_id+"/?format=json"
            req = urllib2.urlopen(url_str)
            result = req.read()
            configs= json.loads(result)
            #在下面的for循环中如果status_monitor_on为false的话，将不会监控
            if configs.get('status_monitor_on') is True:
                for template in configs.get('template_list'):
                    monitor_list +=template['service_list']
                    #print monitor_list
                    #print '======================='
                host_service[host_name[host_id]] = monitor_list
            else:
                #清理redis中的数据
                #new_f_critical_list = []
                #new_f_well_list = []
                for i in redis.r.keys():
                    if i.find(host_name[host_id]) != -1:
                        keys = host_name[host_id]+i[len(host_name[host_id]):len(i)]
                        redis.r.delete(keys)
                for i in critical_list:
                    if i.find(host_name[host_id]) != -1:
                        keys = host_name[host_id]+i[len(host_name[host_id]):len(i)]
                        critical_list.remove(keys)
                for i in well_list:
                    if i.find(host_name[host_id]) != -1:
                        keys = host_name[host_id]+i[len(host_name[host_id]):len(i)]
                        well_list.remove(keys)
        #print host_service[host_name[host_id]]
    
            print host_service.keys()
            #print host_service
        return host_service
    except urllib2.URLError,e:
        print 'URLError Error Msg:',e
if __name__ == '__main__':
    host_name = W_mysql('SELECT id,hostname FROM web_host',num=1)
    #print host_name['1']
    fetch_redis_data()
    start_time = time.time()
    host_service = get_host_service(host_name)
    counter = 0
    #fetch_monitored_list(host_name,start_time)

    while True:
        if counter > 10:
            host_service = get_host_service(host_name)
            counter = 0
        fetch_monitored_list(host_name,start_time)
        counter +=1
        time.sleep(5)

