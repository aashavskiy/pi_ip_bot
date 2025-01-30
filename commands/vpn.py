import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils import load_whitelist, add_to_whitelist

VPN_WHITELIST_FILE = "vpn_whitelist.txt"
VPN_CONFIG_DIR = "/etc/wireguard/clients/"
SERVER_PUBLIC_KEY_PATH = "/etc/wireguard/server_public.key"
SERVER_HOSTNAME = "ashavskiy.keenetic.name"
WG_INTERFACE = "wg0"
BASE_CLIENT_IP = "10.0.0."

# Ensure VPN directory exists
if not os.path.exists(VPN_CONFIG_DIR):
    os.makedirs(VPN_CONFIG_DIR, exist_ok=True)

# Request VPN Access
async def request_vpn(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if user_id in load_whitelist(VPN_WHITELIST_FILE):
        await update.message.reply_text("✅ You are already approved for VPN access.")
        return

    # Send request to admin
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"vpn_approve_{user_id}_{username}"),
            InlineKeyboardButton("❌ Deny", callback_data=f"vpn_deny_{user_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"🚨 New VPN request!\n\nUsername: @{username}\nUser ID: {user_id}", reply_markup=reply_markup)

# Admin approval callback
async def handle_vpn_approval(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data.split("_")
    action, user_id = data[1], data[2]
    username = data[3] if action == "approve" else None

    if action == "approve":
        add_to_whitelist(user_id, username, VPN_WHITELIST_FILE)
        config_path = generate_vpn_config(username, 1)
        await query.edit_message_text(f"✅ User @{username} ({user_id}) approved for VPN access.")
        await context.bot.send_document(chat_id=user_id, document=open(config_path, "rb"), filename=f"{username}_wireguard.conf")
    else:
        await query.edit_message_text(f"❌ User {user_id} was denied VPN access.")

# Generate WireGuard Configuration
def generate_vpn_config(username, device_number):
    user_private_key = subprocess.check_output("wg genkey", shell=True).decode().strip()
    user_public_key = subprocess.check_output(f"echo {user_private_key} | wg pubkey", shell=True).decode().strip()
    server_public_key = open(SERVER_PUBLIC_KEY_PATH).read().strip()

    # Find next available IP
    client_ip = f"{BASE_CLIENT_IP}{device_number}/24"

    config_filename = f"{username}_{device_number}.conf"
    config_path = os.path.join(VPN_CONFIG_DIR, config_filename)

    config_data = f"""
[Interface]
PrivateKey = {user_private_key}
Address = {client_ip}
DNS = 8.8.8.8

[Peer]
PublicKey = {server_public_key}
Endpoint = {SERVER_HOSTNAME}:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"""

    with open(config_path, "w") as f:
        f.write(config_data)

    subprocess.run(f"sudo wg set {WG_INTERFACE} peer {user_public_key} allowed-ips {client_ip.split('/')[0]}/32", shell=True)

    return config_path

# Add an Additional Device
async def add_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if user_id not in load_whitelist(VPN_WHITELIST_FILE):
        await update.message.reply_text("🚫 You do not have VPN access.")
        return

    device_count = len([f for f in os.listdir(VPN_CONFIG_DIR) if f.startswith(username)]) + 1
    config_path = generate_vpn_config(username, device_count)

    await update.message.reply_text(f"✅ Added new device configuration for @{username}.")
    await update.message.reply_document(document=open(config_path, "rb"), filename=f"{username}_{device_count}_wireguard.conf")

# List Current Devices
async def list_devices(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username or "Unknown"
    devices = [f for f in os.listdir(VPN_CONFIG_DIR) if f.startswith(username)]

    if not devices:
        await update.message.reply_text("🔍 No VPN configurations found for you.")
        return

    device_list = "\n".join(devices)
    await update.message.reply_text(f"🖥 Your VPN Configurations:\n{device_list}")

# Remove a Device Configuration
async def remove_device(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username or "Unknown"
    devices = [f for f in os.listdir(VPN_CONFIG_DIR) if f.startswith(username)]

    if not devices:
        await update.message.reply_text("🔍 No VPN configurations found for you.")
        return

    os.remove(os.path.join(VPN_CONFIG_DIR, devices[-1]))
    await update.message.reply_text(f"🗑 Removed latest device configuration for @{username}.")