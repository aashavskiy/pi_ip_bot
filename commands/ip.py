import requests
from telegram import Update
from telegram.ext import CallbackContext
from utils import check_whitelist

async def ip_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)

    # ✅ Check whitelist before responding
    if not check_whitelist(user_id):
        await update.message.reply_text("🚫 You are not authorized to use this bot.")
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