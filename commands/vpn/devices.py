import logging
from telegram import Update
from telegram.ext import CallbackContext
from utils import VPN_WHITELIST_FILE, load_whitelist, save_whitelist

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def list_devices(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to view VPN devices.")
        return

    await update.message.reply_text("📄 Listing your devices is not implemented yet.")

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
    await update.message.reply_text(f"❌ Removing device {device_name} is not implemented yet.")

async def get_config(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    whitelist = load_whitelist(VPN_WHITELIST_FILE)
    if user_id not in whitelist:
        await update.message.reply_text("❌ You are not authorized to get VPN configs.")
        return

    await update.message.reply_text("📥 Fetching your VPN configuration is not implemented yet.")
