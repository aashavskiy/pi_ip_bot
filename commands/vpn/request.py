from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from bot_utils import VPN_WHITELIST, add_to_vpn_whitelist
import os

ADMIN_ID = os.getenv("ADMIN_ID")

async def request_vpn(update: Update, context: CallbackContext) -> None:
    """Handle user VPN access requests."""
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or f"User_{user_id}"

    if user_id in VPN_WHITELIST:
        await update.message.reply_text("✅ You already have VPN access.")
        return

    keyboard = [
        [InlineKeyboardButton("✅ Approve", callback_data=f"vpn_approve_{user_id}_{username}")],
        [InlineKeyboardButton("❌ Deny", callback_data=f"vpn_deny_{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=ADMIN_ID, text=f"🚨 New VPN request!\n\nUsername: @{username}\nUser ID: {user_id}", reply_markup=reply_markup)
    await update.message.reply_text("📨 VPN request sent to the admin. Please wait for approval.")