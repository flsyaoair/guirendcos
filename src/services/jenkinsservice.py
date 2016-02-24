from src.models import jenkins,database
from datetime import datetime
def servicesCreate(taskname,scmurl,poll,shell,typestatus):
#     database = get_session()
    session = get_session()
    T = JenkinsTask()
    T.TaskName = taskname
    T.SCMUrl = scmurl
    T.Poll = poll
    T.Shell = shell
    T.TypeStatus = typestatus
    session.add(T)
    session.commit()
    session.close()
def delete(id):
    session = get_session()
    session.query(JenkinsTask).filter(JenkinsTask.JenkinsTaskId == id).delete()
    session.commit()
    session.close() 
def update(id,taskname,scmurl,poll,shell):
#     taskcasename ='cc'
    session = get_session()

    task = session.query(JenkinsTask).filter(JenkinsTask.JenkinsTaskId == id).update({'TaskName':taskname,'SCMUrl':scmurl,'Poll':poll,'Shell':shell})

    session.commit()
    session.close()     