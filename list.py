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


def list_servers():
    r = requests.post('https://api.glesys.com/server/list',
                      headers=get_headers(),
                      auth=get_auth())

    resp = json.loads(r.text)

    print("Response: {}".format(resp["response"]["status"]["text"]))
    for server in resp["response"]["servers"]:
        iplist = ""
        for ip in server["iplist"]:
            iplist += "{}\t".format(ip["ipaddress"])
        print("{}\t{}\t{}".format(server["serverid"], server["hostname"], iplist))


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print(f"Usage: {sys.argv[0]}")
        sys.exit(1)

    list_servers()
    sys.exit(0)
