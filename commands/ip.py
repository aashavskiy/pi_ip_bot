# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/ip.py

import subprocess
from telegram import Update
from telegram.ext import CallbackContext

# Function to handle the IP command
async def ip_command(update: Update, context: CallbackContext) -> None:
    try:
        # Get external IP using `curl`
        ip_address = subprocess.check_output(["curl", "-s", "https://api.ipify.org"]).decode("utf-8")

        # Handle both command input and button press
        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text(f"Your IP address is: {ip_address}")
        elif update.message:
            await update.message.reply_text(f"Your IP address is: {ip_address}")
    except subprocess.CalledProcessError:
        error_msg = "❌ Unable to fetch the IP address."
        if update.callback_query:
            await update.callback_query.message.reply_text(error_msg)
        elif update.message:
            await update.message.reply_text(error_msg)