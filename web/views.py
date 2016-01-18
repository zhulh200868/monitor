# -*- coding=utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from rest_framework import viewsets
import serializers 
import models
import json
from rest_framework.decorators import api_view
from django.core.context_processors import request
import redis_connector as redis
from core.m_handle import host_service
# Create your views here.



    
class ConfigurationViewSet(viewsets.ModelViewSet):
    queryset =  models.Host.objects.all()
    serializer_class = serializers.HostSerializer 
    
def monitor_data(request):
    #print request.POST
    write_to_redis(request.POST)
    return HttpResponse('service sends status report success!!')

def write_to_redis(data):
    key = data['hostname']+'::'+data['service_name']
    redis.r[key] = json.dumps(data) 

def get_data(request):
    '''
    hostnames = models.Monitor_meg.objects.all().values('hostname').distinct()
    data = []
    h_list = {}
    for i in json.loads(redis.r['critical::list']):
        data.append(i)
    for i in json.loads(redis.r['well::list']):
        data.append(i)
    #print data
    new = []
    for y in range(len(data)):
        new.append(data[0].split(':')[0])
    new = list(set(new))
    #for z in new:
    #    print z
    #print new
    #print hostnames
    for k in new:
        new_data = []
        for i in range(len(data)):
            #if k['hostname'] == data[i].split(':')[0]:
            if k == data[i].split(':')[0]:
                service = str(data[i].split(':')[1])+'_'+str(data[i].split(':')[2])
                new_data.append(service)        
        #h_list[k['hostname']] = new_data 
        h_list[k] = new_data 
        
    print h_list
    '''
    h_service = []
    h_list = get_host_service()
    meg = models.Monitor_critical.objects.all()
    v_value = models.Monitor_meg.objects.all().values('service_name').distinct()
    print h_list
    #for i in h_list.keys():
    #    values = 
    #    h_service.append(i:)
    return render_to_response('home.html',{'v_value':v_value,'meg':meg,'h_list':h_list})

def graph(request):
    '''
        在这里需要考虑一下，因为穿过来hostname这个是其实是index，所以得考虑host_name对应的host_id的关系，在这里是加上了1，但是有点问题，需要解决。
    另外还需要考虑hostname和service_name这个对应关系出处，是redis还是mysql，所以下面的h_list还得值得商榷。
    '''
    hostname = request.POST['hostname']
    ids = int(hostname)+1
    hostnames = models.Host.objects.all().values('hostname').filter(id=ids)
    for k in hostnames:
        new_hostname = k['hostname']
    print new_hostname
    service_name = request.POST['service_name']


    return render_to_response('index.htm',{'hostname':new_hostname,'service_name':service_name})


def graph_data(request):
    fake_data = []
    hostname = request.GET['hostname']
    service_name = request.GET['service_name']
    zhulh = models.Monitor_meg.objects.all().values('time','num').filter(hostname=hostname,service_name=service_name).order_by('time').reverse()[0:100]
    for line in zhulh:
        num = [int(json.loads(line['time'])*1000),json.loads(line['num'])]
        fake_data.append(num)
    fake_data.sort()

    return HttpResponse(json.dumps(fake_data))




def gethostname(request):
    '''
    hostnames = models.Monitor_meg.objects.all().values('hostname').distinct()
    data = []
    h_list = {}
    for i in json.loads(redis.r['critical::list']):
        data.append(i)
    for i in json.loads(redis.r['well::list']):
        data.append(i)
    for k in hostnames:
        new_data = []
        for i in range(len(data)):
            if k['hostname'] == data[i].split(':')[0]:
                service = str(data[i].split(':')[1])+'_'+str(data[i].split(':')[2])
                new_data.append(service)        
        h_list[k['hostname']] = new_data 
    '''
    h_list = get_host_service()
    result = h_list.keys()
    
    return HttpResponse(json.dumps(result))

def getservice_name(request):
    '''
    hostnames = models.Monitor_meg.objects.all().values('hostname').distinct()
    data = []
    h_list = {}
    for i in json.loads(redis.r['critical::list']):
        data.append(i)
    for i in json.loads(redis.r['well::list']):
        data.append(i)
    for k in hostnames:
        new_data = []
        for i in range(len(data)):
            if k['hostname'] == data[i].split(':')[0]:
                service = str(data[i].split(':')[1])+'_'+str(data[i].split(':')[2])
                new_data.append(service)        
        h_list[k['hostname']] = new_data 
    '''
    h_list = get_host_service()
    getData = request.GET
    hostnameId = getData.get('Id')
    result = h_list.values()[int(hostnameId)]
    return HttpResponse(json.dumps(result))

def get_host_service():
    #get the host and the service_name 
    data = []
    h_list = {}
    host = []
    for i in json.loads(redis.r['critical::list']):
        data.append(i)
    for i in json.loads(redis.r['well::list']):
        data.append(i)    
    for y in range(len(data)):
        host.append(data[y].split(':')[0])
    host = list(set(host))
    for k in host:
        new_data = []
        for i in range(len(data)):
            if k == data[i].split(':')[0]:
                service = str(data[i].split(':')[1])+'_'+str(data[i].split(':')[2])
                new_data.append(service)        
        h_list[k] = new_data 
    return h_list

