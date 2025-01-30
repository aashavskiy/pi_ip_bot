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

    # Log the actual message format for debugging
    print(f"DEBUG: Received message text -> {message_text}")

    message_lines = message_text.split("\n")
    print(f"DEBUG: Message lines -> {message_lines}")

    if callback_data.startswith("approve_"):
        user_id = callback_data.split("_")[1]

        # Ensure we have enough lines to extract username
        if len(message_lines) < 4:
            await query.message.reply_text("❌ Error: Unable to extract username. Message format is incorrect.")
            return

        username_line = message_lines[2]  # Third line contains username
        print(f"DEBUG: Username line -> {username_line}")

        if "Username: " not in username_line:
            await query.message.reply_text("❌ Error: Username format is incorrect.")
            return

        username = username_line.split("Username: ")[1].strip()
        print(f"DEBUG: Extracted username -> {username}")

        add_to_whitelist(user_id, username)
        await query.edit_message_text(f"✅ User {username} ({user_id}) has been added to the whitelist.")
    
    elif callback_data.startswith("deny_"):
        user_id = callback_data.split("_")[1]
        await query.edit_message_text(f"❌ User {user_id} was denied access.")