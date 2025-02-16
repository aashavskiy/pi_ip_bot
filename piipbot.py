# /Users/alexanderashavskiy/projects/pi_ip_bot/piipbot.py

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

from commands.menu import router as menu_router
from commands.ip import router as ip_router
from commands.uptime import router as uptime_router
from commands.vpn import get_vpn_router

# Initialize bot
TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Get VPN router after initialization to avoid circular import
vpn_router = get_vpn_router()

# Include routers
dp.include_router(menu_router)
dp.include_router(ip_router)
dp.include_router(uptime_router)
dp.include_router(vpn_router)

# Start command
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Bot started. Use the menu to interact.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())