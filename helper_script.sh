#!/bin/bash

ACTION=$1
USERNAME=$2
DEVICE_NAME=$3
PUBLIC_KEY=$4
DEVICE_IP=$5
WG_CONFIG_FILE="/etc/wireguard/wg0.conf"

validate_config() {
    wg-quick checkconf wg0 2>&1 | tee /tmp/wg_checkconf_output.log
    if [ $? -ne 0 ]; then
        echo "Invalid WireGuard configuration. Aborting."
        cat /tmp/wg_checkconf_output.log
        exit 1
    fi
}

validate_ip() {
    if [[ ! $DEVICE_IP =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]]; then
        echo "Invalid IP address format. Aborting."
        exit 1
    fi
}

if [ "$ACTION" == "add" ]; then
    validate_ip
    echo -e "\n# ${USERNAME}_${DEVICE_NAME}\n[Peer]\nPublicKey = ${PUBLIC_KEY}\nAllowedIPs = ${DEVICE_IP}/32" >> $WG_CONFIG_FILE
    validate_config
elif [ "$ACTION" == "remove" ]; then
    sed -i "/# ${USERNAME}_${DEVICE_NAME}/,/^$/d" $WG_CONFIG_FILE
    validate_config
fi

# Restart WireGuard
systemctl restart wg-quick@wg0
if [ $? -ne 0 ]; then
    echo "Failed to restart WireGuard. Check the configuration and try again."
    exit 1
fi
