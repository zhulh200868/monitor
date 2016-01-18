#!/usr/local/python2.7/bin/python
# -*- coding=utf-8 -*-

import os,sys,MySQLdb

host_name = {}

def W_mysql(host,service,times,num):
    try:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='s6monitor2',unix_socket='/tmp/mysql_3308.sock',port=3308)
        cur = conn.cursor()
        #cur.execute('CREATE DATABASE IF NOT EXISTS nagios')
        #判断nagios数据库是否存在
        '''
        cur.execute('show databases')
        result = cur.fetchall()
        db = []
        for (line,) in result:
            new_line = (line)
            db.append(new_line)
        
        if 'nagios' not in db:
            cur.execute('CREATE DATABASE IF NOT EXISTS nagios20151023 charset="utf-8"')   
        ''' 
        conn.select_db('s6monitor2')
        #判断critical表是否存在
        #cur.execute('show tables')
        '''
        res = cur.fetchall()
        table = []
        for (line,) in res:
            new_res = (line)
            table.append(new_res)
        
        if 'critical' not in table:
            cur.execute('CREATE TABLE IF NOT EXISTS nagios_web_critical(id int(20) not null auto_increment,hostname char(10),service_name char(10),time char(20),primary key(id))')
        '''
        s_cmd = "select time from web_monitor_critical where hostname='"+host+"' and service_name='"+service+"'"
        cur.execute(s_cmd)
        res = cur.fetchall()
        '''
        print res
        for (line,) in res:
            new_res = (line)
        print new_res
        '''
        if str(res).strip('()') != '':
            if num == 'C':
                u_cmd = "update web_monitor_critical set time='"+times+"' where hostname='"+host+"' and service_name='"+service+"';"
                cur.execute(u_cmd)  
            elif num == 'W':
                d_cmd = "delete from web_monitor_critical where hostname='"+host+"' and service_name='"+service+"';" 
                cur.execute(d_cmd)
        elif str(res).strip('()') == '':
            if num == 'C':
                i_cmd = 'insert into web_monitor_critical (hostname,service_name,time) values(' +"'"+host+"',"+"'"+service+"',"+"'"+times+"');"
                cur.execute(i_cmd) 
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print 'Mysql Error Msg:',e
        
def S_mysql(sql_cmd,num):
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
        
        
if __name__ == '__main__':
    host = 'Test_server'
    service = 'memory'
    times='1111'
    num = 'C'
    s_cmd = "select count(*) from web_monitor_critical where hostname='"+host+"' and service_name='"+service+"'"
    W_mysql(host, service, times,num)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    