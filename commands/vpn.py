# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/vpn.py

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher

# Создание диспетчера (предполагается, что бот уже определён где-то в основном файле)
dp = Dispatcher.get_current()

# Обработчик команды VPN
@dp.message_handler(Command("VPN"))
async def vpn_command_handler(message: Message):
    await message.reply("VPN command executed successfully.")