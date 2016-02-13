# Interop 2016 - Network Continuous Integration
This is a fully automated network with application servers connected. 100% of the configuration is managed through git and Ansible. 

The goal of this project is to demonstrate how CI tools like [Travis-CI](https://travis-ci.org/) can be leveraged to automatically spin up a virtual networking environment and automatically run integration tests against the network for any proposed changes. 

#Diagrams:
![Diagram](diagram.png)
Shared Google Drawing
https://docs.google.com/a/cumulusnetworks.com/drawings/d/1KI-OqsfdOIpu6VPe08vRmlXAG1H8IR8B3Yq2-JGpLp0/edit?usp=sharing

#Routing
Server to leaf and leaf to spine routing utilize eBGP. 

The [BGP unnumbered](https://docs.cumulusnetworks.com/display/DOCS/Configuring+Border+Gateway+Protocol+-+BGP#ConfiguringBorderGatewayProtocol-BGP-unnumberedUsingBGPUnnumberedInterfaces) feature is used so that no IP addresses are required for any infrastructure links.

The leafs announce default routes to the hosts.

#Files
- spines.yml: This is the Ansible configuration definition to deploy spine nodes
- leafs.yml: This is the Ansible configuration definition to deploy leaf nodes
- ceph.yml: This is the Ansible configuration definition to deploy ceph hosts
- Vagrantfile: This is the Vagrant configuration definition to build the virtual network and virtual machine parameters
- packages (directory): This contains the Debian packages that are installed on the hosts to install Quagga. This is to provide an offline method for provisioning hosts. 
- ansible.cfg: The configuration file for ansible settings 