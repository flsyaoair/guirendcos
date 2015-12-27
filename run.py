# -*- coding: UTF-8 -*- 

from src import create_dcos_app
from src.cmconfig import *
from src import mesoscollet
from src import marathoncollet

app = create_dcos_app()

if __name__ == '__main__':
#     app.debug = DEBUG
#     app.run(host= HOST,port=PORT)
      mesoscollet.create()
      marathoncollet.marathoncollet()