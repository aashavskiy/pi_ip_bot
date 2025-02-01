#!/bin/bash

ip_counter_file="/etc/wireguard/ip_counter.txt"

if [ ! -f "$ip_counter_file" ]; then
    echo "2" > "$ip_counter_file"  # Start from .2 to avoid conflicts with the server
fi

if [ ! -w "$ip_counter_file" ]; then
    echo "Error: Cannot write to $ip_counter_file. Check permissions."
    exit 1
fi

counter=$(cat "$ip_counter_file")
if [ -z "$counter" ]; then
    echo "Error: Failed to read counter from $ip_counter_file."
    exit 1
fi

next_ip="10.0.0.$counter"
echo "$next_ip/24"

echo $((counter + 1)) > "$ip_counter_file"
if [ $? -ne 0 ]; then
    echo "Error: Failed to update counter in $ip_counter_file."
    exit 1
fi
