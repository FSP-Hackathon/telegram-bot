from telebot import types

from constants.strings import Strings


def databaseActionsKeyboard(url: str):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    website = types.WebAppInfo(url)
    metrcis_button = types.KeyboardButton(
        text=Strings.translate('check_metrics'),
        web_app=website
    )
    menu_button = types.KeyboardButton(text=Strings.translate('menu_main'))
    menu_shortcuts = types.KeyboardButton(
        text=Strings.translate('menu_shortcuts'),
    )
    markup.add(metrcis_button, menu_shortcuts, menu_button)

    return markup
