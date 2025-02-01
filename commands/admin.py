from telegram import Update
from telegram.ext import CallbackContext
from utils import add_to_whitelist, is_user_authorized, request_approval, BOT_WHITELIST_FILE

async def handle_approval(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username)
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
    else:
        await update.message.reply_text("✅ You are authorized to use this bot.")
        add_to_whitelist(BOT_WHITELIST_FILE, user_id, username)