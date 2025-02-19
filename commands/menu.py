# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/menu.py

from telegram import Update
from telegram.ext import CallbackContext
from commands.ip import ip_command
from commands.uptime import uptime_command
from commands.menu_utils import get_main_menu  # Import from the new utility module

# Function to handle menu button presses
async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    if update.callback_query:
        text = update.callback_query.data  # Handle inline button press
        await update.callback_query.answer()  # Acknowledge button press
        message = update.callback_query.message
    else:
        return

    # Match button presses with commands
    if text == "ip":
        await ip_command(update, context)
    elif text == "uptime":
        await uptime_command(update, context)
    else:
        await message.reply_text("❌ Unknown command.")

    # Show the menu again after the command execution
    await message.reply_text("📍 Main Menu:", reply_markup=get_main_menu())

# Command to display the menu
async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=get_main_menu()
    )