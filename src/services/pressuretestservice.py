from src.models import database
from datetime import datetime
def servicesCreate(taskcasename,jmxname,threads,rampup,threadloop,scale):
#     database = get_session()
    session = database.get_session()
    T = TEST_TASK()
    T.TaskCaseName = taskcasename
    T.JmxName = jmxname
    T.Threads = threads
    T.RampUp = rampup
    T.ThreadLoop = threadloop
    T.SCALE = scale
    session.add(T)
    session.commit()
    session.close()
def delete(id):
    session = database.get_session()
    session.query(TEST_TASK).filter(TEST_TASK.TestTaskId == id).delete()
    session.commit()
    session.close()    
def update(id,taskcasename,jmxname,threads,rampup,threadloop,scale):
#     taskcasename ='cc'
    session = database.get_session()

    task = session.query(TEST_TASK).filter(TEST_TASK.TestTaskId == id).update({'TaskCaseName':taskcasename,'JmxName':jmxname,'Threads':threads,'RampUp':rampup,'ThreadLoop':threadloop,'SCALE':scale})

    session.commit()
    session.close()
def remoteclient():

    session = database.get_session()
    taskcase = session.query(TEST_TASK).filter(TEST_TASK.TaskCaseName == taskcasename).one()
#     jmxname= taskcase.JmxName
#     return jsonify({'JmxName':taskcase.JmxName,'Threads':taskcase.Threads,'RampUp':taskcase.RampUp,'ThreadLoop':taskcase.ThreadLoop,'SCALE':taskcase.SCALE})    
def exist_category(name):
    session = database.get_session()

    c = session.query(TEST_TASK).filter(TEST_TASK.TaskCaseName == name).count()

    session.close()
    return c > 0
def get(taskcasename):
    session =  database.get_session()
    taskcase = session.query(TEST_TASK).filter(TEST_TASK.TaskCaseName == taskcasename).one()
    return taskcase 
def gettaskcasename(id):
    session =  database.get_session()
    taskcase = session.query(TEST_TASK).filter(TEST_TASK.TestTaskId == id).one()
    return taskcase 