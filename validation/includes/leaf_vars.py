#!/usr/bin/env python2.7 


import yaml

with open("../roles/spines/vars/main.yml") as stream:
    try:
        print (yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)
