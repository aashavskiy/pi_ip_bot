import os

WIREGUARD_DIR = "/etc/wireguard"
SERVER_PUBLIC_KEY_FILE = f"{WIREGUARD_DIR}/server_public.key"
SERVER_PRIVATE_KEY_FILE = f"{WIREGUARD_DIR}/server_private.key"
CLIENTS_DIR = f"{WIREGUARD_DIR}/clients"
SERVER_IP = "ashavskiy.keenetic.name"
VPN_SUBNET = "10.0.0.0/24"
DNS_SERVER = "1.1.1.1"

def generate_vpn_config(username, device_name):
    """Generate a WireGuard config for a user."""
    client_private_key = os.popen("wg genkey").read().strip()
    client_public_key = os.popen(f"echo '{client_private_key}' | wg pubkey").read().strip()

    # Read the server's public key
    with open(SERVER_PUBLIC_KEY_FILE, "r") as f:
        server_public_key = f.read().strip()

    # Determine the next available IP
    assigned_ips = get_assigned_ips()
    client_ip = get_next_available_ip(assigned_ips)

    config_content = f"""[Interface]
PrivateKey = {client_private_key}
Address = {client_ip}/24
DNS = {DNS_SERVER}

[Peer]
PublicKey = {server_public_key}
Endpoint = {SERVER_IP}:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"""
    config_path = f"{CLIENTS_DIR}/{username}_{device_name}.conf"

    with open(config_path, "w") as f:
        f.write(config_content)

    print(f"✅ VPN configuration generated: {config_path}")
    return config_path