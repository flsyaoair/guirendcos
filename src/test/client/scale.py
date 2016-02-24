from flask import abort,request,Flask,jsonify,make_response
from flask_httpauth import HTTPBasicAuth
import json,httplib2,cx_Oracle,time,os,socket

'''curl -i http://127.0.0.1:5000/v1.0/dcos -H "Content-Type: application/json" -X POST -d '{"app_id":"sjyyt-web","type":"thread","value":70,"time":"20151026193030"}'
'''
auth = HTTPBasicAuth()

@auth.get_password 
def get_password(username):
    if username == 'dcosadmin':
        return 'zjdcos01'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
app = Flask(__name__)

scale_rule=[]
db_conn='dcos/v1g2m60id2499yz@pdbdcos'
marathon_list = ['10.78.182.10','10.78.182.11','10.78.217.10']
marathon_url = "10.78.182.10:8080"

class web_count():
    scale_in_count = 0

class app_count():
    scale_in_count = 0

###############Init scale rule##################
def dcos_init():
    global scale_rule
    conn = cx_Oracle.connect(db_conn)
    cursor = conn.cursor ()

    cursor.execute ("select * from scale_rule")
    rows = cursor.fetchall()  
    for row in rows:  
        temp = {
            'RULE_TYPE': row[0],
            'APP_ID': row[1],
            'RULE_NUM': row[2],
            'REP_TIME': row[3],
            'SCALE_OUT': row[4],
            'SCALE_IN': row[5],
            'SCALE_INIT': row[6],
            'SCALE_MAX': row[7],
            'SCALE_INC': row[8],
            'OBL_VALUE': row[9],
            'THRESHOLD': row[10]
        } 
        scale_rule.append(temp)
    cursor.close ()
    conn.close ()
    return

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

###############Write scale log##################
def scale_log(APP_ID,SCALE_TIME,SCALE_TYPE,OLD_NUM,NEW_NUM,ALT_TYPE,ALT_VALUE,ALT_TIME):
    conn = cx_Oracle.connect(db_conn)
    cursor = conn.cursor ()
    cursor.execute ("insert into scale_log values('"+str(APP_ID)+"','"+str(SCALE_TIME)+"','"+str(SCALE_TYPE)+"',"+str(OLD_NUM)+","+str(NEW_NUM)+",'"+str(ALT_TYPE)+"',"+str(ALT_VALUE)+",'"+str(ALT_TIME)+"')")

    conn.commit()
    cursor.close ()
    conn.close ()
    return

###############Restart##################
def restart_task(app_id):
    conn = httplib2.Http()
    conn.add_credentials('dcosadmin','zjdcos01')
    headers = {"Content-type": "application/json"}
    testMarathon()
    response,content = conn.request('http://'+marathon_url+'/v2/apps/'+app_id+'/restart','POST',headers=headers,body='')
    print "Return code:", response.status, " reason:", response.reason
    if response.status == 200:
        user = json.loads(content)
        print user['version']
    else:
        print "Error sending message,check your input"
    return

###############Write restart log##################
def restart_log(APP_ID,COM_ID):
    conn = cx_Oracle.connect(db_conn)
    cursor = conn.cursor ()
    restart_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
    cursor.execute ("insert into restart_log values('"+str(APP_ID)+"','"+str(COM_ID)+"','"+str(restart_time)+"')")

    conn.commit()
    cursor.close ()
    conn.close ()
    return

###############Scale##################
def scale_task(app_id,int_ins):
    conn = httplib2.Http()
    conn.add_credentials('dcosadmin','zjdcos01')
    headers = {"Content-type": "application/json"}
    params = ({"instances": int_ins})
    testMarathon()
    response,content = conn.request('http://'+marathon_url+'/v2/apps/'+app_id,'PUT',headers=headers,body=json.JSONEncoder().encode(params))
    print "Return code:", response.status, " reason:", response.reason
    if response.status == 200:
        user = json.loads(content)    
        print user['version']
    else:
        print "Error sending message,check your input"
    return

###############Get instance count##################
def get_count(app_id):
    testMarathon()
    marathon = json.loads(os.popen("curl -u dcosadmin:zjdcos01 http://"+marathon_url+"/v2/apps 2>>/dev/null").read())['apps']
    for i in marathon:
        app = i['id'].replace('/','')
        instances_count = i['instances']
        if app == app_id:
            break
    return instances_count

###############Scale test##################
def scale(app_id,alt_type,alt_value,alt_time):
    if app_id == 'sjyyt-web':
        sc = web_count
    else:
        sc = app_count
    rule_num = 0
    for i in scale_rule:
        app = i['APP_ID']
        if app == app_id:
            rule_type = i['RULE_TYPE'] #thread
            if rule_type == alt_type:
                rule_num = i['RULE_NUM'] # 20
                rep_time = i['REP_TIME'] # 30
                scale_out = i['SCALE_OUT'] # 0-close 1-open
                scale_in = i['SCALE_IN'] # 0-close 1-open
                scale_init = i['SCALE_INIT'] # init_ins_num
                scale_max = i['SCALE_MAX'] # max_ins_num
                scale_inc = i['SCALE_INC'] # per increase num
                obl_value = i['OBL_VALUE']
                threshold = i['THRESHOLD']
                break
    if rule_num == 0:
        #no rule
        return 3
    alt_count = get_count(app_id)
    scale_time = time.strftime("%Y%m%d%H%M%S",time.localtime())
    t_count = alt_count * rule_num
    t = 0
    c_count = 0
    scale_type = 0 # 0-scale out 1-scale in
    t_sub = t_count - alt_value
    #11.11 8-20
    '''t_hour = time.strftime("%H",time.localtime())
    t_min = time.strftime("%M",time.localtime())
    if int(t_hour) >= 8 and int(t_hour) <= 20:
        if int(t_min) == 50:
            t_sub = 0'''
    if t_sub <= 0:
        #full scale out
        sc.scale_in_count = 0 #clear scale_in data
        if scale_out == 1:
            
            scale_type = 0
            c_count = scale_max
            if alt_count != c_count:
                scale_task(app_id,scale_max)
                #write scale log
                scale_log(app_id,scale_time,scale_type,alt_count,c_count,alt_type,alt_value,alt_time)
                return 2
    else:
        t_scale = (obl_value*rule_num) - t_sub
        if t_scale <= 0:
            #scale in
            sc.scale_in_count += 1
            t_scale = abs(t_scale)
            if t_scale>(threshold*rule_num):
                if scale_in == 1:
                    if sc.scale_in_count > rep_time:
                        sc.scale_in_count = 0
                        t = t_scale/rule_num
                        scale_type = 1
                        c_count = alt_count - t
                        if c_count < scale_init:
                            c_count = scale_init
                        if alt_count != c_count:
                            scale_task(app_id,c_count)
                            #write scale log
                            scale_log(app_id,scale_time,scale_type,alt_count,c_count,alt_type,alt_value,alt_time)
                            return 1
        else:
            #scale out
            sc.scale_in_count += 1
            if t_scale>(threshold*rule_num):
                sc.scale_in_count = 0
                if scale_out == 1:
                    t = t_scale/rule_num
                    if t < scale_inc:
                        t = scale_inc
                    scale_type = 0
                    c_count = alt_count + t
                    if c_count > scale_max:
                        c_count = scale_max
                    if alt_count != c_count:
                        scale_task(app_id,c_count)
                        #write scale log
                        scale_log(app_id,scale_time,scale_type,alt_count,c_count,alt_type,alt_value,alt_time)
                        return 2
    return 0
    

###############Rest API##################
@app.route('/v1.0/dcos', methods=['POST'])
@auth.login_required
def create_task():  
#   get data
    if not request.json or not 'app_id' in request.json:
        abort(400)
    if not 'com_id' in request.json:
        task = {
            'altApp': request.json['app_id'],
            'altType': request.json['type'],
            'altValue': request.json['value'],
            'altTime': request.json['time']
        }
        res_scale = scale(task['altApp'],task['altType'],task['altValue'],task['altTime'])
        if res_scale == 0:
            print "No scale!"
        elif res_scale == 1:
            print "Scale in!"
        elif res_scale == 2:
            print "Scale out!"
        else:
            print "No rule data!"
    else:
        task = {
            'altCom': request.json['com_id'],
            'altApp': request.json['app_id']
        }
        print "Restart App : " + task['altApp']
        restart_task(task['altApp'])
        restart_log(task['altApp'],task['altCom'])
        
    return jsonify({'task': task}), 201

if __name__ == '__main__':
    try:
        #init data 
        dcos_init()
        app.debug = False
        app.run(host='0.0.0.0',use_reloader=False)
    finally:
        conn = cx_Oracle.connect('mon/mon@zjmon')
        cursor = conn.cursor ()
        cursor.execute ("insert into app_sm values('dcosScale','18258829588','DCOS SCALE APP EXIT!!!')")
        cursor.execute ("insert into app_sm values('dcosScale','15857114022','DCOS SCALE APP EXIT!!!')")

        conn.commit()
        cursor.close ()
        conn.close ()