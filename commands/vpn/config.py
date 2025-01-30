import os

# WireGuard configuration paths
WIREGUARD_DIR = "/etc/wireguard"
SERVER_PUBLIC_KEY_FILE = f"{WIREGUARD_DIR}/server_public.key"
SERVER_PRIVATE_KEY_FILE = f"{WIREGUARD_DIR}/server_private.key"
CLIENTS_DIR = f"{WIREGUARD_DIR}/clients"
WG_CONFIG_PATH = f"{WIREGUARD_DIR}/wg0.conf"

# Network configuration
SERVER_IP = "ashavskiy.keenetic.name"  # ✅ Replace with your actual server domain or IP
VPN_SUBNET = "10.0.0.0/24"
DNS_SERVER = "1.1.1.1"

def generate_vpn_config(username, device_name):
    """Generate a WireGuard configuration file for a user."""
    
    # Generate client private and public keys
    client_private_key = os.popen("wg genkey").read().strip()
    client_public_key = os.popen(f"echo '{client_private_key}' | wg pubkey").read().strip()

    # Read the server's public key
    with open(SERVER_PUBLIC_KEY_FILE, "r") as f:
        server_public_key = f.read().strip()

    # Determine the next available IP
    assigned_ips = get_assigned_ips()
    client_ip = get_next_available_ip(assigned_ips)

    # Create WireGuard client configuration
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

    # Ensure the clients directory exists
    os.system(f"sudo mkdir -p {CLIENTS_DIR}")

    # Save configuration file
    config_path = f"{CLIENTS_DIR}/{username}_{device_name}.conf"
    with open(config_path, "w") as f:
        f.write(config_content)

    # Set correct permissions for the client config
    os.system(f"sudo chmod 600 {config_path}")

    # Add the client to WireGuard server
    add_client_to_wg(username, client_public_key, client_ip)

    print(f"✅ VPN configuration generated: {config_path}")
    return config_path

def get_assigned_ips():
    """Retrieve all currently assigned client IPs."""
    assigned_ips = set()
    if not os.path.exists(CLIENTS_DIR):
        os.system(f"sudo mkdir -p {CLIENTS_DIR}")  # Ensure the directory exists

    for filename in os.listdir(CLIENTS_DIR):
        if filename.endswith(".conf"):
            with open(os.path.join(CLIENTS_DIR, filename), "r") as f:
                for line in f:
                    if line.startswith("Address = "):
                        assigned_ips.add(line.split(" = ")[1].strip().split("/")[0])
    return assigned_ips

def get_next_available_ip(assigned_ips):
    """Find the next available IP address in the VPN subnet."""
    base_ip = "10.0.0."
    for i in range(2, 255):  # Start from 10.0.0.2
        candidate_ip = f"{base_ip}{i}"
        if candidate_ip not in assigned_ips:
            return candidate_ip
    raise ValueError("⚠️ No available IPs left in the VPN subnet!")

def add_client_to_wg(username, client_public_key, client_ip):
    """Add a new WireGuard client to the server configuration and restart WireGuard."""
    
    # Append new client to WireGuard config using sudo
    peer_config = f"""
# {username}
[Peer]
PublicKey = {client_public_key}
AllowedIPs = {client_ip}/32
"""
    
    # Append the new peer entry using sudo
    os.system(f"echo '{peer_config}' | sudo tee -a {WG_CONFIG_PATH} > /dev/null")

    # Restart WireGuard to apply changes
    os.system("sudo systemctl restart wg-quick@wg0")

    print(f"✅ Client {username} added to WireGuard with IP {client_ip}")
    print("🔄 WireGuard restarted successfully!")