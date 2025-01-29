import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to get the public IP address
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=text")
        return response.text
    except Exception as e:
        return f"Error retrieving IP: {e}"

# Command handler for /ip command
async def ip_command(update: Update, context: CallbackContext) -> None:
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