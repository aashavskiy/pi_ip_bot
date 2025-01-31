import os
import importlib
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from commands.menu import menu_command, handle_menu_buttons
from commands.admin import handle_approval

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to dynamically load command handlers from the "commands" folder
def load_commands():
    commands = {}
    commands_dir = "commands"

    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename not in ["__init__.py", "menu.py"]:
            module_name = f"{commands_dir}.{filename[:-3]}"  # Remove .py extension
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

def main():
    app = Application.builder().token(BOT_TOKEN).build()

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

    # Add inline button handler for approving new users
    app.add_handler(CallbackQueryHandler(handle_approval))

    # Handle unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()