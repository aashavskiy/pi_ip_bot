import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler
from commands.ip import ip_command
from commands.start import start_command

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Main function to start the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("ip", ip_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()