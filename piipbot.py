import logging
import os
import importlib
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from commands.menu import menu_command, handle_menu_buttons, vpn_menu
from commands.admin import handle_approval

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Load all command handlers dynamically
    commands = load_commands()
    for cmd_name, cmd_func in commands.items():
        app.add_handler(CommandHandler(cmd_name, cmd_func))
        logging.info(f"✅ Loaded command: /{cmd_name}")

    # Add menu command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("vpn", vpn_menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_buttons))

    # Add inline button handler for approving new users
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_approval))

    logging.info("🤖 Bot is running...")
    app.run_polling()

async def start_command(update, context):
    await menu_command(update, context)

if __name__ == "__main__":
    main()