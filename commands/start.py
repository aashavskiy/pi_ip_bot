from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from commands.menu import get_main_menu
from logger import log_request

async def start_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    await log_request(user_id, username, "/start")

    await update.message.reply_text(
        "👋 Welcome to Pi IP Bot! Use the menu to select a command.",
        reply_markup=ReplyKeyboardRemove()
    )
    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=get_main_menu()
    )