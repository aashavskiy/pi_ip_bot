# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/uptime.py

import subprocess
from telegram import Update
from telegram.ext import CallbackContext
from bot_utils import is_user_authorized, request_approval
from logger import log_request
from commands.menu import get_main_menu  # Import the main menu function

async def uptime_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await log_request(user_id, username, "/uptime")

    try:
        # Get system uptime
        uptime_output = subprocess.check_output("uptime -p", shell=True).decode().strip()
        response = f"⏳ Server Uptime: `{uptime_output}`"
    except subprocess.CalledProcessError:
        response = "❌ Error: Unable to fetch system uptime."

    # Handle both text and button presses
    if update.callback_query:
        await update.callback_query.message.reply_text(response)
        await update.callback_query.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu())
    elif update.message:
        await update.message.reply_text(response)
        await update.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu())