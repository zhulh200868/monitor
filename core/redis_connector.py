#!/usr/local/python2.7/bin/python
# -*- coding=utf-8 -*-

import redis

r = redis.Redis(host='localhost',port=6379,db=0)

#r['YourKey'] = 'YourValue'

def get_redis(host_ip='localhost',port=6379,db=0):

	return redis.Redis(host=host_ip,port=port,db=db)