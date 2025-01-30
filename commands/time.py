from telegram import Update
from telegram.ext import CallbackContext
from datetime import datetime
from logger import log_request

async def time_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    await log_request(user_id, username, "/time")  # ✅ Now passing all required arguments

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await update.message.reply_text(f"⏰ Current server time: `{current_time}`", parse_mode="Markdown")