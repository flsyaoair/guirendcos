# -*- coding: UTF-8 -*- 
from src.models import mesos,database
from datetime import datetime
# from configmanage.collect import mesoscollet
# cpus='1.0'
def create_mesos(cpustotal,memtotal,disktotal,diskused,cpusused,memused):
    session = database.get_session()
    me = mesos()
    me.CpusTotal = cpustotal
    me.MemTotal = memtotal
    me.DiskTotal = disktotal
    me.DiskUsed = diskused
    me.CpusUsed = cpusused
    me.MemUsed  = memused
#     print type(p.Cpus)
    me.CreateDate = datetime.now()  
    
     
    session.add(me)
    session.commit()
    session.close()
    
   
# create_mesos('a')    