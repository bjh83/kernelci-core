#!/bin/bash

set -e

# Network management
if [ -e /lib/systemd/system/systemd-networkd.service ]; then
    systemctl enable systemd-networkd
fi
# DNS resolving
if [ -e /lib/systemd/system/systemd-resolved.service ]; then
    systemctl enable systemd-resolved
fi
# NTP client
if [ -e /lib/systemd/system/systemd-timesyncd.service ]; then
    systemctl enable systemd-timesyncd
fi

ln -sf /lib/systemd/resolv.conf /etc/resolv.conf
