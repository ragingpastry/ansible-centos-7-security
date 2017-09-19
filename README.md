#CentOS 7 Security
=========

This role will configure a CentOS7 system with a hardened baseline based on the CentOS7 DISA STIGs

Requirements
------------
This role has no external requirements.

Role Variables
--------------

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: centos-7-security, x: 42 }

Testing
-------

This role is tested again a vagrant box that can be built with packer. The vagrant box that this role expects can be found here: https://github.com/ragingpastry/oscap-cent7-stig-disa

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