# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/start.py

import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from commands.menu import get_main_menu
from bot_utils import is_user_authorized, request_approval

async def start_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    logging.info(f"Checking authorization for user ID: {user_id}, Username: {username}")

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await update.message.reply_text(
        "👋 Welcome to Pi IP Bot! Use the menu to select a command.",
        reply_markup=ReplyKeyboardRemove()
    )
    
    # ✅ Fixed: Pass `user_id` to `get_main_menu()`
    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=get_main_menu(user_id)
    )