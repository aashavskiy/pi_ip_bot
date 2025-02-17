# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/router_menu.py

import requests
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from commands.router_utils import is_router_admin
from commands.menu_utils import get_main_menu  # ✅ Now importing menu function properly

__all__ = ["router_menu_command", "handle_router_buttons"]  # ✅ Ensure proper exports

# Load environment variables from .env
load_dotenv()

# Retrieve router credentials
ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_USERNAME = os.getenv("ROUTER_USERNAME")
ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD")

# Function to get the router control menu
def get_router_menu():
    keyboard = [
        [InlineKeyboardButton("🔄 Reboot Router", callback_data="router_reboot")],
        [InlineKeyboardButton("📶 Wi-Fi Settings", callback_data="router_wifi")],
        [InlineKeyboardButton("📡 Show Connected Devices", callback_data="router_devices")],
        [InlineKeyboardButton("👤 List Router Users", callback_data="router_users")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Function to display the router menu
async def router_menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.effective_user.id)

    if not is_router_admin(user_id):
        await update.callback_query.answer()
        await update.callback_query.message.reply_text("🚫 You are not authorized to access the router menu.")
        return

    await update.callback_query.answer()  # Acknowledge button press
    await update.callback_query.message.reply_text(
        "⚙ Router Control Menu:",
        reply_markup=get_router_menu()
    )

# Function to fetch router users
def fetch_router_users():
    """Retrieve the list of users from the router."""
    url = f"{ROUTER_IP}/rci/show/users"
    auth = (ROUTER_USERNAME, ROUTER_PASSWORD)

    try:
        response = requests.get(url, auth=auth, timeout=5)
        response.raise_for_status()
        users = response.json().get("users", [])

        if not users:
            return "No users found on the router."

        return "\n".join([f"👤 {user['name']} ({user['role']})" for user in users])

    except requests.RequestException as e:
        return f"❌ Error fetching users: {e}"

# Function to handle router menu button presses
async def handle_router_buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "router_reboot":
        await query.message.reply_text("🔄 Rebooting the router... (Not yet implemented)")
    elif query.data == "router_wifi":
        await query.message.reply_text("📶 Fetching Wi-Fi settings... (Not yet implemented)")
    elif query.data == "router_devices":
        await query.message.reply_text("📡 Listing connected devices... (Not yet implemented)")
    elif query.data == "router_users":
        users_list = fetch_router_users()
        await query.message.reply_text(users_list)
    elif query.data == "main_menu":
        user_id = str(update.effective_user.id)
        await query.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu(user_id))