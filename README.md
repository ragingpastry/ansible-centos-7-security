#CentOS 7 Security
=========

This role will configure a CentOS7 system with a hardened baseline based on the CentOS7 DISA STIGs

Requirements
------------

This role has no external requirements by itself. The testing of those role does depend on various packages. Please see the testing section

Role Variables
--------------

Example Playbook
----------------

    - hosts: servers
      roles:
         - role: ansible-centos-7-security
           

Testing
-------

#### Overview
This role is tested again a vagrant box that can be built with packer. The vagrant box that this role expects can be found here: https://github.com/ragingpastry/oscap-cent7-stig-disa

There are multiple environments in which these tests work. There are defined by molecule and live in molecule/*

There is a workstation environment and a "base" environment available for testing currently. There apply different standards and require different baselines. They also utilize different packer images.


##### Dependencies
1. python-vagrant
2. molecule
3. libvirt
4. qemu-system-x86  
5. vagrant

#### Getting Started
1. Install Depencencies
  - `pip install python-vagrant molecule`
  - `yum install -y libvirt qemu-system-x86`
  - `systemctl enable libvirtd && systemctl start libvirtd`
  - `yum install https://releases.hashicorp.com/vagrant/2.0.0/vagrant_2.0.0_x86_64.rpm`
2. Build Packer images (if required)
  - `git clone https://github.com/ragingpastry/oscap-cent7-stig-disa`
  - `cd oscap-cent7-stig-disa`
  - `packer build packer/<packer image>.json`
3. Add packer images to vagrant
  - `vagrant box add --name centos7-stig-disa`
4. Run tests
  - `tox`

Basically, we just need to make sure that partitioning is correct. The following describes the paritioning in the vagrant box

```
part pv.18 --fstype="lvmpv" --ondisk=vda --size=3000
part /boot --fstype="ext4" --ondisk=vda --size=1000
part pv.11 --fstype="lvmpv" --ondisk=vda --size=1 --grow
volgroup lg_data pv.18
volgroup lg_os pv.11
logvol /  --fstype="xfs" --size=8000 --name=lv_root --vgname=lg_os
logvol /home  --fstype="xfs" --size=1000 --name=lv_home --vgname=lg_data
logvol /tmp  --fstype="xfs" --size=1000 --name=lv_tmp --vgname=lg_os
logvol /var  --fstype="xfs" --size=2000 --name=lv_var --vgname=lg_os
logvol /var/tmp  --fstype="xfs" --size=1000 --name=lv_var_tmp --vgname=lg_os
logvol /var/log  --fstype="xfs" --size=1500 --name=lv_var_log --vgname=lg_os
logvol /var/log/audit  --fstype="xfs" --size=500 --name=lv_var_log_audit --vgname=lg_os
logvol swap  --fstype="swap" --size=1000 --name=lv_swap --vgname=lg_data
```

This role can be tested using `tox`, however we need to make sure the selinux python bindings get included in tox's python environment. This is due to an unfortunate "feature" of ansible currently. 


Tox will attempt to copy /usr/lib64/python2.7/site-packages/selinux into each tox environment. If the selinux python bindings are not installed then this will fail. Ensure `libselinux-python` is installed.

License
-------

BSD

Author Information
------------------

Nick Wilburn
