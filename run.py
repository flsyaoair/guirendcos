# -*- coding: UTF-8 -*- 
from src import create_dcos_app
from src.dcosconfig import *

app = create_dcos_app()

if __name__ == '__main__':
    app.debug = False
    app.run(host= HOST,port=PORT)

