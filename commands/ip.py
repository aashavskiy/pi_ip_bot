import requests
from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu  # Import menu function
from logger import log_request  # Import logging function

# Function to get the public IP address
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text")
        return response.text
    except Exception as e:
        return f"Error retrieving IP: {e}"

# Command handler for /ip
async def ip_command(update: Update, context: CallbackContext) -> None:
    await log_request(update)  # Log the request
    ip_address = get_public_ip()
    reply_markup = get_main_menu()
    await update.message.reply_text(f"Your public IP address: {ip_address}", reply_markup=reply_markup)