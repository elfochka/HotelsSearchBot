from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def request_yes_or_no() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Да')).add(KeyboardButton('Нет'))
    return keyboard
