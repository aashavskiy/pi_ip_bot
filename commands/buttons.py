# /Users/alexanderashavskiy/projects/pi_ip_bot/commands/buttons.py

from aiogram import Router
from aiogram.types import CallbackQuery
from commands.ip import get_external_ip
from commands.uptime import get_system_uptime

router = Router()

@router.callback_query(lambda c: c.data == "get_ip")
async def handle_ip_button(callback_query: CallbackQuery):
    ip_address = get_external_ip()
    await callback_query.message.answer(f"Your external IP: {ip_address}")

@router.callback_query(lambda c: c.data == "get_uptime")
async def handle_uptime_button(callback_query: CallbackQuery):
    uptime_info = get_system_uptime()
    await callback_query.message.answer(f"System uptime: {uptime_info}")

@router.callback_query(lambda c: c.data == "get_vpn")
async def handle_vpn_button(callback_query: CallbackQuery):
    await callback_query.message.answer("VPN settings will be implemented here.")