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


def preview(cloud_init_data):
    payload = {
        "users": [{"username": "demo", "sshkeys": ["ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO8qj4Ss6P9LpZR7tAkj6osCwVWnE+krY8bzRttJ9pnj demo"]}],
        "cloudconfig": cloud_init_data
    }

    r = requests.post('https://api.glesys.com/server/previewcloudconfig',
                      data=json.dumps(payload),
                      headers=get_headers(),
                      auth=get_auth())

    resp = json.loads(r.text)

    print("Response: {}".format(resp["response"]["status"]["text"]))
    print("{}".format(resp["response"]["cloudconfig"]["preview"]))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <cloud-init.yaml>")
        sys.exit(1)

    with open(sys.argv[1]) as cloud_init:
        cloud_init_data = cloud_init.read()
        preview(cloud_init_data)
    sys.exit(0)
