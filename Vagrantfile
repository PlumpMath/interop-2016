# -*- mode: ruby -*-
# vi: set ft=ruby :

groups = {
  "spines" => ["spine1", "spine2"],
  "leafs" => ["leaf1", "leaf2", "leaf3", "leaf4"],
  "servers" => ["server1", "server2", "server3", "server-admin"],
  "network:children" => ["spines", "leafs"]
}


Vagrant.configure("2") do |config|

  cumulus_image = "cumulus-vx-2.5.5"
  server_image = "ubuntu/precise64"

  config.vm.define "leaf1" do |leaf1| 
   leaf1.vm.box = cumulus_image
   leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine1', auto_config: false
   leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine2', auto_config: false
   leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-server1', auto_config: false
   leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-server2', auto_config: false
   leaf1.vm.host_name = "leaf1"
   leaf1.vm.provision "ansible" do |ansible|
    ansible.groups = groups
    #ansible.verbose = "vvv"
    ansible.playbook = "lab.yml"
    end
  end
  
  config.vm.define "leaf2" do |leaf2|
   leaf2.vm.box = cumulus_image 
   leaf2.vm.network "private_network",  virtualbox__intnet: 'leaf2-spine1', auto_config: false
   leaf2.vm.network "private_network",  virtualbox__intnet: 'leaf2-spine2', auto_config: false
   leaf2.vm.network "private_network",  virtualbox__intnet: 'leaf2-server1', auto_config: false
   leaf2.vm.network "private_network",  virtualbox__intnet: 'leaf2-server2', auto_config: false
   leaf2.vm.host_name = "leaf2"
   leaf2.vm.provision "ansible" do |ansible|
    ansible.groups = groups
    ansible.playbook = "lab.yml"
    end
  end

  config.vm.define "leaf3" do |leaf3| 
   leaf3.vm.box = cumulus_image
   leaf3.vm.network "private_network",  virtualbox__intnet: 'leaf3-spine1', auto_config: false
   leaf3.vm.network "private_network",  virtualbox__intnet: 'leaf3-spine2', auto_config: false
   leaf3.vm.network "private_network",  virtualbox__intnet: 'leaf3-server3', auto_config: false
   leaf3.vm.network "private_network",  virtualbox__intnet: 'leaf3-server_admin', auto_config: false
   leaf3.vm.host_name = "leaf3"
   leaf3.vm.provision "ansible" do |ansible|
     ansible.groups = groups
     ansible.playbook = "lab.yml"
    end
  end

  config.vm.define "leaf4" do |leaf4| 
   leaf4.vm.box = cumulus_image
   leaf4.vm.network "private_network",  virtualbox__intnet: 'leaf4-spine1', auto_config: false
   leaf4.vm.network "private_network",  virtualbox__intnet: 'leaf4-spine2', auto_config: false
   leaf4.vm.network "private_network",  virtualbox__intnet: 'leaf4-server3', auto_config: false
   leaf4.vm.network "private_network",  virtualbox__intnet: 'leaf4-server_admin', auto_config: false
   leaf4.vm.host_name = "leaf4"
   leaf4.vm.provision "ansible" do |ansible|
     ansible.groups = groups
     ansible.playbook = "lab.yml"
    end
  end
  
  config.vm.define "spine1" do |spine1| 
   spine1.vm.box = cumulus_image
   spine1.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine1', auto_config: false
   spine1.vm.network "private_network",  virtualbox__intnet: 'leaf2-spine1', auto_config: false
   spine1.vm.network "private_network",  virtualbox__intnet: 'leaf3-spine1', auto_config: false
   spine1.vm.network "private_network",  virtualbox__intnet: 'leaf4-spine1', auto_config: false
   spine1.vm.host_name = "spine1"
   spine1.vm.provision "ansible" do |ansible|
     ansible.groups = groups
     ansible.playbook = "lab.yml"
    end
  end

  config.vm.define "spine2" do |spine2| 
   spine2.vm.box = cumulus_image
   spine2.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine2', auto_config: false
   spine2.vm.network "private_network",  virtualbox__intnet: 'leaf2-spine2', auto_config: false
   spine2.vm.network "private_network",  virtualbox__intnet: 'leaf3-spine2', auto_config: false
   spine2.vm.network "private_network",  virtualbox__intnet: 'leaf4-spine2', auto_config: false
   spine2.vm.host_name = "spine2"
   spine2.vm.provision "ansible" do |ansible|
      ansible.groups = groups
      ansible.playbook = "lab.yml"
    end
  end

  # config.vm.define "server1" do |server1| 
  #  server1.vm.box = "ubuntu/trusty64"
  #  server1.vm.network "private_network",  virtualbox__intnet: 'leaf1-server1', auto_config: false
  #  server1.vm.network "private_network",  virtualbox__intnet: 'leaf2-server1', auto_config: false
  #  server1.vm.host_name = "server1"
  #  server1.vm.provision "ansible" do |ansible|
  #     ansible.groups = groups
  #     ansible.extra_vars = {
  #     loopback_ip: "10.0.0.1",
  #     asn: "65500",
  #     fabric_ports: ["eth1", "eth2"],
  #     interface_list: ["lo", "eth1", "eth2"]
  #   }
  #    ansible.playbook = "server.yml"
  #   end
  # end
  
  # config.vm.define "server2" do |server2| 
  #  server2.vm.box = server_image
  #  server2.vm.network "private_network",  virtualbox__intnet: 'leaf1-server2', auto_config: false
  #  server2.vm.network "private_network",  virtualbox__intnet: 'leaf2-server2', auto_config: false
  #  server2.vm.host_name = "server2"
  #  server2.vm.provision "ansible" do |ansible|
  #     ansible.groups = groups
  #     ansible.extra_vars = {
  #     loopback_ip: "10.0.0.2",
  #     asn: "65500",
  #     fabric_ports: ["eth1", "eth2"],
  #     interface_list: ["lo", "eth1", "eth2"]
  #   }
  #    ansible.playbook = "server.yml"
  #   end
  # end


end
