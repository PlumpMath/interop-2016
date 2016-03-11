from behave import *
import ansible.runner, yaml
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
spine_vars = dict()


def get_spine_vars(context):
    '''
    Open the Ansible vars file and load it into spine_vars
    '''

    with open(spine_vars_location) as stream:
        try:
            context.spine_vars = yaml.load(stream)
        except yaml.YAMLError as exc:
            assert False, "Failed to load spine variables file: " + exc


def get_spine_bgp_neighbors(context):
    ''' 
    Make Ansible API call to pull data directly from the node.
    Return data in json format
    '''
    global spine_bgp_neighbor_config

    runner = ansible.runner.Runner(module_name='command', 
                                   module_args="cl-bgp summary show json",
                                   become=True, pattern="spine2")

    ansible_output = runner.run()

    if ansible_output is None:
        assert False, "Ansible is unable to contact the host"

    spine_bgp_neighbor_config = json.loads(
                                            ansible_output['contacted'].
                                            items()[0][1]["stdout"].strip('"'))


def get_spine_var_bgp_ports(context):
    '''
    Return list of BGP ports from the Ansible vars file
    '''

    if "bgp" in context.spine_vars:
        if "spine2" in context.spine_vars["bgp"]:
            if "fabric_ports" in context.spine_vars["bgp"]["spine2"]:
                return context.spine_vars["bgp"]["spine2"]["fabric_ports"]
            else:
                assert False, "fabric_ports not defined in Ansible vars file"
        else:
            assert False, "spine2 not defined in Ansible vars file"
    else:
        assert False, "bgp not defined in Ansible vars file"


def get_spine_config_ports(context):
    '''
    Extract the interface list from the configured node. Convert to Ascii to make life easy
    '''

    if "peers" in spine_bgp_neighbor_config:
        return [s.encode('ascii') for s in spine_bgp_neighbor_config["peers"].keys()]
    else:
        assert False, "No peer configuration on the device"


def is_bgp_var_defined(context):
    '''
    Determine if BGP has been configured in the Ansible vars file
    '''
    if "bgp" in context.spine_vars:
        return True
    else:
        assert False, "BGP not configured in Ansible vars file"


def is_bgp_configured(context):
    '''
    Determine if BGP configuration was pushed to the device
    '''

    assert True


def is_bgp_established(context):
    '''
    Given an interface, is the peer up?
    '''

    return True


@given('BGP is enabled')
def step_impl(context):

    # Setup: Load Vars
    get_spine_vars(context)

    # Setup: Load Config
    get_spine_bgp_neighbors(context)

    # Only checking that BGP is in the vars file (i.e., it should be enabled)
    assert is_bgp_var_defined(context), spine_bgp_neighbor_config


@when('neighbors are configured')
def step_impl(context):
    '''
    Actually check that the BGP config was pushed to the box 
    and that the number of peers on the box matches what we expect
    '''
    config_port_list = get_spine_config_ports(context)
    var_port_list = get_spine_var_bgp_ports(context)

    if set(config_port_list) == set(var_port_list):
        assert True
    else:
        assert False, "Port lists do not match. Vars: " + str(var_port_list) + " Configured: " + str(config_port_list)


@then('the neighbors should be up')
def step_impl(context):

    failed_list = []

    if "peers" in spine_bgp_neighbor_config:
        for interface, state in spine_bgp_neighbor_config["peers"].iteritems():
            if not state["state"] == "Established":
                failed_list.append([interface.encode('ascii'), state["state"].encode('ascii')])
    else:
        assert False, "No Peers found in BGP configuration"

    if len(failed_list) > 0:
        assert False, "Not all peers are up. The following peers are down: " + str(failed_list)
    else:
        assert True
