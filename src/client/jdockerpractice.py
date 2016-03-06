# -*- coding: UTF-8 -*- 
import os
import subprocess
import json
import time
import urllib2
import jconfig
STRING = os.environ['STRING']
content = STRING
contentlist = content.split('&')
list = []
for i in contentlist:
    p = i.split('=')
    p = p[1] 
    l = list.append(p)
(name,image) =tuple(list)

buidtime = time.strftime("%Y-%m-%d.%Hh%Mm%Ss",time.localtime(time.time()))
print name
BUILD_ID = buidtime
BUILD_ID = BUILD_ID.encode()
def collectDockerImageId ():
    dockerimage = jsonfile()
    dockerimage = dockerimage.encode()
    dockerimage = dockerimage+name
    urllib2.urlopen('%s/iCloud/icloudAjax/acceptMsg.dox?appName=%s&msg=%s' %(jconfig.serverip,name,103)).read()
    os.system ('docker build -t %s.%s . >readme' %(dockerimage,BUILD_ID))
    
    readmeFile = open('readme','r')
    readmeFilelist = readmeFile.readlines()
    content = readmeFilelist[-1]
    content = content.split()
    imageId=content[-1]
#     urllib2.urlopen('http://10.73.144.222:8080/iCloud/icloudAjax/acceptMsg.dox?appName=demo&msg=helloworld').read()
    urllib2.urlopen('%s/iCloud/icloudAjax/acceptMsg.dox?appName=%s&msg=%s' %(jconfig.serverip,name,104)).read()
    cmd1 =os.system ('docker tag -f %s %s.%s' %(imageId,dockerimage,BUILD_ID))
    if not cmd1 == 0:
       return 1
    urllib2.urlopen('%s/iCloud/icloudAjax/acceptMsg.dox?appName=%s&msg=%s' %(jconfig.serverip,name,105)).read()
    cmd2 = os.system ('docker push %s.%s' %(dockerimage,BUILD_ID))
    if not cmd2 == 0:
       return 1
#     urllib2.urlopen('http://10.73.144.222:8080/iCloud/icloudAjax/acceptMsg.dox?appName=demo&msg=helloworld').read()
#     urllib2.urlopen('%s/iCloud/icloudAjax/acceptMsg.dox?appName=%s&msg=%s' %(jconfig.serverip,name,105)).read()
    images = dockerimage+'.'+BUILD_ID
    print images
    buildFile=open('build.txt','w')
    buildFile.write(images)
    buildFile.close()
def jsonfile ():
    readed = json.load(open('temp.json', 'r'))
    dockerimage = readed['container']['docker']['image']
#     json.dump(readed, open('app.json', 'w')) 
    return dockerimage 
if __name__ == '__main__':
    collectDockerImageId()