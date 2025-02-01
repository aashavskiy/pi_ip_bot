import os
import subprocess
from telegram import Update
from telegram.ext import CallbackContext
from utils import VPN_WHITELIST_FILE, load_whitelist

def save_whitelist(filename, data):
    with open(filename, "a") as file:
        file.write(data + "\n")

VPN_CONFIG_DIR = "/etc/wireguard/clients"

async def list_devices(update: Update, context):
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"
    user_devices = []
    if os.path.exists(VPN_WHITELIST_FILE):
        with open(VPN_WHITELIST_FILE, "r") as file:
            for line in file:
                if line.startswith(username):
                    parts = line.strip().split()
                    if len(parts) > 1:
                        user_devices.append(parts[1])
    if user_devices:
        await update.message.reply_text(f"📋 Your devices:\n" + "\n".join(user_devices))
    else:
        await update.message.reply_text("❌ No devices found.")

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
    
    # Add device to wg0.conf
    wg_config_file = "/etc/wireguard/wg0.conf"
    with open(wg_config_file, "a") as file:
        file.write(f"\n# {username}_{device_name}\n[Peer]\nPublicKey = PLACEHOLDER_PUBLIC_KEY\nAllowedIPs = 10.0.0.X/32\n")
    
    # Restart WireGuard
    subprocess.run(["sudo", "systemctl", "restart", "wg-quick@wg0"])
    
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
        # Remove device from wg0.conf
        wg_config_file = "/etc/wireguard/wg0.conf"
        with open(wg_config_file, "r") as file:
            lines = file.readlines()
        with open(wg_config_file, "w") as file:
            skip = False
            for line in lines:
                if line.strip() == f"# {username}_{device_name}":
                    skip = True
                elif skip and line.strip() == "":
                    skip = False
                elif not skip:
                    file.write(line)
        # Restart WireGuard
        subprocess.run(["sudo", "systemctl", "restart", "wg-quick@wg0"])
        await update.message.reply_text(f"✅ Device {device_name} removed and WireGuard restarted.")
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
