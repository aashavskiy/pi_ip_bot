import requests
from telegram import Update
from telegram.ext import CallbackContext
from bot_utils import is_user_authorized, request_approval

async def ip_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await update.message.reply_text("📡 Fetching your IP address...")

    try:
        response = requests.get("https://api64.ipify.org?format=json", timeout=5)
        response.raise_for_status()  # Raise an error for bad responses
        ip_data = response.json()
        public_ip = ip_data.get("ip", "Unknown")

        await update.message.reply_text(f"🌐 Your public IP address: `{public_ip}`", parse_mode="Markdown")
    except requests.RequestException:
        await update.message.reply_text("⚠️ Error: Unable to fetch public IP.")