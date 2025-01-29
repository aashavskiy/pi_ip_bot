import os
from telegram import Update

# Load environment variable for admin notifications
ADMIN_ID = os.getenv("ADMIN_ID")

# Function to notify admin about any bot usage
async def log_request(update: Update):
    username = update.message.from_user.username or "Unknown"
    user_id = update.message.from_user.id
    command = update.message.text  # Get the command or message

    log_message = f"Bot accessed:\nUsername: @{username}\nUser ID: {user_id}\nCommand: {command}"

    print(f"LOG: {log_message}")  # Print to console for debugging

    if ADMIN_ID:
        try:
            await update.get_bot().send_message(chat_id=ADMIN_ID, text=log_message)
        except Exception as e:
            print(f"ERROR: Failed to send log to admin: {e}")