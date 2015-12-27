from flask import Module,render_template,jsonify, redirect, request, session, g
import pycurl
import StringIO
import urllib2 
import json
from src.services import mesosservice
mesos = Module(__name__)
mesosMetricslist = urllib2.urlopen('http://20.26.17.133:5050/metrics/snapshot').read()
colletList = ['master/cpus_total','cpus_used','master/mem_total','mem_used','disk_total','disk_used']
def mesoscollet():
    dictinfo  = json.loads(mesosMetricslist)
    mesoscolletlist = {}
#     print dictinfo
    for i in dictinfo:
        for x in colletList:
            if x in i:
                mesoscolletlist.setdefault(x,dictinfo[i])
    return mesoscolletlist

    
#     print  mesosMetricslist
    
def create():
    mesoscolletlist = mesoscollet()
    diskused = mesoscolletlist['disk_used']
    disktotal = mesoscolletlist['disk_total']
    cpustotal = mesoscolletlist['master/cpus_total']
    memtotal = mesoscolletlist['master/mem_total']
    memused = mesoscolletlist['mem_used']
    cpusused = mesoscolletlist['cpus_used']
#     print  cpustotal
    
    mesosservice.create_mesos(cpustotal, memtotal, disktotal, diskused, cpusused, memused)
    


    
# print json.dump(mesosMetricslist)

