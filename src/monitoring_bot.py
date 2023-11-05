from constants.strings import Strings
import telebot
import logging
import os
import requests

from telebot import types
from dotenv import load_dotenv
from database.bot_users_database import BotUsersDatabase
from keyboards.databases_keyboard import databasesKeyboard
from keyboards.main_menu_keyboard import mainMenuKeyboard
from keyboards.database_actions_keyboard import databaseActionsKeyboard
from keyboards.shortcuts_keyboard import shortcutsKeyboard

logger = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)

ACCESS_SERVICE_BASE_URL_KEY = 'ACCESS_SERVICE_BASE_URL'
DEVS = ['OwlCodR', 'zair_t', 'mthgradr', 'yulia_sharkova', 'danilkandakov']


class MonitoringBot:
    def __init():
        logger.debug(f'__init()')
        load_dotenv()
        token = os.getenv('BOT_TOKEN')
        return telebot.TeleBot(token, parse_mode=None)

    bot = __init()

    def run(drop=False) -> None:
        logger.debug(f'run(drop={drop})')
        BotUsersDatabase.init(drop)
        MonitoringBot.bot.infinity_polling()

    def __getChatOfUser(user: str) -> str:
        logger.debug(f'__getChatOfUser(user = {user})')
        chat = BotUsersDatabase.getChatIdByUsername(user)
        logger.debug(f'__getChatOfUser(chat = {chat})')
        return chat

    def __sendMessageToUser(msg: str, user: str, reply_markup) -> None:
        logger.debug(f'sendMessageToUser(user = {user}, msg = {msg})')
        chat = MonitoringBot.__getChatOfUser(user)

        if chat == None:
            logger.warning(f'chat_id of user {user} is None!')
            return

        MonitoringBot.bot.send_message(
            chat_id=chat,
            text=msg,
            parse_mode='MarkdownV2',
            reply_markup=reply_markup,
        )

    def __sendMessageToUsers(msg: str, users: list[str], reply_markup) -> None:
        logger.debug(f'sendMessageToUsers(msg = {msg}, users = {users})')
        for user in users:
            MonitoringBot.__sendMessageToUser(
                user=user,
                msg=msg,
                reply_markup=reply_markup,
            )

    def __checkUserWhitelisted(message, username: str) -> bool:
        isWhitelisted = MonitoringBot.__isUserWhitelisted(username)
        if not isWhitelisted:
            MonitoringBot.bot.reply_to(
                message, Strings.translate('not_whitelisted'),
            )
        return isWhitelisted

    def __isUserWhitelisted(username: str):
        logger.debug(f'checkByUsername(username={username})')
        base = os.getenv(ACCESS_SERVICE_BASE_URL_KEY)
        path = Strings.CHECK_USER_PATH

        url = f'{base}/{path}'
        params = {'nickname': username}

        logger.debug(f'checkByUsername(url={url}, params = {params})')

        response = requests.get(url, params=params)
        logger.debug(f'checkByUsername(response={response})')

        return response.json()

    def getDatabasesByUser(username: str) -> list[str]:
        logger.debug(f'__getDatabasesByUser(username={username})')

        base = os.getenv(ACCESS_SERVICE_BASE_URL_KEY)
        path = Strings.DATABASES_PATH

        url = f'{base}/{path}'
        params = {'nickname': username}

        logger.debug(f'__getDatabasesByUser(url={url}, params={params})')

        response = requests.get(url, params=params)
        return response.json()['databases']

    def sendErrorMessageToUsers(msg: str, users: list[str], db_name: str) -> None:
        logger.debug(f'sendErrorMessageToUsers(msg = {msg}, users = {users})')

        MonitoringBot.__sendMessageToUsers(
            msg=Strings.translate('internal_error') +
            f'"{db_name}"\n\n' + '```sh\n' + msg + "\n```",
            users=users,
        )

        # MonitoringBot.bot.register_next_step_handler(
        #     answer,
        #     MonitoringBot.actionsHandler,
        # )

    def onDatabaseSelected(message):
        username = message.from_user.username
        logger.debug(f'onDatabaseSelected(username={username})')

        if not MonitoringBot.__checkUserWhitelisted(message, username):
            return

        BotUsersDatabase.setSelectedDatabase(username, message.text)

        MonitoringBot.bot.send_message(
            message.chat.id,
            Strings.translate('selected_database') + message.text + '"',
            reply_markup=databaseActionsKeyboard(Strings.WEB_VIEW_URL),
        )

    def onShortcutSelected(message):
        text = message.text
        username = message.from_user.username
        logger.debug(f'onShortcutSelected(username={username})')

        if not MonitoringBot.__checkUserWhitelisted(message, username):
            return
        
        shortcut = None
        if text == Strings.translate('shortcut_restart'):
            shortcut = 'restart'
        elif text == Strings.translate('shortcut_backup'):
            shortcut = 'backup'
        elif text == Strings.translate('shortcut_terminate'):
            shortcut = 'terminate'
        elif text == Strings.translate('shortcut_restore'):
            shortcut = 'restore'
        elif text == Strings.translate('shortcut_shutdown'):
            shortcut = 'shutdown'

        # TODO: Send action to backend

        MonitoringBot.bot.send_message(
            message.chat.id,
            Strings.translate('selected_shortcut'),
            reply_markup=databaseActionsKeyboard(),
        )

    # @bot.message_handler(commands=['start'], is_whitelisted=True)
    @bot.message_handler(commands=['start'])
    def onStart(message):
        username = message.from_user.username
        logger.debug(f'onStart(username={username})')

        BotUsersDatabase.addUserIfNotExists(
            username=username,
            chatId=message.chat.id,
        )

        if MonitoringBot.__isUserWhitelisted(username):
            text = Strings.translate('welcome')
        else:
            text = Strings.translate('not_whitelisted')

        MonitoringBot.bot.reply_to(
            message,
            text,
            reply_markup=mainMenuKeyboard(showDebug=username in DEVS),
        )

    @bot.message_handler(commands=['databases'])
    def onDatabases(message):
        username = message.from_user.username
        logger.debug(f'onDatabases(username={username})')

        if not MonitoringBot.__checkUserWhitelisted(message, username):
            return

        databases = MonitoringBot.getDatabasesByUser(username)

        answer = MonitoringBot.bot.send_message(
            message.chat.id,
            Strings.translate('select_database'),
            reply_markup=databasesKeyboard(databases),
        )

        MonitoringBot.bot.register_next_step_handler(
            answer,
            MonitoringBot.onDatabaseSelected,
        )

    @bot.message_handler(commands=['current'])
    def onCurrentDatabase(message):
        username = message.from_user.username
        logger.debug(f'onCurrentDatabase(username={username})')

        if not MonitoringBot.__checkUserWhitelisted(message, username):
            return

        current = BotUsersDatabase.getSelectedDatabase(username)

        if current == None:
            text = Strings.translate('not_selected')
        else:
            text = Strings.translate('current_database') + current + '"'

        MonitoringBot.bot.send_message(message.chat.id, text)

    # TODO: Убрать
    @bot.message_handler(commands=['debug'])
    def onDebug(message):
        username = message.from_user.username
        logger.debug(f'onDebug(username={username})')

        MonitoringBot.__checkUserWhitelisted(message, username)

        info = BotUsersDatabase.getAll()

        if info == None:
            info = Strings.translate('empty')

        MonitoringBot.bot.send_message(message.chat.id, str(info))

    @bot.message_handler(commands=['actions'])
    def onShortcuts(message):
        username = message.from_user.username
        logger.debug(f'onShortcuts(username={username})')

        if not MonitoringBot.__checkUserWhitelisted(message, username):
            return

        selected = BotUsersDatabase.getSelectedDatabase(username)

        if selected == None:
            MonitoringBot.bot.send_message(
                message.chat.id,
                Strings.translate('not_selected'),
                reply_markup=types.ReplyKeyboardRemove(),
            )
            return

        answer = MonitoringBot.bot.send_message(
            message.chat.id,
            Strings.translate('select_shortcut') + selected + '"',
            reply_markup=shortcutsKeyboard(),
        )

        MonitoringBot.bot.register_next_step_handler(
            answer,
            MonitoringBot.onShortcutSelected,
        )

    @bot.message_handler(content_types=['text'])
    def mainMenuHandler(message):
        text = message.text
        username = message.from_user.username
        logger.debug(f'mainMenuHandler(username={username})')

        if not MonitoringBot.__checkUserWhitelisted(message, username):
            return

        if text == Strings.translate('menu_databases'):
            MonitoringBot.onDatabases(message)
        elif text == Strings.translate('menu_current'):
            MonitoringBot.onCurrentDatabase(message)
        elif text == Strings.translate('menu_main'):
            MonitoringBot.onStart(message)
        elif text == Strings.translate('menu_shortcuts'):
            MonitoringBot.onShortcuts(message)

        if text == Strings.translate('menu_debug') and username in DEVS:
            MonitoringBot.onDebug(message)

if __name__ == '__main__':
    MonitoringBot.run()
