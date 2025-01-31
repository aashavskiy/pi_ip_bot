from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
import os
from utils import load_whitelist

VPN_WHITELIST_FILE = "vpn_whitelist.txt"

async def request_vpn(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    vpn_whitelist = load_whitelist(VPN_WHITELIST_FILE)

    # ✅ Prevent duplicate VPN requests
    if user_id in vpn_whitelist:
        await update.message.reply_text("✅ You are already approved for VPN access.")
        return

    # Send request to admin for approval
    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"vpn_approve_{user_id}_{username}"),
        InlineKeyboardButton("❌ Deny", callback_data=f"vpn_deny_{user_id}")
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send request message to admin
    admin_id = os.getenv("ADMIN_ID")
    if admin_id:
        message = f"🚨 New VPN request!\n\nUsername: @{username}\nUser ID: {user_id}"
        await context.bot.send_message(chat_id=admin_id, text=message, reply_markup=reply_markup)

    await update.message.reply_text("🔄 Your request for VPN access has been sent to the admin.")