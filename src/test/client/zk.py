from kazoo.client import KazooClient,KazooState,logging,KazooRetry
from kazoo.security import make_digest_acl
from flask import abort,request,Flask,jsonify
import json,cx_Oracle,time,os,socket,urllib
from string import replace

logging.basicConfig()
app = Flask(__name__)

def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
        print "Session lost!"
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        print "Disconnected from zookeeper!"
    else:
        # Handle being connected/reconnected to Zookeeper
        print "Connected to zookeeper!"
        
acls = [make_digest_acl('dcosadmin','zjdcos01',all=True),make_digest_acl('scrm','scrm1121',read=True),]
zk = KazooClient(hosts='10.78.180.44:2181,10.78.180.45:2181,10.78.180.46:2181',auth_data=[('digest','dcosadmin:zjdcos01')])
zk.start()
kr = KazooRetry(max_tries=5, ignore_expire=False)
result = kr(zk.get, "/dcos/chk")
zk.add_listener(my_listener)
crmweb_path = "/ywzc/crm/crm2014/webs"
crmapp_path = "/ywzc/crm/crm2014/apps/cluster"
db_conn = 'dcos/v1g2m60id2499yz@pdbdcos'
marathon_list = ['10.78.182.12','10.78.217.11']
marathon_url = '10.78.182.12:8080'

#Test marathon
def testMarathon():
    global marathon_url
    for i in marathon_list:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(1)
        try:
            sk.connect((i,8080))
            marathon_url = i+':8080'
            sk.close()
            break
        except Exception:
            sk.close()

#Test app
def testUrl(url):
    try:
        statusCode =urllib.urlopen(url).getcode()
        if (statusCode == 200):
            return True
        else:
            return False
    except Exception:
        return False

# Init crm-web node
def zk_init():
    del_path(crmweb_path)
    create_path(crmweb_path)
    del_path(crmapp_path)
    create_path(crmapp_path)
    testMarathon()
    marathon = json.loads(os.popen("curl -u dcosadmin:zjdcos01 http://"+marathon_url+"/v2/tasks 2>>/dev/null").read())['tasks']
    sync_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
    transaction = zk.transaction()
    for i in marathon:
        app = i['appId'].replace('/','')
        if app == 'scrm-web' :
            #host = i['host']
            host = socket.gethostbyname(i['host'])
            ports = str(i['ports'])
            ports = replace(ports,'[','')
            ports = replace(ports,']','')
            for j in range(0, 10):
                if (testUrl("http://"+host+":"+ports+"/version.txt") == True):
                    transaction.create(crmweb_path+"/"+host+":"+ports,acl=acls)
                    zkSync_log(app,sync_time,'init',host,ports,'TASK_RUNNING')
                    break
                time.sleep(20)
        if app == 'scrm-app' :
            host = socket.gethostbyname(i['host'])
            ports = str(i['ports'])
            ports = replace(ports,'[','')
            ports = replace(ports,']','')
            for j in range(0, 10):
                if (testUrl("http://"+host+":"+ports+"/version.txt") == True):
                    transaction.create(crmapp_path+"/jndiTemplate"+host+":"+ports+"?null&null&java.naming.factory.initial=weblogic.jndi.WLInitialContextFactory&java.naming.provider.url=t3:::"+host+":"+ports,acl=acls)
                    zkSync_log(app,sync_time,'init',host,ports,'TASK_RUNNING')
                    break
                time.sleep(20)
    transaction.commit()
    
# Create a node
def create_path(my_path):
    if not zk.exists(my_path):
        zk.create(my_path,acl=acls)

# Determine if a node exists
def chk_path(my_path):
    if zk.exists(my_path):
        # Print the version of a node and its data
        data,stat = zk.get(my_path)
        print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
        # List the children
        children = zk.get_children(my_path)
        print("There are %s children with names %s" % (len(children), children))

# Change a node ACL
def set_acl(my_path,my_acls):
    if zk.exists(my_path):
        zk.set_acls(my_path,my_acls)

# Set a node data
def set_data(my_path,my_data):
    zk.set(my_path, my_data)

# Delete a node with data
def del_path(my_path):
    if zk.exists(my_path):
        zk.delete(my_path, recursive=True)
        
###############Write zkSync log##################
def zkSync_log(APP_ID,SYNC_TIME,SYNC_TYPE,HOST,PORT,TASK_STAT):
    conn = cx_Oracle.connect(db_conn)
    cursor = conn.cursor ()
    cursor.execute ("insert into zkSync_log values('"+str(APP_ID)+"','"+str(SYNC_TIME)+"','"+str(SYNC_TYPE)+"','"+str(HOST)+"','"+str(PORT)+"','"+str(TASK_STAT)+"')")

    conn.commit()
    cursor.close ()
    conn.close ()
    return
   
###############Rest API##################
@app.route('/v1.0/dcos', methods=['POST'])
def create_task():
#   get data
    if not request.json or not 'eventType' in request.json:
        abort(400)
    eventType = request.json['eventType']
    if eventType == 'status_update_event' :
        appId = request.json['appId']
        appId = appId.replace('/','')
        if appId == 'scrm-web' :
            taskStatus = request.json['taskStatus']
            print "web "+taskStatus
            host = socket.gethostbyname(request.json['host'])
            ports = str(request.json['ports'])
            ports = replace(ports,'[','')
            ports = replace(ports,']','')
            if taskStatus == 'TASK_RUNNING' :
                #insert from zk
                for i in range(0, 10):
                    if (testUrl("http://"+host+":"+ports+"/version.txt") == True):
                        sync_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
                        create_path(crmweb_path+"/"+host+":"+ports)
                        zkSync_log(appId,sync_time,'insert',host,ports,taskStatus)
                        break
                    time.sleep(20)
            if (taskStatus == 'TASK_KILLED' or taskStatus == 'TASK_FAILED' or taskStatus == 'TASK_FINISHED' or taskStatus == 'TASK_LOST') :
                #delete from zk
                sync_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
                del_path(crmweb_path+"/"+host+":"+ports)
                zkSync_log(appId,sync_time,'delete',host,ports,taskStatus)
            task = {
                'eventType': eventType,
                'taskStatus': taskStatus,
                'appId': appId,
                'host': host,
                'ports': ports
            }
        if appId == 'scrm-app' :
            taskStatus = request.json['taskStatus']
            print "app "+taskStatus
            host = socket.gethostbyname(request.json['host'])
            ports = str(request.json['ports'])
            ports = replace(ports,'[','')
            ports = replace(ports,']','')
            if taskStatus == 'TASK_RUNNING' :
                #insert from zk
                for i in range(0, 10):
                    if (testUrl("http://"+host+":"+ports+"/version.txt") == True):
                        sync_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
                        create_path(crmapp_path+"/jndiTemplate"+host+":"+ports+"?null&null&java.naming.factory.initial=weblogic.jndi.WLInitialContextFactory&java.naming.provider.url=t3:::"+host+":"+ports)
                        zkSync_log(appId,sync_time,'insert',host,ports,taskStatus)
                        break
                    time.sleep(20)
            if (taskStatus == 'TASK_KILLED' or taskStatus == 'TASK_FAILED' or taskStatus == 'TASK_FINISHED' or taskStatus == 'TASK_LOST') :
                #delete from zk
                sync_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
                del_path(crmapp_path+"/jndiTemplate"+host+":"+ports+"?null&null&java.naming.factory.initial=weblogic.jndi.WLInitialContextFactory&java.naming.provider.url=t3:::"+host+":"+ports)
                zkSync_log(appId,sync_time,'delete',host,ports,taskStatus)
            task = {
                'eventType': eventType,
                'taskStatus': taskStatus,
                'appId': appId,
                'host': host,
                'ports': ports
            }
        else:
            task = {'test': 'test'}
    else:
            task = {'test': 'test'}
            
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    #create_path(crmweb_path+"/10.78.182.20:12345")
    #del_path(crmweb_path+"/10.78.182.20:22345")
    #create_path(crmapp_path)
    #chk_path(crmapp_path)
    #set_acl("/dcos/chk",[make_digest_acl('dcosadmin','zjdcos01',all=True),])
    try:
        #init data
        zk_init()
        app.debug = False
        app.run(host='0.0.0.0',port=80,use_reloader=False,threaded=True)
    finally:
        conn = cx_Oracle.connect('mon/mon@zjmon')
        cursor = conn.cursor ()
        cursor.execute ("insert into app_sm values('zkCrm','18258829588','CRM ZOOKEEPER APP EXIT!!!')")
        #cursor.execute ("insert into app_sm values('zkCrm','15857114022','CRM ZOOKEEPER APP EXIT!!!')")

        conn.commit()
        cursor.close ()
        conn.close ()
        zk.stop()
        zk.close()