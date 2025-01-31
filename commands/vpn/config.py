import os

WIREGUARD_DIR = "/etc/wireguard"
CLIENTS_DIR = f"{WIREGUARD_DIR}/clients"
WG_CONFIG_PATH = f"{WIREGUARD_DIR}/wg0.conf"

def generate_vpn_config(username, device_name):
    """Generate a WireGuard configuration file for a user."""
    client_private_key = os.popen("wg genkey").read().strip()
    client_public_key = os.popen(f"echo '{client_private_key}' | wg pubkey").read().strip()

    server_public_key = open(f"{WIREGUARD_DIR}/server_public.key", "r").read().strip()
    client_ip = f"10.0.0.{100 + hash(username) % 100}/24"

    config_content = f"""[Interface]
PrivateKey = {client_private_key}
Address = {client_ip}
DNS = 1.1.1.1

[Peer]
PublicKey = {server_public_key}
Endpoint = ashavskiy.keenetic.name:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"""

    os.system(f"sudo mkdir -p {CLIENTS_DIR}")
    config_path = f"{CLIENTS_DIR}/{username}_{device_name}.conf"

    with open(config_path, "w") as f:
        f.write(config_content)

    os.system(f"sudo chmod 600 {config_path}")
    os.system(f"echo '\n[Peer]\nPublicKey = {client_public_key}\nAllowedIPs = {client_ip}' | sudo tee -a {WG_CONFIG_PATH}")
    os.system("sudo systemctl restart wg-quick@wg0")

    return config_path