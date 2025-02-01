import logging
import os
import subprocess
import importlib
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from commands.admin import handle_approval
from commands.menu import menu_command, handle_menu_buttons, vpn_menu  # Исправленный импорт

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def load_commands():
    commands = {}
    commands_dir = "commands"
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{commands_dir}.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, f"{filename[:-3]}_command"):
                commands[filename[:-3]] = getattr(module, f"{filename[:-3]}_command")
    return commands

async def vpn_button_handler(update: Update, context):
    await vpn_menu(update, context)  # Исправленный вызов функции

async def start(update: Update, context):
    await update.message.reply_text("Welcome to PI IP Bot!")

# Setup bot application
app = Application.builder().token(BOT_TOKEN).build()

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_menu_buttons))
app.add_handler(CommandHandler("vpn", vpn_button_handler))  # VPN обработчик

if __name__ == "__main__":
    logging.info("🤖 Bot is running...")
    app.run_polling()
