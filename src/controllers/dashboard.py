from flask import Module,render_template,jsonify, request,g
from src.dcosconfig import *
from src.controllers.filters import login_filter
dashboard = Module(__name__)

dashboard.before_request(login_filter)

@dashboard.route('/')
def index():
    menuList = {
        'index': {
            'main': 'active'
        },

        'template': {
            'main': '',
            'sub1': '',
            'sub2': '',
        }
    }
    return render_template('Dashboard/index.html',menu = menuList)

@dashboard.route('/template/container')
def container():
    menuList = {
        'index': {
            'main': ''
        },

        'template': {
            'main': 'active',
            'sub1': 'active',
            'sub2': '',
        }
    }

    return render_template('template/container.html', menu = menuList)


@dashboard.route('/template/service')
def service():
    menuList = {
        'index': {
            'main': ''
        },

        'template': {
            'main': 'active',
            'sub1': '',
            'sub2': 'active',
        }
    }

    return render_template('template/service.html', menu = menuList)
