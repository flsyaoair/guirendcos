# -*- coding: UTF-8 -*- 
from src.models import marathon,database
from datetime import datetime
# from configmanage.collect import mesoscollet
# cpus='1.0'
def create_marathon(appID,cpus,disk,mem,ports,dockerimages,host,port):
    session = database.get_session()
    ma = marathon()
    ma.AppName = appID
    ma.Cpus = cpus
    ma.Mem = mem
    ma.Disk = disk
#     ma.ports  = ports
    ma.DockerImage = dockerimages
    ma.Host = host
    port = port[0]
    ma.Port  = port
    
#     print type(p.Cpus)
    ma.CreateDate = datetime.now()  
    
     
    session.add(ma)
    session.commit()
    session.close()
    