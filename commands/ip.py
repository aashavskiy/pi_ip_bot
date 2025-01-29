import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils import notify_admin, is_user_allowed

# Function to get the public IP address
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text")
        return response.text
    except Exception as e:
        return f"Error retrieving IP: {e}"

# Command handler for /ip
async def ip_command(update: Update, context: CallbackContext) -> None:
    if not is_user_allowed(update):
        await update.message.reply_text("Access denied.")
        return

    await notify_admin(update)
    ip_address = get_public_ip()

    # Keep the buttons visible
    keyboard = [["/ip", "/start"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text(f"Your public IP address: {ip_address}", reply_markup=reply_markup)