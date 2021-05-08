#!/bin/bash

# clean
sudo rm -f /tmp/usb-lockdown.log
sudo rm -vf /usr/local/bin/usb-*
sudo cp -v etc/udev/rules.d/* /etc/udev/rules.d

# copy to local
sudo cp -v usr/local/bin/* /usr/local/bin
sudo cp -v etc/udev/rules.d/* /etc/udev/rules.d

# restart udev service
sudo systemctl restart udev
