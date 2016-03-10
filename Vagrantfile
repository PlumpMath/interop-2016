# -*- mode: ruby -*-
# vi: set ft=ruby :

groups = {
  "spines" => ["spine1"],
  "leafs" => ["leaf1", "leaf2", "leaf3", "leaf4"],
  "servers" => ["ceph1", "ceph2", "ceph3", "ceph-admin"],
  "network:children" => ["spines", "leafs"]
}


Vagrant.configure("2") do |config|

  cumulus_image = "cumulus-vx-2.5.5"
  ceph_image = "ubuntu/precise64"

  config.vm.define "leaf1" do |leaf1| 
   leaf1.vm.box = cumulus_image
   leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine1', auto_config: false
   leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-spine2', auto_config: false
   leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-ceph1', auto_config: false
   leaf1.vm.network "private_network",  virtualbox__intnet: 'leaf1-ceph2', auto_config: false
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
   leaf2.vm.network "private_network",  virtualbox__intnet: 'leaf2-ceph1', auto_config: false
   leaf2.vm.network "private_network",  virtualbox__intnet: 'leaf2-ceph2', auto_config: false
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
   leaf3.vm.network "private_network",  virtualbox__intnet: 'leaf3-ceph3', auto_config: false
   leaf3.vm.network "private_network",  virtualbox__intnet: 'leaf3-ceph_admin', auto_config: false
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
   leaf4.vm.network "private_network",  virtualbox__intnet: 'leaf4-ceph3', auto_config: false
   leaf4.vm.network "private_network",  virtualbox__intnet: 'leaf4-ceph_admin', auto_config: false
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
      ansible.playbook = "spines.yml"
    end
  end

  # config.vm.define "ceph1" do |ceph1| 
  #  ceph1.vm.box = "ubuntu/trusty64"
  #  ceph1.vm.network "private_network",  virtualbox__intnet: 'leaf1-ceph1', auto_config: false
  #  ceph1.vm.network "private_network",  virtualbox__intnet: 'leaf2-ceph1', auto_config: false
  #  ceph1.vm.host_name = "ceph1"
  #  ceph1.vm.provision "ansible" do |ansible|
  #     ansible.groups = groups
  #     ansible.extra_vars = {
  #     loopback_ip: "10.0.0.1",
  #     asn: "65500",
  #     fabric_ports: ["eth1", "eth2"],
  #     interface_list: ["lo", "eth1", "eth2"]
  #   }
  #    ansible.playbook = "ceph.yml"
  #   end
  # end
  
  # config.vm.define "ceph2" do |ceph2| 
  #  ceph2.vm.box = ceph_image
  #  ceph2.vm.network "private_network",  virtualbox__intnet: 'leaf1-ceph2', auto_config: false
  #  ceph2.vm.network "private_network",  virtualbox__intnet: 'leaf2-ceph2', auto_config: false
  #  ceph2.vm.host_name = "ceph2"
  #  ceph2.vm.provision "ansible" do |ansible|
  #     ansible.groups = groups
  #     ansible.extra_vars = {
  #     loopback_ip: "10.0.0.2",
  #     asn: "65500",
  #     fabric_ports: ["eth1", "eth2"],
  #     interface_list: ["lo", "eth1", "eth2"]
  #   }
  #    ansible.playbook = "ceph.yml"
  #   end
  # end

  # config.vm.define "ceph3" do |ceph3| 
  #  ceph3.vm.box = "ubuntu/trusty64"
  #  ceph3.vm.network "private_network",  virtualbox__intnet: 'leaf3-ceph3', auto_config: false
  #  ceph3.vm.network "private_network",  virtualbox__intnet: 'leaf4-ceph3', auto_config: false
  #  ceph3.vm.host_name = "ceph3"
  #  ceph3.vm.provision "ansible" do |ansible|
  #     ansible.groups = groups
  #     ansible.extra_vars = {
  #     loopback_ip: "10.0.0.3",
  #     asn: "65500",
  #     fabric_ports: ["eth1", "eth2"],
  #     interface_list: ["lo", "eth1", "eth2"]
  #   }
  #    ansible.playbook = "ceph.yml"
  #   end
  # end

  # config.vm.define "ceph-admin" do |ceph_admin| 
  #  ceph_admin.vm.box = ceph_image
  #  ceph_admin.vm.network "private_network",  virtualbox__intnet: 'leaf3-ceph_admin', auto_config: false
  #  ceph_admin.vm.network "private_network",  virtualbox__intnet: 'leaf4-ceph_admin', auto_config: false
  #  ceph_admin.vm.host_name = "ceph-admin"
  #  ceph_admin.vm.provision "ansible" do |ansible|
  #     ansible.groups = groups
  #     ansible.extra_vars = {
  #     loopback_ip: "10.0.0.4",
  #     asn: "65500",
  #     fabric_ports: ["eth1", "eth2"],
  #     interface_list: ["lo", "eth1", "eth2"]
  #   }
  #    ansible.playbook = "ceph.yml"
  #   end
  # end
end
