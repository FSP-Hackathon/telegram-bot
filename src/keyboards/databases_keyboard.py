from telebot import types

from constants.strings import Strings
from monitoring_bot import MonitoringBot

def databasesKeyboard(names: list[str]):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    
    for name in names:
        button = types.KeyboardButton(name)
        markup.add(button)