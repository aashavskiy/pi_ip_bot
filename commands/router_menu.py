# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/router_menu.py

import requests
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from commands.router_utils import is_router_admin

# Load environment variables from .env
load_dotenv()

# Retrieve router credentials
ROUTER_IP = os.getenv("ROUTER_IP")
ROUTER_USERNAME = os.getenv("ROUTER_USERNAME")
ROUTER_PASSWORD = os.getenv("ROUTER_PASSWORD")

# Function to get the router control menu
get_/*************  ✨ Codeium Command ⭐  *************/
    """
    Handles access to the router menu.

    If the user is not authorized, sends a "Not authorized" message.
    Otherwise, sends a message with the router menu buttons.
    """
/******  d3cb9806-d703-4b60-a628-f53b753c7387  *******/router_menu():
    keyboard = [
        [InlineKeyboardButton("🔄 Reboot Router", callback_data="router_reboot")],
        [InlineKeyboardButton("📶 Wi-Fi Settings", callback_data="router_wifi")],
        [InlineKeyboardButton("📡 Show Connected Devices", callback_data="router_devices")],
        [InlineKeyboardButton("👤 List Router Users", callback_data="router_users")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

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
        from commands.menu import get_main_menu
        user_id = str(update.effective_user.id)
        await query.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu(user_id))