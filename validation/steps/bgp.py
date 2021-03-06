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
spine_bgp_neighbor_config = dict() 
leaf_bgp_neighbor_config = dict()
spine_vars = dict()
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

    if "bgp" in context.spine_vars.keys():
        for node in context.spine_vars["bgp"]:
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

    if "bgp" in context.leaf_vars.keys():
        for node in context.leaf_vars["bgp"]:
            list_of_leafs.append(node)


def get_spine_bgp_neighbors(context):
    ''' 
    Make Ansible API call to pull data directly from the node.
    Return data in json format
    '''
    global spine_bgp_neighbor_config

    runner = ansible.runner.Runner(module_name='command', 
                                   module_args="cl-bgp summary show json",
                                   become=True, pattern=list_of_spines)

    ansible_output = runner.run()

    if ansible_output is None:
        assert False, "Ansible is unable to contact the host"

    spine_bgp_neighbor_config = ansible_output["contacted"]


def get_leaf_bgp_neighbors(context):
    ''' 
    Make Ansible API call to pull data directly from the node.
    Return data in json format
    '''
    global leaf_bgp_neighbor_config

    runner = ansible.runner.Runner(module_name='command', 
                                   module_args="cl-bgp summary show json",
                                   become=True, pattern=list_of_leafs)

    ansible_output = runner.run()

    if ansible_output is None:
        assert False, "Ansible is unable to contact the host"

    leaf_bgp_neighbor_config = ansible_output["contacted"]


def get_spine_config_ports(context):
    '''
    Extract the interface list from the configured node. Convert to Ascii to make life easy
    '''
    global spine_bgp_neighbor_config

    return_dict = dict()

    for spine in list_of_spines:
        if spine_bgp_neighbor_config[spine]["stdout"] == "":
            assert False, "No BGP configuration found on " + spine

        else:
            json_data = json.loads(spine_bgp_neighbor_config[spine]["stdout"])

            if len(json_data["peers"]) == 0:
                assert False, "No peers found on " + spine

            return_dict[spine] = json_data["peers"].keys()


def get_leaf_config_ports(context):
    '''
    Extract the interface list from the configured node. Convert to Ascii to make life easy
    '''

    global leaf_bgp_neighbor_config

    for leaf in list_of_leafs:
        if leaf_bgp_neighbor_config[leaf]["stdout"] == "":
            assert False, "No BGP configuration found on " + leaf

        else:
            json_data = json.loads(leaf_bgp_neighbor_config[leaf]["stdout"])

            if len(json_data["peers"]) == 0:
                assert False, "No peers found on " + leaf

            return json_data["peers"].keys()


@given('BGP is enabled')
def step_impl(context):

    # Setup: Load Vars
    get_spine_vars(context)
    get_leaf_vars(context)

    # Setup: Load Config
    get_spine_bgp_neighbors(context)
    get_leaf_bgp_neighbors(context)

    # Only checking that BGP is in the vars file (i.e., it should be enabled)
    if len(list_of_spines) > 0 or len(list_of_leafs) > 0:
        assert True
    else:
        assert False, "No BGP peers defined in Ansible vars files for spines or leafs."


@when('neighbors are configured')
def step_impl(context):
    '''
    Actually check that the BGP config was pushed to the box 
    and that the number of peers on the box matches what we expect
    '''

    spine_var_ports = dict()
    spine_config_ports = dict()
    leaf_var_ports = dict()
    leaf_config_ports = dict()

    # Iterate over Spine Variables File
    if "bgp" in context.spine_vars:
            for spine in context.spine_vars["bgp"].keys():
                if "fabric_ports" in context.spine_vars["bgp"][spine]:
                    spine_var_ports[spine] = context.spine_vars["bgp"][spine]["fabric_ports"]
                else:
                    assert False, "fabric_ports not defined in Ansible vars file for " + spine

    # Iterate over Leaf Variables File
    if "bgp" in context.leaf_vars:
        for leaf in context.leaf_vars["bgp"].keys():
            if "fabric_ports" in context.leaf_vars["bgp"][leaf]:
                leaf_var_ports[leaf] = context.leaf_vars["bgp"][leaf]["fabric_ports"]
            else:
                assert False, "fabric_ports not defined in Ansible vars file for " + leaf

    for spine in list_of_spines:
        if spine_bgp_neighbor_config[spine]["stdout"] == "":
            assert False, "No BGP configuration found on " + spine
        else:
            json_data = json.loads(spine_bgp_neighbor_config[spine]["stdout"])

            if len(json_data["peers"]) == 0:
                assert False, "No peers found on " + spine

            # convert unicode elements to ascii
            spine_config_ports[spine] = [s.encode('ascii') for s in json_data["peers"].keys()]

    for leaf in list_of_leafs:
        if leaf_bgp_neighbor_config[leaf]["stdout"] == "":
            assert False, "no BGP configuration found on " + leaf
        else:
            json_data = json.loads(leaf_bgp_neighbor_config[leaf]["stdout"])

            if len(json_data["peers"]) == 0:
                assert False, "No peers found on " + leaf

            # convert unicode elements to ascii
            leaf_config_ports[leaf] = [s.encode('ascii') for s in json_data["peers"].keys()] 

    for leaf in leaf_var_ports:
        if not set(leaf_var_ports[leaf]) == set(leaf_config_ports[leaf]):
            assert False, "Configured leaf ports do not match variables file ports for " + leaf

    for spine in spine_var_ports:
        if not set(spine_var_ports[spine]) == set(spine_config_ports[spine]):
            assert False, "Configured spine ports do not match variables file ports for " + spine

    assert True


@then('the neighbors should be up')
def step_impl(context):
    '''
    Validate that the BGP state from Ansible is "Established"
    '''

    global spine_bgp_neighbor_config, list_of_spines
    global leaf_bgp_neighbor_config, list_of_leafs

    for spine in list_of_spines:
        json_data = json.loads(spine_bgp_neighbor_config[spine]["stdout"])

        neighbor_list = json_data["peers"].keys()

        for neighbor in neighbor_list:
            if not json_data["peers"][neighbor]["state"] == "Established":
                assert False, spine + " peer " + neighbor + " not Established. Current state: " + json_data["peers"][neighbor]["state"]

    for leaf in list_of_leafs:
        json_data = json.loads(leaf_bgp_neighbor_config[leaf]["stdout"])

        neighbor_list = json_data["peers"].keys()

        for neighbor in neighbor_list:
            if not json_data["peers"][neighbor]["state"] == "Established":
                assert False, leaf + " peer " + neighbor + " not Established. Current state: " + json_data["peers"][neighbor]["state"]

    assert True
