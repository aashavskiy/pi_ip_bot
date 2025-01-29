from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu
from logger import log_request  # Import logging function

# Command handler for /time
async def time_command(update: Update, context: CallbackContext) -> None:
    await log_request(update)  # Log the request
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reply_markup = get_main_menu()
    await update.message.reply_text(f"Current time: {current_time}", reply_markup=reply_markup)