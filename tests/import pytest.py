import pytest
from unittest.mock import patch, MagicMock
from piipbot import main, load_commands

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("BOT_TOKEN", "test_token")
    monkeypatch.setenv("ADMIN_ID", "admin_id")

@pytest.fixture
def mock_application_builder():
    with patch('piipbot.Application.builder') as mock_builder:
        mock_app = MagicMock()
        mock_builder.return_value.token.return_value.build.return_value = mock_app
        yield mock_app

@pytest.fixture
def mock_load_commands():
    with patch('piipbot.load_commands') as mock_load:
        mock_load.return_value = {
            "test_command": MagicMock()
        }
        yield mock_load

def test_main(mock_env, mock_application_builder, mock_load_commands):
    main()

    # Check if the bot token is set correctly
    mock_application_builder.builder().token.assert_called_with("test_token")

    # Check if the command handlers are added correctly
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())
    mock_application_builder.add_handler.assert_any_call(MagicMock())

    # Check if the bot is running
    mock_application_builder.run_polling.assert_called_once()