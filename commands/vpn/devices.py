from telegram import Update
from telegram.ext import CallbackContext
from commands.vpn.config import generate_vpn_config
import os

async def add_device(update: Update, context: CallbackContext) -> None:
    """Generate a WireGuard configuration for a user's device."""
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"

    if len(context.args) == 0:
        await update.message.reply_text("❌ Usage: /adddevice <device_name>")
        return

    device_name = context.args[0]
    config_path = generate_vpn_config(username, device_name)

    await update.message.reply_text(f"✅ VPN configuration for `{device_name}` generated and sent.")
    await context.bot.send_document(chat_id=user_id, document=open(config_path, "rb"), filename=f"{device_name}.conf")

async def get_config(update: Update, context: CallbackContext) -> None:
    """Send an existing VPN configuration file to the user."""
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"

    if len(context.args) == 0:
        await update.message.reply_text("❌ Usage: /getconfig <device_name>")
        return

    device_name = context.args[0]
    config_path = f"/etc/wireguard/clients/{username}_{device_name}.conf"

    if not os.path.exists(config_path):
        await update.message.reply_text(f"⚠️ No configuration found for `{device_name}`.")
        return

    await update.message.reply_text(f"📂 Sending `{device_name}` configuration.")
    await context.bot.send_document(chat_id=user_id, document=open(config_path, "rb"), filename=f"{device_name}.conf")