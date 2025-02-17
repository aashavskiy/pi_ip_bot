# /Users/alexanderashavskiy/projects/pi_ip_bot/piipbot.py

import os
import importlib
import logging
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from commands.admin import handle_approval, handle_approval_callback
from commands.start import start_command
from commands.menu import menu_command, handle_menu_buttons, get_main_menu, get_conversation_handler
from bot_utils import is_user_authorized, request_approval

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID is not set in the environment variables.")

# Function to dynamically load command handlers from the "commands" folder
def load_commands():
    commands = {}
    commands_dir = "commands"

    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{commands_dir}.{filename[:-3]}"  # Remove .py extension
            module = importlib.import_module(module_name)

            if hasattr(module, f"{filename[:-3]}_command"):
                commands[filename[:-3]] = getattr(module, f"{filename[:-3]}_command")

    return commands

# Main function to start the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Dynamically load all command handlers
    commands = load_commands()
    for cmd_name, cmd_func in commands.items():
        app.add_handler(CommandHandler(cmd_name, cmd_func))
        print(f"✅ Loaded command: /{cmd_name}")

    # Add start command and button handler
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(handle_menu_buttons, pattern='^(?!approve|deny).*$'))
    app.add_handler(CallbackQueryHandler(handle_approval_callback, pattern='^(approve|deny):'))

    # Register approval handler
    app.add_handler(MessageHandler(filters.ALL, handle_approval))

    print("🤖 Bot is running...")
    app.run_polling()

async def start(update: Update, context):
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    logging.info(f"Checking authorization for user ID: {user_id}, Username: {username}")

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await update.message.reply_text(
        "👋 Welcome to Pi IP Bot! Use the menu to select a command.",
        reply_markup=ReplyKeyboardRemove()
    )
    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=get_main_menu()
    )

if __name__ == "__main__":
    main()