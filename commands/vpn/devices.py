import os
from telegram import Update
from telegram.ext import CallbackContext
from commands.vpn.config import generate_vpn_config
from utils import load_whitelist

VPN_CONFIG_DIR = "/etc/wireguard/clients/"
VPN_WHITELIST_FILE = "vpn_whitelist.txt"

async def add_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    vpn_whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in vpn_whitelist:
        await update.message.reply_text("🚫 You are not authorized to add VPN devices.")
        return

    device_name = f"{username}_device"
    config_path = os.path.join(VPN_CONFIG_DIR, f"{device_name}.conf")

    if os.path.exists(config_path):
        await update.message.reply_text("❌ Device already exists.")
        return

    private_key = "SOME_GENERATED_PRIVATE_KEY"  # Replace with real key generation
    config_path = generate_vpn_config(device_name, private_key)

    await update.message.reply_text(f"✅ VPN configuration generated: `{config_path}`")
    
    # Send file
    with open(config_path, "rb") as file:
        await context.bot.send_document(chat_id=user_id, document=file, filename=f"{device_name}.conf")

async def list_devices(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    vpn_whitelist = load_whitelist(VPN_WHITELIST_FILE)

    if user_id not in vpn_whitelist:
        await update.message.reply_text("🚫 You are not authorized to list VPN devices.")
        return

    devices = os.listdir(VPN_CONFIG_DIR)
    if devices:
        device_list = "\n".join(devices)
        await update.message.reply_text(f"📄 Your VPN devices:\n```\n{device_list}\n```", parse_mode="Markdown")
    else:
        await update.message.reply_text("📂 No VPN devices found.")

async def remove_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    vpn_whitelist = load_whitelist(VPN_WHITELIST_FILE)

    if user_id not in vpn_whitelist:
        await update.message.reply_text("🚫 You are not authorized to remove VPN devices.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("❌ Usage: `/removedevice <device_name>`")
        return

    device_name = args[0]
    config_path = os.path.join(VPN_CONFIG_DIR, f"{device_name}.conf")

    if os.path.exists(config_path):
        os.remove(config_path)
        await update.message.reply_text(f"✅ VPN device `{device_name}` has been removed.")
    else:
        await update.message.reply_text("❌ Device not found.")

async def get_config(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    vpn_whitelist = load_whitelist(VPN_WHITELIST_FILE)

    # ✅ Check if user is approved for VPN
    if user_id not in vpn_whitelist:
        await update.message.reply_text("🚫 You are not authorized to retrieve VPN configurations.")
        return

    args = context.args
    if not args:
        await update.message.reply_text("❌ Usage: `/getconfig <device_name>`")
        return

    device_name = args[0]
    config_path = os.path.join(VPN_CONFIG_DIR, f"{device_name}.conf")

    if os.path.exists(config_path):
        with open(config_path, "rb") as file:
            await context.bot.send_document(chat_id=user_id, document=file, filename=f"{device_name}.conf")
    else:
        await update.message.reply_text("❌ Device configuration not found.")