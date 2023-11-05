from telebot import types

from constants.strings import Strings


def mainMenuKeyboard(showDebug: bool):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    menu_databases = types.KeyboardButton(
        Strings.translate('menu_databases'),
    )
    menu_current = types.KeyboardButton(Strings.translate('menu_current'))
    markup.add(menu_databases, menu_current)

    if showDebug:
        menu_debug = types.KeyboardButton(Strings.translate('menu_debug'))
        markup.add(menu_debug)

    return markup
