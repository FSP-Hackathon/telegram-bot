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

    def run() -> None:
        logger.debug(f'run()')
        BotUsersDatabase.init(drop=True)
        MonitoringBot.bot.add_custom_filter(WhitelistFilter())
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

    @bot.message_handler(commands=['start'], is_whitelisted=True)
    def start(message):
        logger.debug(f'start()')

        username = message.from_user.username

        BotUsersDatabase.addUserIfNotExists(
            username=username, 
            chatId=message.chat.id,
        )
        
        if WhitelistFilter.checkByUsername(username):
            text = Strings.translate('welcome') 
        else:
            text = Strings.translate('not_whitelisted')

        MonitoringBot.bot.reply_to(message, text)

# Не забывать проверять на is_whitelisted
class WhitelistFilter(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_whitelisted'

    @staticmethod
    def checkByUsername(username: str):
        logger.debug(f'checkByUsername(username={username})')
        base = os.getenv(ACCESS_SERVICE_BASE_URL_KEY)
        path = Strings.CHECK_USER_PATH

        url = f'{base}/{path}'
        params = {'nickname': username}

        logger.debug(f'checkByUsername(url={url}, params = {params})')

        response = requests.get(url, params=params)
        logger.debug(f'checkByUsername(response={response})')

        return bool(response)

    @staticmethod
    def check(message: telebot.types.Message) -> bool:
        username = message.from_user.username
        logger.debug(f'check(username={message.from_user.username})')
        return WhitelistFilter.checkByUsername(username)


if __name__ == '__main__':
    MonitoringBot.run()
