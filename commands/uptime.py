import time
from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu
from logger import log_request  # Import logging function

# Store the bot start time
BOT_START_TIME = time.time()

# Function to get uptime
def get_uptime():
    uptime_seconds = int(time.time() - BOT_START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"⏳ Uptime: {hours}h {minutes}m {seconds}s"

# Command handler for /uptime
async def uptime_command(update: Update, context: CallbackContext) -> None:
    await log_request(update)  # Log the request
    uptime_text = get_uptime()
    reply_markup = get_main_menu()
    await update.message.reply_text(uptime_text, reply_markup=reply_markup)