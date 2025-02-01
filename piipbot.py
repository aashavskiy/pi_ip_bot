# piipbot.py
import logging
import os
import subprocess
import importlib
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from commands.admin import handle_approval
from commands.menu import menu_command, handle_menu_buttons, vpn_menu, get_main_menu
from commands.vpn.devices import add_device, list_devices, get_config, remove_device  # Добавлены команды VPN

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

/*************  ✨ Codeium Command 🌟  *************/
def load_commands():
    """
    Load command functions from Python files in the 'commands' directory.
    
    Returns:
        dict: A dictionary where keys are command names and values are the corresponding functions.
    """
    commands = {}
    commands_dir = "commands"
    
    # Iterate through files in the commands directory
    for filename in os.listdir(commands_dir):
        # Consider only Python files excluding '__init__.py'
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{commands_dir}.{filename[:-3]}"
            # Dynamically import the module
            module = importlib.import_module(module_name)
            command_attr = f"{filename[:-3]}_command"
            # Check if the module has the command function and add it to the dictionary
            if hasattr(module, command_attr):
                commands[filename[:-3]] = getattr(module, command_attr)
    
    # Log the loaded commands
            if hasattr(module, f"{filename[:-3]}_command"):
                commands[filename[:-3]] = getattr(module, f"{filename[:-3]}_command")
    logging.info(f"✅ Loaded commands from {commands_dir}: {', '.join(commands.keys())}")
    return commands
/******  dba50695-774b-4e28-b5c2-081e6deedef2  *******/

async def vpn_button_handler(update: Update, context):
    await vpn_menu(update, context)

async def start(update: Update, context):
    await update.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu())
    await menu_command(update, context)

# Setup bot application
app = Application.builder().token(BOT_TOKEN).build()

# Register handlers
commands = load_commands()
for command_name, command_func in commands.items():
    app.add_handler(CommandHandler(command_name, command_func))
    logging.info(f"🔹 Registered command: /{command_name}")

# Добавляем команды VPN
app.add_handler(CommandHandler("add_device", add_device))
app.add_handler(CommandHandler("list_devices", list_devices))
app.add_handler(CommandHandler("get_config", get_config))
app.add_handler(CommandHandler("remove_device", remove_device))

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_menu_buttons))
app.add_handler(CommandHandler("vpn", vpn_button_handler))

if __name__ == "__main__":
    logging.info("🤖 piipbot.py is running...")
    if commands:
        logging.info(f"📌 Available commands: {', '.join(commands.keys())}")
    else:
        logging.warning("⚠️ No commands loaded!")
    app.run_polling()
