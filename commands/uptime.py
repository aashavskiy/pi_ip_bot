import time
import os
from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu
from logger import log_request  # Import logging function

# Store the bot start time
BOT_START_TIME = time.time()

# Function to get system uptime
def get_system_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
            hours, remainder = divmod(int(uptime_seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"🖥 Server uptime: {hours}h {minutes}m {seconds}s"
    except Exception as e:
        return f"Error retrieving system uptime: {e}"

# Function to get bot uptime
def get_bot_uptime():
    uptime_seconds = int(time.time() - BOT_START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"🤖 Bot uptime: {hours}h {minutes}m {seconds}s"

# Command handler for /uptime
async def uptime_command(update: Update, context: CallbackContext) -> None:
    await log_request(update)  # Log the request
    system_uptime = get_system_uptime()
    bot_uptime = get_bot_uptime()
    uptime_text = f"{system_uptime}\n{bot_uptime}"
    reply_markup = get_main_menu()
    await update.message.reply_text(uptime_text, reply_markup=reply_markup)