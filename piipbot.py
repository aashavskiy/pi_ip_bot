import os
import importlib
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from utils import load_whitelist
from commands.admin import handle_approval
from commands.vpn import handle_vpn_approval  # VPN approval handler

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ ERROR: BOT_TOKEN is not set in .env!")

# Load whitelists
BOT_WHITELIST_FILE = "bot_whitelist.txt"
BOT_WHITELIST = load_whitelist(BOT_WHITELIST_FILE)

# Function to check if a user is authorized
async def check_whitelist(update):
    user_id = str(update.message.from_user.id)
    
    if user_id not in BOT_WHITELIST:
        await update.message.reply_text("🚫 You are not authorized to use this bot.")
        print(f"🚨 Unauthorized access attempt: {update.message.from_user.username} ({user_id})")
        return False  # ⛔ Stop execution if not whitelisted
    
    return True  # ✅ Allow execution if whitelisted

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
        async def wrapped_func(update, context, func=cmd_func):
            if await check_whitelist(update):  # Enforce whitelist
                await func(update, context)

        app.add_handler(CommandHandler(cmd_name, wrapped_func))
        print(f"✅ Loaded command: /{cmd_name}")

    # Add admin approval handler (for bot access)
    app.add_handler(CallbackQueryHandler(handle_approval))

    # Add VPN-related handlers
    from commands.vpn import request_vpn, add_device, list_devices, remove_device
    app.add_handler(CommandHandler("vpn", request_vpn))
    app.add_handler(CommandHandler("adddevice", add_device))
    app.add_handler(CommandHandler("listdevices", list_devices))
    app.add_handler(CommandHandler("removedevice", remove_device))
    app.add_handler(CallbackQueryHandler(handle_vpn_approval, pattern="vpn_approve_|vpn_deny_"))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()