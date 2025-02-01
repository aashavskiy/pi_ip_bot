import pytest
import asyncio
import sys
import os
from telegram import Update, User, Message, Chat, CallbackQuery
from telegram.ext import CallbackContext

# Добавляем корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot_utils import is_user_authorized, request_approval, add_to_whitelist, BOT_WHITELIST_FILE, VPN_WHITELIST_FILE
from commands.menu import menu_command, vpn_menu
from commands.admin import handle_approval_callback

@pytest.fixture
def mock_update():
    user = User(id=12345, first_name="Test", is_bot=False)
    chat = Chat(id=67890, type="private")
    message = Message(message_id=1, date=None, chat=chat, text="/start", from_user=user)
    return Update(update_id=1, message=message)

@pytest.fixture
def mock_context(mock_update):
    return CallbackContext.from_update(mock_update, None)

@pytest.fixture
def mock_callback_query():
    user = User(id=12345, first_name="Test", is_bot=False)
    chat = Chat(id=67890, type="private")
    message = Message(message_id=1, date=None, chat=chat, text="/start", from_user=user)
    return CallbackQuery(id=1, from_user=user, message=message, chat_instance="instance", data="")

@pytest.mark.asyncio
async def test_menu_command_authorized(mock_update, mock_context, monkeypatch):
    def mock_is_user_authorized(user_id):
        return True

    monkeypatch.setattr('bot_utils.is_user_authorized', mock_is_user_authorized)
    await menu_command(mock_update, mock_context)
    assert mock_update.message.reply_text.call_count == 2

@pytest.mark.asyncio
async def test_menu_command_unauthorized(mock_update, mock_context, monkeypatch):
    def mock_is_user_authorized(user_id):
        return False

    async def mock_request_approval(user_id, username, approval_type):
        pass

    monkeypatch.setattr('bot_utils.is_user_authorized', mock_is_user_authorized)
    monkeypatch.setattr('bot_utils.request_approval', mock_request_approval)
    await menu_command(mock_update, mock_context)
    assert mock_update.message.reply_text.call_count == 1

@pytest.mark.asyncio
async def test_vpn_menu_authorized(mock_update, mock_context, monkeypatch):
    def mock_is_user_in_vpn_whitelist(user_id):
        return True

    monkeypatch.setattr('bot_utils.is_user_in_vpn_whitelist', mock_is_user_in_vpn_whitelist)
    await vpn_menu(mock_update, mock_context)
    assert mock_update.message.reply_text.call_count == 1

@pytest.mark.asyncio
async def test_vpn_menu_unauthorized(mock_update, mock_context, monkeypatch):
    def mock_is_user_in_vpn_whitelist(user_id):
        return False

    async def mock_request_approval(user_id, username, approval_type):
        pass

    monkeypatch.setattr('bot_utils.is_user_in_vpn_whitelist', mock_is_user_in_vpn_whitelist)
    monkeypatch.setattr('bot_utils.request_approval', mock_request_approval)
    await vpn_menu(mock_update, mock_context)
    assert mock_update.message.reply_text.call_count == 1

@pytest.mark.asyncio
async def test_handle_approval_callback_approve_bot(mock_context, monkeypatch):
    user = User(id=12345, first_name="Test", is_bot=False)
    chat = Chat(id=67890, type="private")
    message = Message(message_id=1, date=None, chat=chat, text="/start", from_user=user)
    callback_query = CallbackQuery(id=1, from_user=user, message=message, chat_instance="instance", data="approve:12345:TestUser:bot")
    update = Update(update_id=1, callback_query=callback_query)

    def mock_add_to_whitelist(filename, user_id, username):
        assert filename == BOT_WHITELIST_FILE
        assert user_id == "12345"
        assert username == "TestUser"

    monkeypatch.setattr('bot_utils.add_to_whitelist', mock_add_to_whitelist)
    await handle_approval_callback(update, mock_context)
    assert update.callback_query.edit_message_text.call_count == 1

@pytest.mark.asyncio
async def test_handle_approval_callback_approve_vpn(mock_context, monkeypatch):
    user = User(id=12345, first_name="Test", is_bot=False)
    chat = Chat(id=67890, type="private")
    message = Message(message_id=1, date=None, chat=chat, text="/start", from_user=user)
    callback_query = CallbackQuery(id=1, from_user=user, message=message, chat_instance="instance", data="approve:12345:TestUser:vpn")
    update = Update(update_id=1, callback_query=callback_query)

    def mock_add_to_whitelist(filename, user_id, username):
        assert filename == VPN_WHITELIST_FILE
        assert user_id == "12345"
        assert username == "TestUser"

    monkeypatch.setattr('bot_utils.add_to_whitelist', mock_add_to_whitelist)
    await handle_approval_callback(update, mock_context)
    assert update.callback_query.edit_message_text.call_count == 1

@pytest.mark.asyncio
async def test_handle_approval_callback_deny(mock_context):
    user = User(id=12345, first_name="Test", is_bot=False)
    chat = Chat(id=67890, type="private")
    message = Message(message_id=1, date=None, chat=chat, text="/start", from_user=user)
    callback_query = CallbackQuery(id=1, from_user=user, message=message, chat_instance="instance", data="deny:12345:TestUser:bot")
    update = Update(update_id=1, callback_query=callback_query)

    await handle_approval_callback(update, mock_context)
    assert update.callback_query.edit_message_text.call_count == 1
