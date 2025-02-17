# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/router_menu.py

import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from commands.router_utils import is_router_admin
from commands.router_cli import run_router_command  # ✅ Import SSH CLI function

load_dotenv()

# ✅ Explicitly expose functions to prevent import issues
__all__ = ["router_menu_command", "handle_router_buttons"]

# Function to generate the router control menu
def get_router_menu():
    keyboard = [
        [InlineKeyboardButton("🔄 Reboot Router", callback_data="router_reboot")],
        [InlineKeyboardButton("📡 Show Connected Devices", callback_data="router_devices")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ✅ Function to display the router menu
async def router_menu_command(update: Update, context: CallbackContext) -> None:
    """Handles opening the router control menu."""
    query = update.callback_query
    await query.answer()

    user_id = str(update.effective_user.id)
    if not is_router_admin(user_id):
        await query.message.reply_text("🚫 You are not authorized to access the router menu.")
        return

    await query.message.reply_text(
        "⚙ Router Control Menu:",
        reply_markup=get_router_menu()
    )

# ✅ Function to handle router menu button presses
async def handle_router_buttons(update: Update, context: CallbackContext) -> None:
    """Handles button presses inside the router control menu."""
    query = update.callback_query
    await query.answer()

    if query.data == "router_reboot":
        result = run_router_command("system reboot")
        await query.message.reply_text(f"🔄 {result}")
    elif query.data == "router_devices":
        result = run_router_command("show ip dhcp bindings")  # ✅ Corrected command
        await query.message.reply_text(f"📡 Connected Devices:\n{result}")
    elif query.data == "main_menu":
        from commands.menu import get_main_menu  # ✅ Import inside function to avoid circular import
        user_id = str(update.effective_user.id)
        await query.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu(user_id))