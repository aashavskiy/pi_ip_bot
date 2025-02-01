from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, filters
from bot_utils import is_user_in_vpn_whitelist, is_user_authorized, request_approval
from commands.vpn.devices import add_device, list_devices, get_config, remove_device
from commands.ip import ip_command
from commands.uptime import uptime_command
import logging

# Define states for the conversation
DEVICE_NAME = range(1)

def get_main_menu():
    return ReplyKeyboardMarkup([
        ["🌐 IP", "⏳ Uptime"],
        ["🔐 VPN"]
    ], resize_keyboard=True, one_time_keyboard=True)

def get_vpn_menu():
    return ReplyKeyboardMarkup([
        ["➕ Add Device", "📋 List Devices"],
        ["🔑 Get Config", "❌ Remove Device"],
        ["🔙 Main Menu"]
    ], resize_keyboard=True, one_time_keyboard=True)

async def menu_command(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    if not is_user_authorized(user_id):
        await request_approval(user_id, username, "bot")
        await update.message.reply_text("🚫 You are not authorized to use this bot. An approval request has been sent to the admin.")
        return

    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=ReplyKeyboardRemove()
    )
    await update.message.reply_text(
        "📍 Main Menu:",
        reply_markup=get_main_menu()
    )

async def vpn_menu(update: Update, context: CallbackContext) -> None:
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "Unknown"

    logging.info(f"Checking VPN authorization for user ID: {user_id}, Username: {username}")

    if not is_user_in_vpn_whitelist(user_id):
        await request_approval(user_id, username, "vpn")
        await update.message.reply_text("❌ You are not authorized for VPN access. An approval request has been sent to the admin.")
        return

    await update.message.reply_text("🔐 VPN Menu:", reply_markup=get_vpn_menu())

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    if update.message:
        text = update.message.text.strip()
        message = update.message
    elif update.callback_query:
        text = update.callback_query.data
        message = update.callback_query.message
    else:
        return

    context.args = text.split()

    if text == "🌐 IP":
        await ip_command(update, context)
    elif text == "⏳ Uptime":
        await uptime_command(update, context)
    elif text == "🔐 VPN":
        await vpn_menu(update, context)
    elif text == "➕ Add Device":
        await update.message.reply_text("Please enter the device name:")
        return DEVICE_NAME
    elif text == "📋 List Devices":
        await list_devices(update, context)
    elif text == "🔑 Get Config":
        await get_config(update, context)
    elif text == "❌ Remove Device":
        await remove_device(update, context)
    elif text == "🔙 Main Menu":
        await menu_command(update, context)
    else:
        await message.reply_text("❌ Unknown command. Please use the menu or type /help for available commands.")

async def device_name_handler(update: Update, context: CallbackContext) -> None:
    device_name = update.message.text.strip()
    context.args = [device_name]
    await add_device(update, context)
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Operation cancelled.", reply_markup=get_main_menu())
    return ConversationHandler.END

def get_conversation_handler():
    return ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_buttons)],
        states={
            DEVICE_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, device_name_handler)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )