# /Users/alexanderashavskiy/projects/pi_ip_bot/menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Определение кнопок главного меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("IP"))
main_menu.add(KeyboardButton("UPTIME"))
main_menu.add(KeyboardButton("VPN"))