from constants.strings import Strings
import telebot
import logging
import os
import requests

from telebot import types
from dotenv import load_dotenv
from database.bot_users_database import BotUsersDatabase

logger = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)

ACCESS_SERVICE_BASE_URL_KEY = 'ACCESS_SERVICE_BASE_URL'
WEB_VIEW_URL = 'https://monitoring-bot.netlify.app/'
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

    def sendMessageToUser(msg: str, user: str, reply_markup) -> None:
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

    def sendMessageToUsers(msg: str, users: list[str], reply_markup) -> None:
        logger.debug(f'sendMessageToUsers(msg = {msg}, users = {users})')
        for user in users:
            MonitoringBot.sendMessageToUser(user=user, msg=msg, reply_markup=reply_markup)

    def sendErrorMessageToUsers(msg: str, users: list[str], db_name: str) -> None:
        logger.debug(f'sendErrorMessageToUsers(msg = {msg}, users = {users})')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        shortcut_restart = types.KeyboardButton(text=Strings.translate('shortcut_restart'))
        shortcut_backup = types.KeyboardButton(text=Strings.translate('shortcut_backup'))
        shortcut_terminate = types.KeyboardButton(text=Strings.translate('shortcut_terminate'))
        shortcut_restore = types.KeyboardButton(text=Strings.translate('shortcut_restore'))

        markup.add(shortcut_restart, shortcut_restore, shortcut_backup, shortcut_terminate)

        answer = MonitoringBot.sendMessageToUsers(
            msg=Strings.translate('internal_error') +
            f'"{db_name}"\n\n' + '```sh\n' + msg + "\n```",
            users=users,
            reply_markup=markup,
        )

        MonitoringBot.bot.register_next_step_handler(
            answer,
            MonitoringBot.actionsHandler,
        )

    def __checkUserWhitelisted(message, username: str) -> bool:
        isWhitelisted = MonitoringBot.isUserWhitelisted(username)
        if not isWhitelisted:
            MonitoringBot.bot.reply_to(
                message, Strings.translate('not_whitelisted'),
            )
        return isWhitelisted

    def __getDatabasesByUser(username: str) -> list[str]:
        logger.debug(f'__getDatabasesByUser(username={username})')

        base = os.getenv(ACCESS_SERVICE_BASE_URL_KEY)
        path = Strings.DATABASES_PATH

        url = f'{base}/{path}'
        params = {'nickname': username}

        logger.debug(f'__getDatabasesByUser(url={url}, params={params})')

        response = requests.get(url, params=params)
        return response.json()['databases']

    def isUserWhitelisted(username: str):
        logger.debug(f'checkByUsername(username={username})')
        base = os.getenv(ACCESS_SERVICE_BASE_URL_KEY)
        path = Strings.CHECK_USER_PATH

        url = f'{base}/{path}'
        params = {'nickname': username}

        logger.debug(f'checkByUsername(url={url}, params = {params})')

        response = requests.get(url, params=params)
        logger.debug(f'checkByUsername(response={response})')

        return response.json()

    def selectDatabase(message):
        username = message.from_user.username
        logger.debug(f'selectDatabase(username={username})')

        if not MonitoringBot.__checkUserWhitelisted(message, username):
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        website = types.WebAppInfo(WEB_VIEW_URL)
        metrcis_button = types.KeyboardButton(
            text=Strings.translate('check_metrics'),
            web_app=website
        )
        menu_button = types.KeyboardButton(text=Strings.translate('menu_main'))
        markup.add(metrcis_button, menu_button)

        BotUsersDatabase.setSelectedDatabase(username, message.text)

        MonitoringBot.bot.send_message(
            message.chat.id,
            Strings.translate('selected_database') + message.text + '"',
            reply_markup=markup,
        )

    # @bot.message_handler(commands=['start'], is_whitelisted=True)
    @bot.message_handler(commands=['start'])
    def start(message):
        username = message.from_user.username
        logger.debug(f'start(username={username})')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        menu_databases = types.KeyboardButton(
            Strings.translate('menu_databases'))
        menu_current = types.KeyboardButton(Strings.translate('menu_current'))
        markup.add(menu_databases, menu_current)

        if username in DEVS:
            menu_debug = types.KeyboardButton(Strings.translate('menu_debug'))
            markup.add(menu_debug)

        BotUsersDatabase.addUserIfNotExists(
            username=username,
            chatId=message.chat.id,
        )

        if MonitoringBot.isUserWhitelisted(username):
            text = Strings.translate('welcome')
        else:
            text = Strings.translate('not_whitelisted')

        MonitoringBot.bot.reply_to(message, text, reply_markup=markup)

    @bot.message_handler(commands=['databases'])
    def databases(message):
        username = message.from_user.username
        logger.debug(f'databases(username={username})')

        if not MonitoringBot.__checkUserWhitelisted(message, username):
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        databases = MonitoringBot.__getDatabasesByUser(username)
        for database in databases:
            button = types.KeyboardButton(database)
            markup.add(button)

        answer = MonitoringBot.bot.send_message(
            message.chat.id,
            Strings.translate('select_database'),
            reply_markup=markup,
        )

        MonitoringBot.bot.register_next_step_handler(
            answer,
            MonitoringBot.selectDatabase,
        )

    @bot.message_handler(commands=['current'])
    def currentDatabase(message):
        username = message.from_user.username
        logger.debug(f'currentDatabase(username={username})')

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
    def debug(message):
        username = message.from_user.username
        logger.debug(f'debug(username={username})')

        MonitoringBot.__checkUserWhitelisted(message, username)

        info = BotUsersDatabase.getAll()

        if info == None:
            info = '<Пусто>'

        MonitoringBot.bot.send_message(message.chat.id, str(info))

    @bot.message_handler(content_types=['actions'])
    def actionsHandler(message):
        text = message.text
        username = message.from_user.username

        selected = BotUsersDatabase.getSelectedDatabase(username)

        if selected == None:
            text = Strings.translate('not_selected')
            return

        action = None
        if text == Strings.translate('shortcut_restart'):
            action = 'restart'
        elif text == Strings.translate('shortcut_backup'):
            action = 'backup'
        elif text == Strings.translate('shortcut_terminate'):
            action = 'terminate'
        elif text == Strings.translate('shortcut_restore'):
            action = 'restore'

        # TODO: Send action to backend

    @bot.message_handler(content_types=['text'])
    def mainMenuHandler(message):
        text = message.text
        username = message.from_user.username

        if text == Strings.translate('menu_databases'):
            MonitoringBot.databases(message)
        elif text == Strings.translate('menu_current'):
            MonitoringBot.currentDatabase(message)
        elif text == Strings.translate('menu_main'):
            MonitoringBot.start(message)

        if text == Strings.translate('menu_debug') and username in DEVS:
            MonitoringBot.debug(message)


if __name__ == '__main__':
    MonitoringBot.run()
