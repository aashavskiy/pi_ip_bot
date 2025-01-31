import os
import subprocess
from telegram import Update
from telegram.ext import CallbackContext
from utils import VPN_WHITELIST_FILE, load_whitelist, save_whitelist

VPN_CONFIG_DIR = "/etc/wireguard/clients"

def list_devices(username: str):
    user_devices = []
    if os.path.exists(VPN_WHITELIST_FILE):
        with open(VPN_WHITELIST_FILE, "r") as file:
            for line in file:
                if line.startswith(username):
                    parts = line.strip().split()
                    if len(parts) > 1:
                        user_devices.append(parts[1])
    return user_devices

async def add_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"
    if len(context.args) == 0:
        await update.message.reply_text("❌ Please specify a device name.")
        return
    device_name = context.args[0]
    device_config = os.path.join(VPN_CONFIG_DIR, f"{username}_{device_name}.conf")
    with open(device_config, "w") as f:
        f.write(f"[Interface]\nPrivateKey = PLACEHOLDER\nAddress = 10.0.0.X/24\n\n[Peer]\nPublicKey = SERVER_PUBLIC_KEY\nEndpoint = SERVER_IP:51820\nAllowedIPs = 0.0.0.0/0, ::/0\n")
    save_whitelist(VPN_WHITELIST_FILE, f"{username} {device_name}")
    await update.message.reply_document(open(device_config, "rb"), filename=f"{username}_{device_name}.conf")

async def remove_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"
    if len(context.args) == 0:
        await update.message.reply_text("❌ Please specify a device name to remove.")
        return
    device_name = context.args[0]
    device_config = os.path.join(VPN_CONFIG_DIR, f"{username}_{device_name}.conf")
    if os.path.exists(device_config):
        os.remove(device_config)
        await update.message.reply_text(f"✅ Device {device_name} removed.")
    else:
        await update.message.reply_text("❌ Device not found.")

async def get_config(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"
    if len(context.args) == 0:
        await update.message.reply_text("❌ Please specify a device name.")
        return
    device_name = context.args[0]
    device_config = os.path.join(VPN_CONFIG_DIR, f"{username}_{device_name}.conf")
    if os.path.exists(device_config):
        await update.message.reply_document(open(device_config, "rb"), filename=f"{username}_{device_name}.conf")
    else:
        await update.message.reply_text("❌ Configuration file not found.")