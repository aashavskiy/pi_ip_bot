# File: commands/menu.py

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, ApplicationBuilder, Application
from bot_utils import is_user_in_vpn_whitelist, is_user_authorized, request_approval
import logging

# Initialize application
application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

# Define states for the conversation
DEVICE_NAME, REMOVE_DEVICE_NAME = range(2)

def get_main_menu():
    return ReplyKeyboardMarkup([
        ["🌐 IP", "⏳ Uptime"],
        ["🔐 VPN"]
    ], resize_keyboard=True, one_time_keyboard=True)

def get_vpn_menu():
    return ReplyKeyboardMarkup([
        ["➕ Add Device", "📋 List Devices"],
        ["🔑 Get Config", "❌ Remove Device"],
        ["🔙 Main Menu"]
    ], resize_keyboard=True, one_time_keyboard=True)

async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        return

    await update.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu())

# Register menu command handler
menu_handler = CommandHandler("menu", menu_command)
application.add_handler(menu_handler)