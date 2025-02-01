#!/bin/bash

ACTION=$1
USERNAME=$2
DEVICE_NAME=$3
WG_CONFIG_FILE="/etc/wireguard/wg0.conf"

validate_config() {
    wg-quick checkconf $WG_CONFIG_FILE
    if [ $? -ne 0 ]; then
        echo "Invalid WireGuard configuration. Aborting."
        exit 1
    fi
}

if [ "$ACTION" == "add" ]; then
    echo -e "\n# ${USERNAME}_${DEVICE_NAME}\n[Peer]\nPublicKey = PLACEHOLDER_PUBLIC_KEY\nAllowedIPs = 10.0.0.X/32" >> $WG_CONFIG_FILE
    validate_config
elif [ "$ACTION" == "remove" ]; then
    sed -i "/# ${USERNAME}_${DEVICE_NAME}/,/^$/d" $WG_CONFIG_FILE
    validate_config
fi

# Restart WireGuard
systemctl restart wg-quick@wg0
