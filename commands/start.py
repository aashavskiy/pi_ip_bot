from telegram import Update
from telegram.ext import CallbackContext
from logger import log_request

async def start_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    await log_request(user_id, username, "/start")  # ✅ Correctly pass all required arguments

    await update.message.reply_text("👋 Welcome to Pi IP Bot! Use the menu to select a command. Chlenotest")