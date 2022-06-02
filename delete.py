#!/usr/bin/env python3

from pathlib import Path
import configparser
import requests
import json
import sys


def get_headers():
    return {'Content-Type': 'application/json', 'Accept':'application/json'}


def get_auth():
    config = configparser.ConfigParser()
    config.read(f"{Path.home()}/.glesys.ini")
    return config['api']['project'], config['api']['key']


def delete_server(server_id):
    payload = {
        'serverid': server_id,
        "keepip": "no"
    }

    r = requests.post('https://api.glesys.com/server/destroy',
                      data=json.dumps(payload),
                      headers=get_headers(),
                      auth=get_auth())

    resp = json.loads(r.text)
    print("Response: {}".format(resp["response"]["status"]["text"]))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <server id>")
        sys.exit(1)

    delete_server(sys.argv[1])
    sys.exit(0)
