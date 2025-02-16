# commands/menu.py

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

def menu_command(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1')],
                [InlineKeyboardButton("Option 2", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an option:', reply_markup=reply_markup)

def get_main_menu():
    keyboard = [[InlineKeyboardButton("Main Option", callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)

def get_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('start', menu_command)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, some_handler_function)]
        },
        fallbacks=[CommandHandler('cancel', cancel_handler)]
    )

def some_handler_function(update, context):
    update.message.reply_text("You entered some text.")
    return ConversationHandler.END

def cancel_handler(update, context):
    update.message.reply_text("Conversation cancelled.")
    return ConversationHandler.END