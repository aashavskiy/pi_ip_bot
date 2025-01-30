import os

VPN_CONFIG_DIR = "/etc/wireguard/clients/"
SERVER_IP = os.getenv("SERVER_IP")  # Load from .env
SERVER_PUBLIC_KEY = os.getenv("SERVER_PUBLIC_KEY")

def generate_vpn_config(device_name, private_key):
    config_content = f"""[Interface]
PrivateKey = {private_key}
Address = 10.0.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = {SERVER_PUBLIC_KEY}
Endpoint = {SERVER_IP}:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"""

    config_path = os.path.join(VPN_CONFIG_DIR, f"{device_name}.conf")
    with open(config_path, "w") as f:
        f.write(config_content)

    return config_path