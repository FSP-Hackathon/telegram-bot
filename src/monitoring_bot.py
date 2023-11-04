from constants.strings import Strings
import telebot
import logging
import os
import requests

from telebot import TeleBot
from dotenv import load_dotenv

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

    def run():
        logger.debug(f'run()')
        MonitoringBot.bot.add_custom_filter(WhitelistFilter())
        MonitoringBot.bot.infinity_polling()

    @bot.message_handler(commands=['start'], is_whitelisted=True)
    def start(message):
        logger.debug(f'start()')
        MonitoringBot.bot.reply_to(message, Strings.translate('welcome'))

# Не забывать проверять на is_whitelisted


class WhitelistFilter(telebot.custom_filters.SimpleCustomFilter):
    key = 'is_whitelisted'

    @staticmethod
    def check(message: telebot.types.Message) -> bool:
        base = os.getenv(ACCESS_SERVICE_BASE_URL_KEY)
        path = Strings.CHECK_USER_PATH

        url = f'{base}/{path}'
        params = {'nickname': message.from_user.username}

        response = requests.get(url, params=params)
        return bool(response)


if __name__ == '__main__':
    MonitoringBot.run()
