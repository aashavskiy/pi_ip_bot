# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/router_menu.py

import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from commands.router_utils import is_router_admin
from commands.router_cli import run_router_command  # ✅ Import SSH CLI function

load_dotenv()

# Function to generate the router control menu
def get_router_menu():
    keyboard = [
        [KeyboardButton("🔄 Reboot Router"), KeyboardButton("📡 Show Connected Devices")],
        [KeyboardButton("⬅ Back to Main Menu")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

# Function to display the router menu
async def router_menu_command(update: Update, context: CallbackContext) -> None:
    """Handles opening the router control menu."""
    user_id = str(update.effective_user.id)

    if not is_router_admin(user_id):
        await update.message.reply_text("🚫 You are not authorized to access the router menu.")
        return

    await update.message.reply_text("⚙ Router Control Menu:", reply_markup=get_router_menu())

# Function to handle router menu commands
async def handle_router_commands(update: Update, context: CallbackContext) -> None:
    """Handles text commands inside the router control menu."""
    text = update.message.text.strip()

    if text == "🔄 Reboot Router":
        result = run_router_command("system reboot")
        await update.message.reply_text(f"🔄 {result}")
    elif text == "📡 Show Connected Devices":
        result = run_router_command("show ip dhcp bindings")  # ✅ Corrected command
        await update.message.reply_text(f"📡 Connected Devices:\n{result}")
    elif text == "⬅ Back to Main Menu":
        from commands.menu import get_main_menu
        user_id = str(update.effective_user.id)
        await update.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu(user_id))
    else:
        await update.message.reply_text("❌ Unknown command. Please use the menu.")