from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from utils import add_to_whitelist, WHITELIST
import os

ADMIN_ID = os.getenv("ADMIN_ID")

# Function to handle admin approvals via inline buttons
async def handle_approval(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge button press

    callback_data = query.data
    if callback_data.startswith("approve_"):
        user_id = callback_data.split("_")[1]
        username = query.message.text.split("\n")[1].split(": ")[1]  # Extract username from message
        add_to_whitelist(user_id, username)
        await query.edit_message_text(f"✅ User {username} ({user_id}) has been added to the whitelist.")
    elif callback_data.startswith("deny_"):
        user_id = callback_data.split("_")[1]
        await query.edit_message_text(f"❌ User {user_id} was denied access.")