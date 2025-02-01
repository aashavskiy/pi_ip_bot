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
    
    # Use a helper script to add device to wg0.conf and restart WireGuard
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'helper_script.sh')
    subprocess.run(["sudo", script_path, "add", username, device_name])
    
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
        # Use a helper script to remove device from wg0.conf and restart WireGuard
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'helper_script.sh')
        subprocess.run(["sudo", script_path, "remove", username, device_name])
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
