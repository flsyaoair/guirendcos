# -*- coding: UTF-8 -*- 

from flask import request, redirect, g,session

def login_filter():
    if 'username' not in session or session['username'] == None:
        return redirect('/')
    else:
        g.user_id = session['userid']

def admin_filter():
    if 'username' not in session or session['username'] == None or 'isadmin' not in session or session['isadmin'] == False:
        return redirect('/')