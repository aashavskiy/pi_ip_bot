from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu  # Import menu function

# Command handler for /start
async def start_command(update: Update, context: CallbackContext) -> None:
    reply_markup = get_main_menu()  # Get the keyboard from menu.py
    await update.message.reply_text("Choose a command:", reply_markup=reply_markup)