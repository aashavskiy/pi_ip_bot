import os
import importlib
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to dynamically load command handlers from the "commands" folder
def load_commands():
    commands = {}
    commands_dir = "commands"
    
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{commands_dir}.{filename[:-3]}"  # Remove .py extension
            module = importlib.import_module(module_name)
            
            if hasattr(module, f"{filename[:-3]}_command"):
                commands[filename[:-3]] = getattr(module, f"{filename[:-3]}_command")

    return commands

# Main function to start the bot
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Dynamically load all command handlers
    commands = load_commands()
    for cmd_name, cmd_func in commands.items():
        app.add_handler(CommandHandler(cmd_name, cmd_func))
        print(f"Loaded command: /{cmd_name}")

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()