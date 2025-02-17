# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/menu.py

from telegram import Update
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from commands.ip import ip_command
from commands.uptime import uptime_command
from commands.router_utils import is_router_admin
from commands.router_menu import router_menu_command  # ✅ Now correctly defined

# Function to generate the main menu
def get_main_menu(user_id: str):
    keyboard = [
        [InlineKeyboardButton("🌐 IP", callback_data="ip")],
        [InlineKeyboardButton("⏳ Uptime", callback_data="uptime")]
    ]

    # Add Router Control Menu button **only for whitelisted users**
    if is_router_admin(user_id):
        keyboard.append([InlineKeyboardButton("⚙ Router Control", callback_data="router_menu")])

    return InlineKeyboardMarkup(keyboard)

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
        await router_menu_command(update, context)  # ✅ Now correctly implemented
    else:
        await message.reply_text("❌ Unknown command.")

    await message.reply_text("📍 Main Menu:", reply_markup=get_main_menu(user_id))