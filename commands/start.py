from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu
from logger import log_request  # Import logging function

# Command handler for /start
async def start_command(update: Update, context: CallbackContext) -> None:
    await log_request(update)  # Log the request
    reply_markup = get_main_menu()
    await update.message.reply_text("Choose a command:", reply_markup=reply_markup)