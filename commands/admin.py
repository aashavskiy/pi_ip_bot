from telegram import Update
from telegram.ext import CallbackContext
from utils import add_to_whitelist, load_whitelist

BOT_WHITELIST_FILE = "bot_whitelist.txt"

async def handle_approval(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    callback_data = query.data.split("_")
    action = callback_data[1]
    user_id = callback_data[2]
    username = callback_data[3] if action == "approve" else None

    if action == "approve":
        add_to_whitelist(user_id, username, BOT_WHITELIST_FILE)
        await query.edit_message_text(f"✅ User @{username} ({user_id}) has been approved to use the bot.")
        await context.bot.send_message(chat_id=user_id, text="🎉 You have been approved! Use /menu to see available commands.")
    else:
        await query.edit_message_text(f"❌ User {user_id} was denied access.")