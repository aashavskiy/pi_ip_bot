#!/bin/bash

ip_counter_file="/etc/wireguard/ip_counter.txt"

if [ ! -f "$ip_counter_file" ]; then
    echo "2" > "$ip_counter_file"  # Start from .2 to avoid conflicts with the server
fi

counter=$(cat "$ip_counter_file")
next_ip="10.0.0.$counter"
echo "$next_ip/24"

echo $((counter + 1)) > "$ip_counter_file"
