import os
import importlib
import asyncio
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import BotCommand
from commands.menu import menu_command, handle_menu_buttons
from commands.admin import handle_approval
from commands.vpn.request import request_vpn
from commands.vpn.approval import handle_vpn_approval
from commands.vpn.devices import add_device, get_config, list_devices, remove_device

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def clear_persistent_menu(application):
    """Clear the menu near the input field."""
    await application.bot.set_my_commands([])  # Remove all persistent commands

def load_commands():
    commands = {}
    commands_dir = "commands"

    for root, _, files in os.walk(commands_dir):
        for filename in files:
            if filename.endswith(".py") and filename not in ["__init__.py", "menu.py", "time.py", "weather.py"]:
                module_path = os.path.join(root, filename)
                module_name = module_path.replace("/", ".").replace("\\", ".")[:-3]
                
                module = importlib.import_module(module_name)

                if hasattr(module, f"{filename[:-3]}_command"):
                    commands[filename[:-3]] = getattr(module, f"{filename[:-3]}_command")
    
    return commands

async def start_command(update, context):
    """Send a welcome message and show the menu."""
    await update.message.reply_text("👋 **Welcome!** Use the menu below:")
    await menu_command(update, context)

async def end_command(update, context):
    """End the conversation."""
    await update.message.reply_text("👋 **Goodbye!** Closing the menu.", parse_mode="Markdown")

async def unknown_command(update, context):
    """Handle unknown commands."""
    await update.message.reply_text("❌ I don't recognize this command. Use /menu to see available options.")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Clear persistent menu before running the bot
    await clear_persistent_menu(app)

    # Dynamically load all command handlers
    commands = load_commands()
    for cmd_name, cmd_func in commands.items():
        app.add_handler(CommandHandler(cmd_name, cmd_func))
        print(f"✅ Loaded command: /{cmd_name}")

    # Add menu and inline button handlers
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CallbackQueryHandler(handle_menu_buttons))

    # Add start and end commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("end", end_command))

    # Add VPN commands
    app.add_handler(CommandHandler("vpn", request_vpn))
    app.add_handler(CommandHandler("adddevice", add_device))
    app.add_handler(CommandHandler("getconfig", get_config))
    app.add_handler(CommandHandler("listdevices", list_devices))
    app.add_handler(CommandHandler("removedevice", remove_device))
    app.add_handler(CallbackQueryHandler(handle_vpn_approval, pattern="vpn_approve_|vpn_deny_"))

    # Add inline button handler for approving new users
    app.add_handler(CallbackQueryHandler(handle_approval))

    # Handle unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    print("🤖 Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
