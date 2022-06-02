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


def create_server(hostname, cloud_init_data):
    payload = {
        'datacenter': 'Falkenberg',
        "platform": "KVM",
        "hostname": hostname,
        "templatename": "ubuntu-22-04",
        "cpucores": 2,
        "memorysize": 2048,
        "disksize": 20,
        "users": [{"username": "demo", "sshkeys": ["ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIO8qj4Ss6P9LpZR7tAkj6osCwVWnE+krY8bzRttJ9pnj demo"]}],
        "cloudconfig": cloud_init_data
    }

    r = requests.post('https://api.glesys.com/server/create',
                      data=json.dumps(payload),
                      headers=get_headers(),
                      auth=get_auth())

    resp = json.loads(r.text)

    print("Response: {}".format(resp["response"]["status"]["text"]))
    print("Server ID: {}".format(resp["response"]["server"]["serverid"]))
    iplist = resp["response"]["server"]["iplist"]
    for ip in iplist:
        print("{}".format(ip["ipaddress"]))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <hostname> <cloud-init.yaml>")
        sys.exit(1)

    hostname = sys.argv[1]
    with open(sys.argv[2]) as cloud_init:
        cloud_init_data = cloud_init.read()
        create_server(hostname, cloud_init_data)
    sys.exit(0)
