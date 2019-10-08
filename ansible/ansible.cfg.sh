#!/bin/bash

ansibleDefaultPath=/etc/ansible

if [ -d $ansibleDefaultPath ]; then
	echo "$ansibleDefaultPath Directory Exist"
else
	mkdir $ansibleDefaultPath
	mkdir $ansibleDefaultPath/inventory
fi

cd $ansibleDefaultPath

if [ -e ansible.cfg ]; then
	echo "ansible.cfg Exist"
else
	touch ansible.cfg
fi

cat << EOF > /etc/ansible/ansible.cfg
[defaults]
inventory = inventory/hosts
remote_user = ec2-user
become = true
become_method = sudo
become_user = root
library = library
EOF
