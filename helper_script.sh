#!/bin/bash

ACTION=$1
USERNAME=$2
DEVICE_NAME=$3
WG_CONFIG_FILE="/etc/wireguard/wg0.conf"

if [ "$ACTION" == "add" ]; then
    echo -e "\n# ${USERNAME}_${DEVICE_NAME}\n[Peer]\nPublicKey = PLACEHOLDER_PUBLIC_KEY\nAllowedIPs = 10.0.0.X/32" >> $WG_CONFIG_FILE
elif [ "$ACTION" == "remove" ]; then
    sed -i "/# ${USERNAME}_${DEVICE_NAME}/,/^$/d" $WG_CONFIG_FILE
fi

# Restart WireGuard
systemctl restart wg-quick@wg0
