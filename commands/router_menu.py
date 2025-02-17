# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/router_menu.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from commands.router_utils import is_router_admin

# Function to get the router control menu
def get_router_menu():
    keyboard = [
        [InlineKeyboardButton("🔄 Reboot Router", callback_data="router_reboot")],
        [InlineKeyboardButton("📶 Wi-Fi Settings", callback_data="router_wifi")],
        [InlineKeyboardButton("📡 Show Connected Devices", callback_data="router_devices")],
        [InlineKeyboardButton("⬅ Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Function to handle router menu access
async def router_menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.effective_user.id)

    if not is_router_admin(user_id):
        await update.message.reply_text("🚫 You are not authorized to access the router menu.")
        return

    await update.message.reply_text(
        "⚙ Router Control Menu:",
        reply_markup=get_router_menu()
    )

# Function to handle router menu button clicks
async def handle_router_buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "router_reboot":
        await query.message.reply_text("🔄 Rebooting the router... (Not yet implemented)")
    elif query.data == "router_wifi":
        await query.message.reply_text("📶 Fetching Wi-Fi settings... (Not yet implemented)")
    elif query.data == "router_devices":
        await query.message.reply_text("📡 Listing connected devices... (Not yet implemented)")
    elif query.data == "main_menu":
        from commands.menu import get_main_menu
        await query.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu())