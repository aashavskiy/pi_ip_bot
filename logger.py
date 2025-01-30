import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from utils import WHITELIST

ADMIN_ID = os.getenv("ADMIN_ID")

# Function to notify admin about bot usage and request approval for unknown users
async def log_request(update: Update):
    username = update.message.from_user.username or "Unknown"
    user_id = update.message.from_user.id
    command = update.message.text  # Get the command or message

    log_message = f"Bot accessed:\nUsername: @{username}\nUser ID: {user_id}\nCommand: {command}"

    print(f"LOG: {log_message}")  # Print to console for debugging

    # If user is not in the whitelist, send approval request with inline buttons
    if str(user_id) not in WHITELIST:
        keyboard = [
            [
                InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ Deny", callback_data=f"deny_{user_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        approval_message = f"🚨 New user request!\n\nUsername: @{username}\nUser ID: {user_id}\n\nApprove or Deny:"
        
        if ADMIN_ID:
            try:
                await update.get_bot().send_message(chat_id=ADMIN_ID, text=approval_message, reply_markup=reply_markup)
            except Exception as e:
                print(f"ERROR: Failed to send admin approval request: {e}")
    else:
        # If user is allowed, send log message to admin
        if ADMIN_ID:
            try:
                await update.get_bot().send_message(chat_id=ADMIN_ID, text=log_message)
            except Exception as e:
                print(f"ERROR: Failed to send log to admin: {e}")