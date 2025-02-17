# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/router_menu.py

import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from commands.router_utils import is_router_admin
from commands.router_cli import run_router_command  # ✅ Import SSH CLI function

load_dotenv()

# Function to get the router control menu
def get_router_menu():
    keyboard = [
        [InlineKeyboardButton("🔄 Reboot Router", callback_data="router_reboot")],
        [InlineKeyboardButton("📡 Show Connected Devices", callback_data="router_devices")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Function to handle router menu button presses
async def handle_router_buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "router_reboot":
        result = run_router_command("system reboot")
        await query.message.reply_text(f"🔄 {result}")
    elif query.data == "router_devices":
        result = run_router_command("show ip dhcp bindings")  # ✅ Corrected command
        await query.message.reply_text(f"📡 Connected Devices:\n{result}")
    elif query.data == "main_menu":
        from commands.menu import get_main_menu
        user_id = str(update.effective_user.id)
        await query.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu(user_id))