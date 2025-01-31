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

async def get_config(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to retrieve VPN configurations.")
        return

    if not context.args or len(context.args) == 0:
        await update.message.reply_text("❌ Please specify a device name.")
        return

    device_name = context.args[0]
    config_path = os.path.join(VPN_CONFIG_DIR, f"{username}_{device_name}.conf")

    if not os.path.exists(config_path):
        await update.message.reply_text("⚠ Device configuration not found.")
        return
    
    await update.message.reply_text(f"📥 Sending VPN configuration for `{device_name}`...")
    await context.bot.send_document(chat_id=user_id, document=open(config_path, "rb"), filename=f"{device_name}.conf")

async def list_devices(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to view VPN devices.")
        return
    
    device_files = [f for f in os.listdir(VPN_CONFIG_DIR) if f.startswith(username)]
    if not device_files:
        await update.message.reply_text("📄 You have no registered VPN devices.")
    else:
        device_list = "\n".join([f"- {d}" for d in device_files])
        await update.message.reply_text(f"📄 Your VPN devices:\n{device_list}")

async def remove_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to remove VPN devices.")
        return

    if not context.args or len(context.args) == 0:
        await update.message.reply_text("❌ Please specify a device name to remove.")
        return

    device_name = context.args[0]
    device_config_path = os.path.join(VPN_CONFIG_DIR, f"{username}_{device_name}.conf")

    if not os.path.exists(device_config_path):
        await update.message.reply_text("⚠ Device not found.")
        return
    
    os.remove(device_config_path)
    await update.message.reply_text(f"✅ VPN device `{device_name}` removed successfully.")
