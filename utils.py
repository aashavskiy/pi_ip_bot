import os
from telegram import Update

# Load admin ID
ADMIN_ID = os.getenv("ADMIN_ID")

# Function to check if user is allowed
def is_user_allowed(update: Update):
    username = update.message.from_user.username
    if not username:
        return False

    # Load whitelisted usernames
    with open("whitelist.txt", "r") as f:
        whitelist = {line.strip().lower() for line in f}

    return username.lower() in whitelist

# Function to notify admin
async def notify_admin(update: Update):
    username = update.message.from_user.username or "Unknown"
    user_id = update.message.from_user.id

    message = f"Bot accessed by:\nUsername: @{username}\nUser ID: {user_id}"
    if ADMIN_ID:
        await update.get_bot().send_message(chat_id=ADMIN_ID, text=message)