import os
from telegram import Update
from telegram.ext import CallbackContext
from commands.vpn.config import generate_vpn_config

CLIENTS_DIR = "/etc/wireguard/clients"
WG_CONFIG_PATH = "/etc/wireguard/wg0.conf"

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
    config_path = f"{CLIENTS_DIR}/{username}_{device_name}.conf"

    if not os.path.exists(config_path):
        await update.message.reply_text(f"⚠️ No configuration found for `{device_name}`.")
        return

    await update.message.reply_text(f"📂 Sending `{device_name}` configuration.")
    await context.bot.send_document(chat_id=user_id, document=open(config_path, "rb"), filename=f"{device_name}.conf")

async def list_devices(update: Update, context: CallbackContext) -> None:
    """List all VPN devices associated with the user."""
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"

    user_files = [f for f in os.listdir(CLIENTS_DIR) if f.startswith(f"{username}_")]

    if not user_files:
        await update.message.reply_text("⚠️ You have no registered VPN devices.")
        return

    device_list = "\n".join(f"- {f.replace(f'{username}_', '').replace('.conf', '')}" for f in user_files)
    await update.message.reply_text(f"🖥 **Your VPN Devices:**\n{device_list}", parse_mode="Markdown")

async def remove_device(update: Update, context: CallbackContext) -> None:
    """Remove a user's device from the VPN configuration."""
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"

    if len(context.args) == 0:
        await update.message.reply_text("❌ Usage: /removedevice <device_name>")
        return

    device_name = context.args[0]
    config_path = f"{CLIENTS_DIR}/{username}_{device_name}.conf"

    if not os.path.exists(config_path):
        await update.message.reply_text(f"⚠️ No configuration found for `{device_name}`.")
        return

    os.remove(config_path)

    # Remove device from WireGuard server configuration
    with open(WG_CONFIG_PATH, "r") as f:
        lines = f.readlines()

    with open(WG_CONFIG_PATH, "w") as f:
        skip = False
        for line in lines:
            if f"AllowedIPs = 10.0.0." in line and username in line:
                skip = True  # Start skipping lines for this device
            elif skip and line.strip() == "":
                skip = False  # Stop skipping after an empty line
            elif not skip:
                f.write(line)

    os.system("sudo systemctl restart wg-quick@wg0")

    await update.message.reply_text(f"🗑 Device `{device_name}` removed from VPN.")