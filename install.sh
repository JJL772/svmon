#!/bin/bash
set -e 
GREEN="\e[92m"
YELLOW="\e[93m"
RED="\e[91m"

# Non-root mode for pre-req install
if [ $EUID -ne 0 ]; then
	export SVMON_INSTALL_SH_RAN_ALREADY=1;
	pip3 install --user psutil
	echo -e "$RED AUTHENTICATION FOR $USER:"
	sudo -E -k $0
	exit 0
else
	if [ -z $SVMON_INSTALL_SH_RAN_ALREADY ]; then
		echo -e "Please don't run this script as root!"
		exit 1
	fi
	printf "\e[0m"
fi 

function install_thing()
{
	echo -e "\tINSTALL $1  -->  $2"
	mkdir -p `dirname $2`
	cp $1 $2
}

echo "Installing..."
mkdir -p /etc/svmon/
install_thing ./etc/svmon/source_servers.json /etc/svmon/source_servers.json

systemctl daemon-reload