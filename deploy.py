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
env = [l.strip() for l in open('env').readlines() if l.strip()]

girder_url = os.environ['GIRDER_URL'].rstrip('/')
girder_user = os.environ['GIRDER_USER']
girder_password = os.environ['GIRDER_PASSWORD']
girder_folder = os.environ['GIRDER_FOLDER']

chunk_size = 1024 * 1024 * 64

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

with open('package.tar.bz2') as f:
    size = os.path.getsize('package.tar.bz2')

    id = requests.post(
        girder_url + '/file',
        params={
            'parentType': 'item',
            'parentId': item,
            'name': name + '_' + version + '.tar.bz2',
            'size': size
        }
    ).json()['_id']

    next_size = min(chunk_size, size)
    while next_size > 0:
        chunk = f.read(next_size)

        assert requests.post(
            girder_url + '/file/chunk',
            params={
                'offset': f.tell(),
                'uploadId': id
            },
            files={
                'chunk': chunk
            }
        ).ok

        next_size = min(chunk_size, size - f.tell())
