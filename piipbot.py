import logging
import os
import subprocess
import importlib
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from commands.admin import handle_approval
from commands.menu import menu_command, handle_menu_buttons  # Ensure menu functions are imported
from commands.vpn.menu import vpn_menu  # Import VPN menu

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

async def unknown_command(update: Update, context):
    await update.message.reply_text("❌ Unknown command. Please use the menu or type /help for available commands.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    commands = load_commands()
    for cmd_name, cmd_func in commands.items():
        app.add_handler(CommandHandler(cmd_name, cmd_func))
        print(f"✅ Loaded command: /{cmd_name}")
    
    app.add_handler(CallbackQueryHandler(handle_approval))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_command))
    app.add_handler(CommandHandler("menu", menu_command))  # Ensure menu command is available
    app.add_handler(CommandHandler("vpn", vpn_menu))  # Ensure VPN menu command is available
    app.add_handler(CallbackQueryHandler(handle_menu_buttons))  # Handle menu button interactions
    
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()