from telegram import Update
from telegram.ext import CallbackContext
from utils import check_whitelist  # ✅ Import from utils.py

async def ip_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)

    # ✅ Check whitelist before responding
    if not check_whitelist(user_id):
        await update.message.reply_text("🚫 You are not authorized to use this bot.")
        return

    await update.message.reply_text("📡 Fetching your IP address... (This is just a placeholder)")