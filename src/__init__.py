# -*- coding: UTF-8 -*- 
from flask import Flask
from src.collect import *
from src.controllers import *
from src.dcosconfig import *

def create_dcos_app():
    app = Flask(__name__)
    app.config.from_pyfile('dcosconfig.py')
    app.jinja_env.variable_start_string = '(('
    app.jinja_env.variable_end_string = '))'
    app.register_module(home)
    app.register_module(dashboard)
    app.register_module(mesos)
    app.register_module(marathon)
    app.register_module(jenkins)
    app.register_module(docker)
    app.register_module(project)
    return app
