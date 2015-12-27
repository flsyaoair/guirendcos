# -*- coding: UTF-8 -*- 
from flask import Flask
from src.collect import *

def create_dcos_app():
    app = Flask(__name__)
    app.config.from_pyfile('dcosconfig.py')
    app.jinja_env.variable_start_string = '(('
    app.jinja_env.variable_end_string = '))'
    app.register_module(mesos)
    app.register_module(marathon)
    return app