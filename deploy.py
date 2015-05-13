import os
import json

import pip
pip.main(['install', 'requests'])

import requests

home = os.path.expanduser('~')
name = os.environ['name']
version = os.environ['version']
url = os.environ['url']
prefix = os.path.join(home, os.environ['prefix'])
env = open('env').readlines()

girder_url = os.environ['GIRDER_URL'].rstrip('/')
girder_user = os.environ['GIRDER_USER']
girder_password = os.environ['GIRDER_PASSWORD']
girder_folder = os.environ['GIRDER_FOLDER']

token = requests.get(
    girder_url + '/user/authentication',
    auth=(girder_user, girder_password)
).json()['authToken']['token']

item = requests.post(
    girder_url + '/item',
    params={
        'token': token,
        'folderId': girder_folder,
        'name': name + ' ' + version
    }
).json()['_id']

assert requests.put(
    girder_url + '/item/' + item + '/metadata',
    params={'token': token},
    data=json.dumps({
        'name': name,
        'version': version,
        'source': url,
        'prefix': prefix,
        'env': env
    })
).ok
