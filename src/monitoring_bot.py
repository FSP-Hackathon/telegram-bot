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

    def sendMessageToUser(msg: str, user: str) -> None:
        logger.debug(f'sendMessageToUser(user = {user}, msg = {msg})')
        chat = MonitoringBot.__getChatOfUser(user)

        if chat == None:
            logger.warning(f'chat_id of user {user} is None!')
            return

        MonitoringBot.bot.send_message(chat_id=chat, text=msg)

    def sendMessageToUsers(msg: str, users: list[str]) -> None:
        logger.debug(f'sendMessageToUsers(msg = {msg}, users = {users})')
        for user in users:
            MonitoringBot.sendMessageToUser(user=user, msg=msg)

    def __checkUserWhitelisted(message, username: str) -> bool:
        isWhitelisted = MonitoringBot.isUserWhitelisted(username)
        if not isWhitelisted:
            MonitoringBot.bot.reply_to(message, Strings.translate('not_whitelisted'))
        return isWhitelisted

    def __getDatabasesByUser(username: str) -> list[str]:
        # TODO: Получение спискаБД с сервера
        return ['БД1', 'База данных полльзователей', 'БД Маши! Не трогать!']

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

    # @bot.message_handler(commands=['start'], is_whitelisted=True)
    @bot.message_handler(commands=['start'])
    def start(message):
        username = message.from_user.username
        logger.debug(f'start(username={username})')

        BotUsersDatabase.addUserIfNotExists(
            username=username,
            chatId=message.chat.id,
        )

        if MonitoringBot.isUserWhitelisted(username):
            text = Strings.translate('welcome')
        else:
            text = Strings.translate('not_whitelisted')

        MonitoringBot.bot.reply_to(message, text)

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

        MonitoringBot.bot.register_next_step_handler(answer, MonitoringBot.selectDatabase)

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

        MonitoringBot.bot.send_message(message.chat.id, info)

    def selectDatabase(message):
        username = message.from_user.username
        logger.debug(f'selectDatabase(username={username})')

        if not MonitoringBot.__checkUserWhitelisted(message, username):
            return

        markup = types.ReplyKeyboardRemove()

        BotUsersDatabase.setSelectedDatabase(username, message.text)

        MonitoringBot.bot.send_message(
            message.chat.id, 
            Strings.translate('selected_database') + message.text + '"', 
            reply_markup=markup,
        )

if __name__ == '__main__':
    MonitoringBot.run()
