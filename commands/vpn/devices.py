import logging
import os
from telegram import Update
from telegram.ext import CallbackContext
from utils import VPN_WHITELIST_FILE, load_whitelist

VPN_CONFIG_DIR = "/etc/wireguard/clients/"  # Directory where VPN client configs are stored

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def list_devices(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to view VPN devices.")
        return
    
    if not os.path.exists(VPN_CONFIG_DIR):
        await update.message.reply_text("⚠ No VPN devices found.")
        return
    
    device_files = [f for f in os.listdir(VPN_CONFIG_DIR) if f.endswith(".conf")]
    user_devices = [f for f in device_files if f.startswith(update.message.from_user.username)]
    
    if not user_devices:
        await update.message.reply_text("📄 You have no registered VPN devices.")
    else:
        device_list = "\n".join([f"- {d}" for d in user_devices])
        await update.message.reply_text(f"📄 Your VPN devices:\n{device_list}")

async def add_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to add VPN devices.")
        return

    await update.message.reply_text("➕ Adding a new device is not implemented yet.")

async def remove_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to remove VPN devices.")
        return

    if not context.args or len(context.args) == 0:
        await update.message.reply_text("❌ Please specify the device name to remove.")
        return

    device_name = context.args[0]
    device_path = os.path.join(VPN_CONFIG_DIR, f"{device_name}.conf")
    
    if os.path.exists(device_path):
        os.remove(device_path)
        await update.message.reply_text(f"✅ Device {device_name} removed successfully.")
    else:
        await update.message.reply_text("⚠ Device not found.")

async def get_config(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to get VPN configs.")
        return

    await update.message.reply_text("📥 Fetching your VPN configuration is not implemented yet.")
