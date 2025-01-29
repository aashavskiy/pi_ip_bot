from datetime import datetime
from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu  # Import menu function

# Command handler for /time
async def time_command(update: Update, context: CallbackContext) -> None:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time
    reply_markup = get_main_menu()  # Keep the menu visible
    await update.message.reply_text(f"Current time: {current_time}", reply_markup=reply_markup)