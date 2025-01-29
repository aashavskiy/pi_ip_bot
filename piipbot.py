import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # Get admin ID from .env

# Whitelist file path
WHITELIST_FILE = "whitelist.txt"

# Function to load whitelisted usernames
def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return set()
    with open(WHITELIST_FILE, "r") as f:
        return {line.strip().lower() for line in f}  # Convert to lowercase for case-insensitive matching

WHITELIST = load_whitelist()

# Function to get the public IP address
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text")
        return response.text
    except Exception as e:
        return f"Error retrieving IP: {e}"

# Notify admin when someone accesses the bot
async def notify_admin(update: Update):
    username = update.message.from_user.username or "Unknown"
    user_id = update.message.from_user.id

    message = f"Bot accessed by:\nUsername: @{username}\nUser ID: {user_id}"
    if ADMIN_ID:
        await update.get_bot().send_message(chat_id=ADMIN_ID, text=message)

# Command handler for /ip command
async def ip_command(update: Update, context: CallbackContext) -> None:
    username = update.message.from_user.username  # Get Telegram username

    if not username:
        await update.message.reply_text("Access denied: Username is missing. Please set a Telegram username.")
        return

    if username.lower() not in WHITELIST:
        await update.message.reply_text("Access denied.")
        return

    # Notify admin about access
    await notify_admin(update)

    # Get public IP
    ip_address = get_public_ip()
    await update.message.reply_text(f"Your public IP address: {ip_address}")

# Main function to start the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ip", ip_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()