import os
import json
def createContainerProfile():
        readed = json.load(open('../static/model/docker/temp.json', 'r'))
        print readed

    
if __name__ == '__main__':
    createContainerProfile() 