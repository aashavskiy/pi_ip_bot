from telegram import Update
from telegram.ext import CallbackContext
from utils import add_to_whitelist, WHITELIST
import os

ADMIN_ID = os.getenv("ADMIN_ID")

# Function to handle admin approvals via inline buttons
async def handle_approval(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Acknowledge button press

    callback_data = query.data
    message_text = query.message.text or ""

    if callback_data.startswith("approve_"):
        user_id = callback_data.split("_")[1]

        # Ensure the message has enough lines before extracting username
        message_lines = message_text.split("\n")
        if len(message_lines) < 2 or ": " not in message_lines[1]:
            await query.message.reply_text("❌ Error: Unable to extract username from the request.")
            return

        username = message_lines[1].split(": ")[1]  # Extract username
        add_to_whitelist(user_id, username)

        await query.edit_message_text(f"✅ User {username} ({user_id}) has been added to the whitelist.")
    
    elif callback_data.startswith("deny_"):
        user_id = callback_data.split("_")[1]
        await query.edit_message_text(f"❌ User {user_id} was denied access.")