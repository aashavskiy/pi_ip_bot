import os
from telegram import Update

# Load admin ID from environment variables
ADMIN_ID = os.getenv("ADMIN_ID")

# Debug print to check if ADMIN_ID is loaded correctly
print(f"Loaded ADMIN_ID: {ADMIN_ID}")

# Function to notify admin about bot usage
async def notify_admin(update: Update):
    username = update.message.from_user.username or "Unknown"
    user_id = update.message.from_user.id

    message = f"Bot accessed by:\nUsername: @{username}\nUser ID: {user_id}"
    
    if not ADMIN_ID:
        print("ADMIN_ID is missing! Notification not sent.")
        return
    
    try:
        await update.get_bot().send_message(chat_id=ADMIN_ID, text=message)
        print("Notification sent to admin.")
    except Exception as e:
        print(f"Error sending notification: {e}")