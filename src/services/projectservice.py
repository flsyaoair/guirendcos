# -*- coding: UTF-8 -*- 
from src.models import database
from src.models import project
from src.models.cm import projectProfile
from datetime import datetime

def create_project (projectname,projectkey,packagegettype,scmurl,poll,shell,status):
    session = database.get_session()
    pj = project()
    pj.ProjectName = projectname
    pj.ProjectKey = projectkey
    pj.PackageGetType = packagegettype
    pj.SCMUrl = scmurl
    pj.Poll = poll
    pj.Shell = shell
    pj.Status = status
    pj.CreateDate = datetime.now()  
    pj.LastUpdateDate = datetime.now() 
    session.add(pj)
    session.commit()
    session.close()
def create_projectProfile(projectkey,dockerprofile):
    session = database.get_session()
    docker = projectProfile()
    docker.ProjectKey = projectkey
    docker.DockerProfile = dockerprofile
    docker.CreateDate = datetime.now()  
    docker.LastUpdateDate = datetime.now() 
    session.add(docker)
    session.commit()
    session.close()
      