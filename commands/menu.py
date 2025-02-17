# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/menu.py

from telegram import Update
from telegram.ext import CallbackContext
from commands.ip import ip_command
from commands.uptime import uptime_command
from commands.menu_utils import get_main_menu  # ✅ Import from menu_utils.py
from commands.router_menu import router_menu_command  # ✅ Import directly

__all__ = ["menu_command", "handle_menu_buttons"]  # ✅ Ensure it's available for import

# Function to handle menu button presses
async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    if update.callback_query:
        text = update.callback_query.data
        await update.callback_query.answer()
        message = update.callback_query.message
        user_id = str(update.effective_user.id)
    else:
        return

    if text == "ip":
        await ip_command(update, context)
    elif text == "uptime":
        await uptime_command(update, context)
    elif text == "router_menu":
        await router_menu_command(update, context)  # ✅ Now correctly imported
    else:
        await message.reply_text("❌ Unknown command.")

    await message.reply_text("📍 Main Menu:", reply_markup=get_main_menu(user_id))

# Command to display the main menu
async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)  # Ensure user ID is a string

    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=get_main_menu(user_id)
    )