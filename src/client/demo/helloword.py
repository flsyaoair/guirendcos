# -*- coding: UTF-8 -*- 
import os
from flask import Flask,request,url_for
from datetime import datetime
app = Flask(__name__)
@app.route('/')
def helloword():
    return '我的名字fls'


if __name__ == '__main__':

    app.run(host= '0.0.0.0',port=5004)