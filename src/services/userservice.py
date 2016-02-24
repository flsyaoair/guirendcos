# -*- coding: UTF-8 -*- 

from src.models import UserProfile, UserStatus, database
from datetime import datetime
#from projectTeam.powerteamconfig import PAGESIZE
from sqlalchemy.sql.expression import or_
from src.dcosconfig import *

def get(email):
    session = database.get_session()

    user = session.query(UserProfile).filter(UserProfile.Email == email).first()
    session.close()
    return user

def get_user_by_id(user_id):
    session = database.get_session()

    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).one()
    session.close()
    return user

def change_password(raw_password,new_password,user_id):
    session = database.get_session()

    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).first()
    if not user.Password == raw_password:
        session.close()
        return False
    user.Password = new_password

    session.commit()
    session.close()
    return True

def udpate_profile(email,nick,user_id):
    email = email.strip()
    nick = nick.strip()
    session = database.get_session()

    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).first()

    if not user.Email == email:
        exist = session.query(UserProfile).filter(UserProfile.Email == email).count() > 0
        if exist:
            session.close()
            return False
        else :
            user.Email = email

    user.Nick = nick

    session.commit()
    session.close()
    return True

def register(email,nick,password):
    email = email.strip()
    nick = nick.strip()
    session = database.get_session()

    exist = session.query(UserProfile).filter(UserProfile.Email == email).count() > 0

    userid = -1

    if not exist :
        user = UserProfile()
        user.Email = email
        user.Nick = nick
        user.Password = password
        user.EmailVerify = False
        user.Status = UserStatus.Enabled
        user.IsAdmin = False
        user.RegDate = datetime.now()
        session.add(user)
        session.commit()
        userid = user.UserId

    session.close()
    return (exist,userid)

def enable_user(user_id):
    session = database.get_session()

    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).update({'Status':UserStatus.Enabled})

    session.commit()
    session.close()

def disable_user(user_id):
    session = database.get_session()

    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).update({'Status':UserStatus.Disabled})

    session.commit()
    session.close()


def assign_admin(user_id):
    session = database.get_session()

    user = session.query(UserProfile).filter(UserProfile.UserId == user_id).one()

    user.IsAdmin = not user.IsAdmin

    session.commit()
    session.close()