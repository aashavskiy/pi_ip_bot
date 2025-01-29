import requests
from telegram import Update
from telegram.ext import CallbackContext
from menu import get_main_menu  # Import menu function

# Keenetic router settings
KEENETIC_IP = "192.168.1.1"  # Или реальный IP, если доступен снаружи
USERNAME = "guest"  # Логин от роутера
PASSWORD = "ydwb8tkc_EPJ*pdr@ubn"  # Пароль

def get_keenetic_ip():
    try:
        session = requests.Session()

        # 1. Авторизуемся в Keenetic
        auth_url = f"http://{KEENETIC_IP}/auth"
        auth_data = {"username": USERNAME, "password": PASSWORD}
        response = session.post(auth_url, json=auth_data)
        if response.status_code != 200:
            return "Error: Unable to authenticate with Keenetic"

        # 2. Запрашиваем IP
        ip_url = f"http://{KEENETIC_IP}/rci/show/interface"
        response = session.get(ip_url)
        data = response.json()

        # 3. Ищем внешний IP в интерфейсе интернет-соединения
        for interface in data.get("interface", []):
            if "internet" in interface.get("name", "").lower():
                return f"Your external IP: {interface['ip']}"

        return "Error: Could not find external IP"

    except Exception as e:
        return f"Error retrieving IP: {e}"

# Command handler for /ip
async def ip_command(update: Update, context: CallbackContext) -> None:
    ip_info = get_keenetic_ip()
    reply_markup = get_main_menu()
    await update.message.reply_text(ip_info, reply_markup=reply_markup)