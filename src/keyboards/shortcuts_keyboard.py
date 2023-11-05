from telebot import types

from constants.strings import Strings


def shortcutsKeyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    shortcut_restart = types.KeyboardButton(
        text=Strings.translate('shortcut_restart'),
    )
    shortcut_backup = types.KeyboardButton(
        text=Strings.translate('shortcut_backup'),
    )
    shortcut_terminate = types.KeyboardButton(
        text=Strings.translate('shortcut_terminate'),
    )
    shortcut_restore = types.KeyboardButton(
        text=Strings.translate('shortcut_restore'),
    )
    shortcut_shutdown = types.KeyboardButton(
        text=Strings.translate('shortcut_shutdown'),
    )

    markup.add(
        shortcut_restart,
        shortcut_restore,
        shortcut_backup,
        shortcut_terminate,
        shortcut_shutdown,
    )

    return markup
