import os
import subprocess
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from utils import load_whitelist, add_to_whitelist

VPN_WHITELIST_FILE = "vpn_whitelist.txt"
VPN_CONFIG_DIR = "/etc/wireguard/clients/"

async def request_vpn(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"
    
    vpn_whitelist = load_whitelist(VPN_WHITELIST_FILE)

    # ✅ Prevent duplicate VPN requests
    if user_id in vpn_whitelist:
        await update.message.reply_text("✅ You are already approved for VPN access.")
        return
    
    # Send request to admin for approval
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"vpn_approve_{user_id}_{username}"),
            InlineKeyboardButton("❌ Deny", callback_data=f"vpn_deny_{user_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send request message to admin
    admin_id = os.getenv("ADMIN_ID")
    if admin_id:
        message = f"🚨 New VPN request!\n\nUsername: @{username}\nUser ID: {user_id}"
        await context.bot.send_message(chat_id=admin_id, text=message, reply_markup=reply_markup)
    
    # Confirm request to user
    await update.message.reply_text("🔄 Your request for VPN access has been sent to the admin.")

async def handle_vpn_approval(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split("_")
    action = callback_data[1]
    user_id = callback_data[2]
    username = callback_data[3] if action == "approve" else None

    if action == "approve":
        add_to_whitelist(user_id, username, VPN_WHITELIST_FILE)  # ✅ Ensure user is saved in VPN whitelist

        # ✅ Reload whitelist dynamically
        global VPN_WHITELIST
        VPN_WHITELIST = load_whitelist(VPN_WHITELIST_FILE)

        await query.edit_message_text(f"✅ User @{username} ({user_id}) has been approved for VPN access.")
        await context.bot.send_message(chat_id=user_id, text="🎉 You have been approved for VPN access! Use /menu to see VPN commands.")
    else:
        await query.edit_message_text(f"❌ User {user_id} was denied VPN access.")

async def add_device(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    vpn_whitelist = load_whitelist(VPN_WHITELIST_FILE)

    # ✅ Check if user is approved for VPN
    if user_id not in vpn_whitelist:
        await update.message.reply_text("🚫 You are not authorized to add VPN devices.")
        return

    device_name = f"{username}_device"
    config_path = os.path.join(VPN_CONFIG_DIR, f"{device_name}.conf")

    # Generate VPN config
    config_content = f"""[Interface]
PrivateKey = YOUR_PRIVATE_KEY
Address = 10.0.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = YOUR_SERVER_PUBLIC_KEY
Endpoint = YOUR_SERVER_IP:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
"""

    with open(config_path, "w") as f:
        f.write(config_content)

    await update.message.reply_text(f"✅ VPN configuration generated: `{config_path}`")

async def list_devices(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    vpn_whitelist = load_whitelist(VPN_WHITELIST_FILE)

    # ✅ Check if user is approved for VPN
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

    # ✅ Check if user is approved for VPN
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