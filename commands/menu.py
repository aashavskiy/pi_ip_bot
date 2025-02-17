# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/menu.py

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from commands.ip import ip_command
from commands.uptime import uptime_command
from commands.router_utils import is_router_admin
from commands.router_menu import router_menu_command  # ✅ Import correctly

# Function to generate the main menu
def get_main_menu(user_id: str):
    keyboard = [
        [KeyboardButton("🌐 IP"), KeyboardButton("⏳ Uptime")]
    ]

    # Add Router Control Menu button **only for whitelisted users**
    if is_router_admin(user_id):
        keyboard.append([KeyboardButton("⚙ Router Control")])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

# Function to handle menu text commands
async def handle_menu_commands(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip()
    user_id = str(update.message.from_user.id)

    if text == "🌐 IP":
        await ip_command(update, context)
    elif text == "⏳ Uptime":
        await uptime_command(update, context)
    elif text == "⚙ Router Control":
        await router_menu_command(update, context)
    else:
        await update.message.reply_text("❌ Unknown command. Please use the menu.")

# Command to display the main menu
async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)

    await update.message.reply_text("📍 Main Menu:", reply_markup=get_main_menu(user_id))