import os
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot_utils import VPN_WHITELIST_FILE, load_whitelist
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SERVER_PUBLIC_KEY = os.getenv("SERVER_PUBLIC_KEY")
SERVER_IP = os.getenv("SERVER_IP")

if not SERVER_PUBLIC_KEY:
    raise ValueError("SERVER_PUBLIC_KEY is not set in the .env file")

def save_whitelist(filename, data):
    with open(filename, "a") as file:
        file.write(data + "\n")

DEVICE_LIST_DIR = "device_lists"
VPN_CONFIG_DIR = "/etc/wireguard/clients"

def get_device_list_file(username):
    return os.path.join(DEVICE_LIST_DIR, f"devices.{username}.txt")

def get_next_ip():
    # Call a helper script to get the next available IP address
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'get_next_ip.sh')
    result = subprocess.check_output(["sudo", script_path]).strip().decode('utf-8')
    return result

def save_device_list(filename, username, device_name, remove=False):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if remove:
        with open(filename, "r") as file:
            lines = file.readlines()
        with open(filename, "w") as file:
            for line in lines:
                if line.strip() != f"{username}_{device_name}":
                    file.write(line)
    else:
        with open(filename, "a") as file:
            file.write(f"{username}_{device_name}\n")

async def list_devices(update: Update, context: CallbackContext) -> None:
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
        keyboard = [[InlineKeyboardButton(device, callback_data=f"remove_device:{device}") for device in user_devices]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("📋 Your devices:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("❌ No devices found.")

async def add_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"
    if len(context.args) == 0:
        await update.message.reply_text("❌ Please specify a device name.")
        return
    device_name = context.args[0]

    # Generate a new key pair for the device
    private_key = subprocess.check_output(["wg", "genkey"]).strip().decode('utf-8')
    public_key = subprocess.check_output(["wg", "pubkey"], input=private_key.encode('utf-8')).strip().decode('utf-8')

    # Get the next available IP address
    device_ip = get_next_ip()

    device_config = os.path.join(VPN_CONFIG_DIR, f"{username}_{device_name}.conf")
    with open(device_config, "w") as f:
        f.write(f"[Interface]\nPrivateKey = {private_key}\nAddress = {device_ip}/24\n\n[Peer]\nPublicKey = {SERVER_PUBLIC_KEY}\nEndpoint = {SERVER_IP}:51820\nAllowedIPs = 0.0.0.0/0, ::/0\n")
    save_whitelist(VPN_WHITELIST_FILE, f"{username} {device_name}")
    
    # Use a helper script to add device to wg0.conf and restart WireGuard
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'helper_script.sh')
    subprocess.run(["sudo", script_path, "add", username, device_name, public_key, device_ip])
    
    await update.message.reply_document(open(device_config, "rb"), filename=f"{username}_{device_name}.conf")

async def remove_device(update: Update, context: CallbackContext) -> None:
    if update.message:
        user_id = str(update.message.from_user.id)
        username = update.message.from_user.username or f"User_{user_id}"
        reply_func = update.message.reply_text
    elif update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        username = update.callback_query.from_user.username or f"User_{user_id}"
        reply_func = update.callback_query.message.reply_text
    else:
        return

    if context.args is None or len(context.args) == 0:
        await reply_func("❌ Please specify a device name to remove.")
        return
    device_name = context.args[0]
    device_config = os.path.join(VPN_CONFIG_DIR, f"{username}_{device_name}.conf")
    if os.path.exists(device_config):
        os.remove(device_config)
        
        # Remove device from whitelist
        if os.path.exists(VPN_WHITELIST_FILE):
            with open(VPN_WHITELIST_FILE, "r") as file:
                lines = file.readlines()
            with open(VPN_WHITELIST_FILE, "w") as file:
                for line in lines:
                    if line.strip() != f"{username} {device_name}":
                        file.write(line)
        
        # Use a helper script to remove device from wg0.conf and restart WireGuard
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'helper_script.sh')
        subprocess.run(["sudo", script_path, "remove", username, device_name])
        await reply_func(f"✅ Device {device_name} removed and WireGuard restarted.")
    else:
        await reply_func("❌ Device not found.")

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
