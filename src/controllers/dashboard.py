from flask import Module,render_template,jsonify, request,g
from src.dcosconfig import *
from src.controllers.filters import login_filter
dashboard = Module(__name__)

dashboard.before_request(login_filter)

@dashboard.route('/Dashboard')
def index():
    return render_template('Dashboard/index.html')
