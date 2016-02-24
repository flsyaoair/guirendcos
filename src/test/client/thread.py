import os
import json
import time
import socket
import re
import threading
import subprocess
from subprocess import TimeoutExpired

hostname = socket.gethostname()
os.putenv("CLASSPATH","/opt/jrockit/lib/wlclient.jar:/opt/jrockit/lib/wljmxclient.jar:/opt/jrockit/:.")
a='Thread Total: 80 Thread Idle: 79 Thread Standby: 0 Thread Running: 1 Thread Throughput: 6.00'
exp ='zj(web|app) Session Total :\s+(?P<session_total>\d+)\sThread Total:\s+(?P<thread_total>\d+)\sThread Idle:\s+(?P<thread_idle>\d+)\sThread Standby:\s+(?P<thread_standby>\d+)\sThread Running:\s+(?P<thread_running>\d+).*'
reg=re.compile(exp)
mutex = threading.Lock() 

def logging(text):
    ts = time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime())
    loginfo = '%s  %s' %(ts,text)
    logfile = '/var/log/thread.log'
    fd = open(logfile,'a')
    fd.write(loginfo)
    fd.write('\n')
    fd.close()

def get_metrics(name):
    container_context = json.load(os.popen("docker inspect %s" %name))[0]
    container_pid = os.popen('ps -ef | grep -v grep | grep java | grep %s | awk \'{print $2}\'' %name).read().strip()
    container_starttime = container_context['State']['StartedAt'].split('.')[0].replace('T','_')
    container_name = name
    container_type = container_context['Config']['Image'].split('/')[1].split(':')[0]
    try:
        container_cpu_used = os.popen("ps -p %d -o %%cpu | tail -1" %int(container_pid)).read().strip()
        container_mem_used = os.popen("grep 'VmRSS:' /proc/%d/status | awk -F' ' '{print $2}'" %int(container_pid)).read().strip()
    except Exception:
        container_cpu_used = 0
        container_mem_used = 0
    try:
        container_port = container_context['NetworkSettings']['Ports']['7001/tcp'][0]['HostPort']
        cmdline = "docker exec %s sh /app/bin/getThread.sh 2>/dev/null | xargs" %name
        proc = subprocess.Popen(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        text = 'the %s exec thread %s is OK' %(name,proc.pid)
        logging(text)
        outs,errs = proc.communicate(timeout=8)
        match=reg.match(outs.strip())
        container_thread=match.groupdict()
    except TimeoutExpired:
        text = 'the pid %s process is killed' %proc.pid
        logging(text)
        proc.kill()
        container_thread = {'thread_total':0,'thread_idle':0,'thread_running':0,'session_total':0}
        container_port = 0
    except Exception,e:
        logging(str(e))
        container_thread = {'thread_total':0,'thread_idle':0,'thread_running':0,'session_total':0}
        container_port = 0
    if mutex.acquire():
        print hostname,container_name,container_starttime,container_type,container_port,container_cpu_used,container_mem_used,container_thread['thread_total'],container_thread['thread_idle'],container_thread['thread_running'],container_thread['session_total']
        mutex.release() 

if __name__ == '__main__':
    containers= os.popen("docker ps | egrep -v 'CONTAINER|mesos:1|haproxy|zookeeper|marathon' | awk '{print $1}' | tee /tmp/newcontainers").read().split()
    threadname = []
    for name in containers:
        t=threading.Thread(target=get_metrics,args=(name,))
        threadname.append(t)

    for i in threadname:
        i.start()
        time.sleep(0.5)

    for i in threadname:
        i.join()