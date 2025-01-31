import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Message, Chat
from telegram.ext import CallbackContext, CallbackQueryHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def menu_command(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("📡 IP Address", callback_data="menu_ip")],
        [InlineKeyboardButton("📊 Uptime", callback_data="menu_uptime")],
        [InlineKeyboardButton("🔐 VPN Access", callback_data="menu_vpn")],
        [InlineKeyboardButton("👋 End", callback_data="menu_end")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📌 **Choose an option:**", reply_markup=reply_markup, parse_mode="Markdown")

async def handle_menu_buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    command_map = {
        "menu_ip": "/ip",
        "menu_uptime": "/uptime",
        "menu_vpn": "/vpn",
        "menu_end": "/end"
    }

    command = command_map.get(query.data)
    if command:
        fake_update = Update(
            update.update_id,
            message=Message(
                message_id=query.message.message_id,
                date=query.message.date,
                chat=Chat(id=query.message.chat_id, type="private"),
                from_user=query.from_user,
                text=command,
                bot=context.bot
            )
        )
        fake_update._bot = context.bot
        fake_update.effective_chat = fake_update.message.chat
        fake_update.effective_user = fake_update.message.from_user

        if command == "/ip":
            from commands.ip import ip_command
            await ip_command(fake_update, context)
        elif command == "/uptime":
            from commands.uptime import uptime_command
            await uptime_command(fake_update, context)
        elif command == "/vpn":
            from commands.vpn.request import request_vpn
            await request_vpn(fake_update, context)
        elif command == "/end":
            await query.message.reply_text("👋 Goodbye! Closing the menu.")
            return
        
        await menu_command(update, context)  # Show menu after command execution
