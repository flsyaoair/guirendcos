# -*- coding: UTF-8 -*- 
from src.models import database
from src.models.project import project
from src.models.cm.projectprofile import projectProfile
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
def update_projectProfile(projectkey,dockerprofile):
    session = database.get_session()
    docker = session.query(projectProfile).filter(projectProfile.ProjectKey == projectkey).one()
    docker.DockerProfile = dockerprofile
    docker.LastUpdateDate = datetime.now() 
    session.commit()
    session.close()
def delete_project(project_id):
#     project_id = int(project_id)
    session = database.get_session()
    dp = session.query(project).filter(project.ProjectId == project_id).one()
    projectkey = dp.ProjectKey
    session.query(projectProfile).filter(projectProfile.ProjectKey == projectkey).delete()
    session.query(project).filter(project.ProjectId == project_id).delete()
    session.commit()
    session.close()
      
def query_projectProfile(projectkey):
    session = database.get_session()
    projectprofile = session.query(projectProfile).filter(projectProfile.ProjectKey == projectkey).one()
    session.commit()
    session.close()
    return projectprofile   
def query_project():
    session = database.get_session()
    project_list = session.query(project).all()
    session.commit()
    session.close()
    return project_list  
      
      