#!/usr/bin/env python2.7 

import yaml
import ansible.runner
import json

spine_vars_location = "../roles/spines/vars/main.yml"
leaf_vars_location = "../roles/leafs/vars/main.yml"


def get_spine_vars(): 
    with open(spine_vars_location) as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def get_leaf_vars():
    with open(leaf_vars_location) as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)    

spine_vars = get_spine_vars()


#print spine_vars["bgp"]["spine1"]["fabric_ports"]
list_of_spines = ["spine1", "spine2"]
runner = ansible.runner.Runner(module_name='command', module_args="cl-bgp summary show json", 
                               become=True, pattern=list_of_spines)

#runner = ansible.runner.Runner(module_name="ping", module_args="", pattern="all")
datas = runner.run()

print datas
# Hostname: datas['contacted'].items()[0][0]
# command output: datas['contacted'].items()[0][1]["stdout"]
#command_output = json.loads(datas['contacted'].items()[0][1]["stdout"].strip('"'))

#convert json output to ASCII, return only swp list
#d = [s.encode('ascii') for s in command_output["peers"].keys()] 



# print d

#print "bgp" in spine_vars#["bgp"]["spine1"]["fabric_ports"]

# print set(spine_vars)
# print set(d)


# for interface, data in command_output["peers"].iteritems():
#     #print interface + " " + data["state"]
#     print data