from telegram import ReplyKeyboardMarkup

# Function to generate the keyboard menu
def get_main_menu():
    commands = ["/start", "/ip"]  # Add more commands here
    keyboard = [[cmd] for cmd in commands]  # Each command on a separate row
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)