# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/ip.py

import subprocess
from telegram import Update
from telegram.ext import CallbackContext

# Function to handle the IP command
async def ip_command(update: Update, context: CallbackContext) -> None:
    try:
        # Get external IP using `curl` (or another way to get public IP)
        ip_address = subprocess.check_output(["curl", "-s", "https://api.ipify.org"]).decode("utf-8")
        await update.message.reply_text(f"Your IP address is: {ip_address}")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text("❌ Unable to fetch the IP address.")