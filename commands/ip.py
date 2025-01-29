import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils import notify_admin, is_user_allowed
from menu import get_main_menu  # Import menu function

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

    # Use the centralized menu
    reply_markup = get_main_menu()
    await update.message.reply_text(f"Your public IP address: {ip_address}", reply_markup=reply_markup)