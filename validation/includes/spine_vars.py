#!/usr/bin/env python2.7 

import yaml

with open("../roles/spines/vars/main.yml") as stream:
    try:
        return yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        return -1
