from behave import *
import ansible.runner
import yaml
import json

'''
    Scenario: Check BGP Neighbors
    Given BGP is enabled
    when neighbors are configured
    then the neighbors should be up
'''

spine_vars_location = "../roles/spines/vars/main.yml"
leaf_vars_location = "../roles/leafs/vars/main.yml"
spine_interface_config = dict() 
leaf_interface_config = dict()
spine_vars = dict()
leaf_vars = dict()
list_of_leafs = []
list_of_spines = []


def get_spine_vars(context):
    '''
    Open the Ansible vars file for spines and load it into spine_vars
    '''
    global list_of_spines

    with open(spine_vars_location) as stream:
        try:
            context.spine_vars = yaml.load(stream)
        except yaml.YAMLError as exc:
            assert False, "Failed to load spine variables file: " + exc

    if "interfaces" in context.spine_vars.keys():
        for node in context.spine_vars["interfaces"]:
            list_of_spines.append(node)


def get_leaf_vars(context):
    '''
    Open the Ansible vars file for leafs and load it into leaf_vars
    '''
    global list_of_leafs

    with open(leaf_vars_location) as stream:
        try:
            context.leaf_vars = yaml.load(stream)
        except yaml.YAMLError as exc:
            assert False, "Failed to load leaf variables file: " + exc

    if "interfaces" in context.leaf_vars.keys():
        for node in context.leaf_vars["interfaces"]:
            list_of_leafs.append(node)


def get_spine_interfaces(context):
    ''' 
    Make Ansible API call to pull data directly from the node.
    Return data in json format
    '''
    global spine_interface_config

    runner = ansible.runner.Runner(module_name='command', 
                                   module_args="netshow interface all -j",
                                   become=True, pattern=list_of_spines)

    ansible_output = runner.run()

    if ansible_output is None:
        assert False, "Ansible is unable to contact the host"

    spine_interface_config = ansible_output["contacted"]


def get_leaf_interfaces(context):
    ''' 
    Make Ansible API call to pull data directly from the node.
    Return data in json format
    '''
    global leaf_interface_config

    runner = ansible.runner.Runner(module_name='command', 
                                   module_args="netshow interface all -j",
                                   become=True, pattern=list_of_leafs)

    ansible_output = runner.run()

    if ansible_output is None:
        assert False, "Ansible is unable to contact the host"

    leaf_interface_config = ansible_output["contacted"]
 

@given('an interface is configured')
def step_impl(context):

    # Setup: Load Vars
    get_spine_vars(context)
    get_leaf_vars(context)

    # Setup: Load Config
    get_spine_interfaces(context)
    get_leaf_interfaces(context)

    # Only checking that BGP is in the vars file (i.e., it should be enabled)
    if len(list_of_spines) > 0 or len(list_of_leafs) > 0:
        assert True
    else:
        assert False, "No interfaces defined in Ansible vars files for spines or leafs."

@then('the interfaces should be up')
def step_impl(context):

    # global spine_bgp_neighbor_config, list_of_spines
    # global leaf_bgp_neighbor_config, list_of_leafs

    for spine in list_of_spines:
        json_data = json.loads(spine_interface_config[spine]["stdout"])
        # configured_iface_list = json_data.keys()
        var_interface_list = context.spine_vars["interfaces"][spine].keys()

        for interface in var_interface_list:
            if json_data[interface]["linkstate"] == "UP":
                continue
            else:
                assert False, "Interface " + interface + " on " + spine + " is in state " + json_data[interface]["linkstate"]
    assert True
