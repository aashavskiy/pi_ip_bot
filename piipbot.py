import logging
import os
import importlib
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from commands.menu import menu_command, handle_menu_buttons, vpn_menu

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
    logging.info(f"✅ Loaded commands from {commands_dir}: {', '.join(commands.keys())}")
    return commands

async def start(update: Update, context: CallbackContext) -> None:
    await menu_command(update, context)

# Setup bot application
app = Application.builder().token(BOT_TOKEN).build()

# Register handlers
commands = load_commands()
for command_name, command_func in commands.items():
    app.add_handler(CommandHandler(command_name, command_func))
    logging.info(f"🔹 Registered command: /{command_name}")

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_menu_buttons))
app.add_handler(CommandHandler("vpn", vpn_menu))

if __name__ == "__main__":
    logging.info("🤖 piipbot.py is running...")
    if commands:
        logging.info(f"📌 Available commands: {', '.join(commands.keys())}")
    else:
        logging.warning("⚠️ No commands loaded!")
    app.run_polling()