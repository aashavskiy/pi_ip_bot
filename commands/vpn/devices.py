import logging
import os
import subprocess
from telegram import Update
from telegram.ext import CallbackContext
from utils import VPN_WHITELIST_FILE, load_whitelist

VPN_CONFIG_DIR = "/etc/wireguard/clients/"  # Directory where VPN client configs are stored
WG_CONFIG_PATH = "/etc/wireguard/wg0.conf"  # WireGuard server config
VPN_SUBNET = "10.0.0.0/24"  # Subnet for VPN clients

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_next_available_ip():
    existing_ips = set()
    if os.path.exists(WG_CONFIG_PATH):
        with open(WG_CONFIG_PATH, "r") as f:
            for line in f:
                if "AllowedIPs" in line:
                    ip = line.split()[-1].split("/")[0]
                    existing_ips.add(ip)
    
    for i in range(2, 255):
        new_ip = f"10.0.0.{i}"
        if new_ip not in existing_ips:
            return new_ip
    return None

async def add_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to add VPN devices.")
        return

    if not context.args or len(context.args) == 0:
        await update.message.reply_text("❌ Please specify a device name.")
        return

    device_name = context.args[0]
    device_config_path = os.path.join(VPN_CONFIG_DIR, f"{username}_{device_name}.conf")

    if os.path.exists(device_config_path):
        await update.message.reply_text("⚠ Device already exists.")
        return

    client_private_key = subprocess.run(["wg", "genkey"], capture_output=True, text=True).stdout.strip()
    client_public_key = subprocess.run(["echo", client_private_key, "|", "wg", "pubkey"], capture_output=True, text=True).stdout.strip()
    server_public_key = subprocess.run(["wg", "show", "wg0", "public-key"], capture_output=True, text=True).stdout.strip()
    allocated_ip = get_next_available_ip()

    if not allocated_ip:
        await update.message.reply_text("❌ No available IP addresses.")
        return

    config_content = f"""[Interface]
PrivateKey = {client_private_key}
Address = {allocated_ip}/24
DNS = 1.1.1.1

[Peer]
PublicKey = {server_public_key}
Endpoint = YOUR_SERVER_IP:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"""
    with open(device_config_path, "w") as config_file:
        config_file.write(config_content)

    with open(WG_CONFIG_PATH, "a") as wg_file:
        wg_file.write(f"\n[Peer]\nPublicKey = {client_public_key}\nAllowedIPs = {allocated_ip}/32\n")

    subprocess.run(["sudo", "systemctl", "restart", "wg-quick@wg0"], check=True)

    await update.message.reply_text(f"✅ VPN device `{device_name}` added successfully. Sending configuration...")
    await context.bot.send_document(chat_id=user_id, document=open(device_config_path, "rb"), filename=f"{device_name}.conf")
