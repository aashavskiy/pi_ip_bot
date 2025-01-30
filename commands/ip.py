import requests
from telegram import Update
from telegram.ext import CallbackContext
from logger import log_request
from piipbot import check_whitelist  # Import the whitelist check function

async def ip_command(update: Update, context: CallbackContext) -> None:
    if not await check_whitelist(update):  # ⛔ Stop execution if unauthorized
        return

    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    await log_request(user_id, username, "/ip")  # Log the request

    try:
        # Fetch external IP address
        response = requests.get("https://api64.ipify.org?format=text", timeout=5)
        response.raise_for_status()  # Raise an error for HTTP failures
        public_ip = response.text.strip()

        await update.message.reply_text(f"🌍 Your public IP address is: `{public_ip}`", parse_mode="Markdown")

    except requests.RequestException as e:
        await update.message.reply_text("❌ Error: Unable to fetch the public IP address.")
        print(f"ERROR: Failed to fetch IP - {e}")  # Log the error