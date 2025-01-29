from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

# Function to send the command keyboard
async def start_command(update: Update, context: CallbackContext) -> None:
    keyboard = [["/ip", "/start"]]  # Add more commands if needed
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    await update.message.reply_text("Choose a command:", reply_markup=reply_markup)