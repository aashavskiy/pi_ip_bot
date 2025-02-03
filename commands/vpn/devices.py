import os
import subprocess
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot_utils import save_device_list, load_device_list
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
SERVER_PUBLIC_KEY = os.getenv("SERVER_PUBLIC_KEY")
SERVER_IP = os.getenv("SERVER_IP")
BOT_NAME = os.getenv("BOT_NAME", "pi_ip_bot")
SERVER_COUNTRY = os.getenv("SERVER_COUNTRY", "unknown")

if not SERVER_PUBLIC_KEY:
    raise ValueError("SERVER_PUBLIC_KEY is not set in the .env file")

DEVICE_LIST_DIR = "device_lists"

if not os.path.exists(DEVICE_LIST_DIR):
    os.makedirs(DEVICE_LIST_DIR)

def get_device_list_file(username):
    return os.path.join(DEVICE_LIST_DIR, f"devices.{username}.txt")

VPN_CONFIG_DIR = "/etc/wireguard/clients"

def get_next_ip():
    # Call a helper script to get the next available IP address
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'get_next_ip.sh')
    result = subprocess.check_output(["sudo", script_path]).strip().decode('utf-8')
    return result

async def list_devices(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"
    device_list_file = get_device_list_file(username)
    user_devices = load_device_list(device_list_file, username)
    if user_devices:
        keyboard = [[InlineKeyboardButton(f"Delete {device}", callback_data=f"remove_device:{device}") for device in user_devices]]
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

    formatted_device_name = f"{username}_{device_name}_{BOT_NAME}_{SERVER_COUNTRY}"
    logging.info(f"Adding device with name: {formatted_device_name}")
    device_config = os.path.join(VPN_CONFIG_DIR, f"{formatted_device_name}.conf")
    logging.info(f"Device config path: {device_config}")
    with open(device_config, "w") as f:
        f.write(f"[Interface]\nPrivateKey = {private_key}\nAddress = {device_ip}/24\n\n[Peer]\nPublicKey = {SERVER_PUBLIC_KEY}\nEndpoint = {SERVER_IP}:51820\nAllowedIPs = 0.0.0.0/0, ::/0\n")
    device_list_file = get_device_list_file(username)
    save_device_list(device_list_file, username, formatted_device_name)
    
    # Use a helper script to add device to wg0.conf and restart WireGuard
    script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'helper_script.sh')
    subprocess.run(["sudo", script_path, "add", username, formatted_device_name, public_key, device_ip])
    
    await update.message.reply_document(open(device_config, "rb"), filename=f"{formatted_device_name}.conf")

async def remove_device(update: Update, context: CallbackContext) -> None:
    if update.message:
        user_id = str(update.message.from_user.id)
        username = update.message.from_user.username or f"User_{user_id}"
        reply_func = update.message.reply_text
        device_name = context.args[0] if context.args else None
    elif update.callback_query:
        user_id = str(update.callback_query.from_user.id)
        username = update.callback_query.from_user.username or f"User_{user_id}"
        reply_func = update.callback_query.message.reply_text
        device_name = update.callback_query.data.split(":")[1]
    else:
        return

    if not device_name:
        await reply_func("❌ Please specify a device name to remove.")
        return

    formatted_device_name = f"{username}_{device_name}_{BOT_NAME}_{SERVER_COUNTRY}"
    logging.info(f"Removing device with name: {formatted_device_name}")
    device_config = os.path.join(VPN_CONFIG_DIR, f"{formatted_device_name}.conf")
    logging.info(f"Device config path: {device_config}")
    
    if os.path.exists(device_config):
        os.remove(device_config)
        
        # Remove device from device list
        device_list_file = get_device_list_file(username)
        save_device_list(device_list_file, username, formatted_device_name, remove=True)
        
        # Use a helper script to remove device from wg0.conf and restart WireGuard
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'helper_script.sh')
        subprocess.run(["sudo", script_path, "remove", username, formatted_device_name])
        await reply_func(f"✅ Device {formatted_device_name} removed and WireGuard restarted.")
    else:
        logging.error(f"Device config not found: {device_config}")
        await reply_func("❌ Device not found.")

async def get_config(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"
    if len(context.args) == 0:
        await update.message.reply_text("❌ Please specify a device name.")
        return
    device_name = context.args[0]
    formatted_device_name = f"{username}_{device_name}_{BOT_NAME}_{SERVER_COUNTRY}"
    device_config = os.path.join(VPN_CONFIG_DIR, f"{formatted_device_name}.conf")
    logging.info(f"Device config path: {device_config}")
    if os.path.exists(device_config):
        await update.message.reply_document(open(device_config, "rb"), filename=f"{formatted_device_name}.conf")
    else:
        logging.error(f"Device config not found: {device_config}")
        await update.message.reply_text("❌ Configuration file not found.")

async def show_devices_for_removal(update: Update, context):
    user_id = str(update.message.from_user.id)
    if not is_user_authorized(user_id):
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    username = update.message.from_user.username or f"User_{user_id}"
    device_list_file = get_device_list_file(username)
    devices = load_device_list(device_list_file, username)
    
    if not devices:
        await update.message.reply_text("No devices found.")
        return

    keyboard = [[InlineKeyboardButton(device, callback_data=f"remove_device:{device}") for device in devices]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select a device to remove:", reply_markup=reply_markup)

async def remove_device(update: Update, context):
    query = update.callback_query
    device_name = query.data.split(":")[1]
    user_id = str(query.from_user.id)
    username = query.from_user.username or f"User_{user_id}"
    
    # Ensure the device name is correctly formatted
    if not device_name.startswith(f"{username}_"):
        device_name = f"{username}_{device_name}"
    
    formatted_device_name = f"{device_name}_{BOT_NAME}_{SERVER_COUNTRY}"
    
    logging.info(f"Removing device with name: {formatted_device_name}")
    device_config = os.path.join(VPN_CONFIG_DIR, f"{formatted_device_name}.conf")
    logging.info(f"Device config path: {device_config}")
    
    if os.path.exists(device_config):
        os.remove(device_config)
        
        # Remove device from device list
        device_list_file = get_device_list_file(username)
        save_device_list(device_list_file, username, formatted_device_name, remove=True)
        
        # Use a helper script to remove device from wg0.conf and restart WireGuard
        script_path = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'helper_script.sh')
        subprocess.run(["sudo", script_path, "remove", username, formatted_device_name])
        await query.answer()
        await query.edit_message_text(text=f"✅ Device {formatted_device_name} removed and WireGuard restarted.")
    else:
        logging.error(f"Device config not found: {device_config}")
        await query.answer()
        await query.edit_message_text(text="❌ Device not found.")
