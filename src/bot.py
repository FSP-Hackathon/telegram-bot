import logging
import os
import traceback
import asyncio

from dotenv import load_dotenv
from telegram import Update

from constants.strings import Strings
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from database.bot_users_database import BotUsersDatabase


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.DEBUG)
logging.getLogger(__name__).setLevel(logging.DEBUG)

ERRORS, METRICS, STATUS, BIO = range(4)
BOT_TOKEN_KEY = 'BOT_TOKEN'

admins = ['OwlCodR']

load_dotenv()


class Bot:
    def __getToken() -> str:
        return os.getenv(BOT_TOKEN_KEY)

    def __getChatIdsByUsernames(users: list) -> list:
        logger.debug(f'__getChatsOfUsers(users = {users})')

        chats = []
        for user in users:
            chat = BotUsersDatabase.getChatIdByUsername(user)
            if chat != None:
                chats.append(chat)
        logger.debug(f'__getChatsOfUsers(chats = {chats})')

        return chats

    def __getAdmins() -> str:
        return Bot.__getChatIdsByUsernames(admins)

    def isUserWhitelisted(username: int) -> bool:
        # TODO: Send request and check if user whitelisted
        return True

    async def notifyUsers(
        users: list,
        message: str,
        parse_mode=None,
    ):
        logger.debug(f'notifyUsers(users = {users})')

        chats = Bot.__getChatIdsByUsernames(users)

        for chat in chats:
            logger.debug(f'notifyUsers(chat = {chat})')
            await Bot.context.bot.send_message(
                chat_id=chat,
                text=message,
            )

    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        Bot.context = context
        logger.error("Exception while handling an update:",
                     exc_info=context.error)

        exceptions = traceback.format_exception(
            None,
            context.error,
            context.error.__traceback__
        )
        error_text = "```md\n" + "".join(exceptions) + "\n```"

        await Bot.notifyUsers(
            users=Bot.__getAdmins(),
            message=Strings.translate('internal_error') + error_text,
            parse_mode=ParseMode.MARKDOWN,
        )

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        Bot.context = context

        username = update.message.from_user['username']
        logger.debug(f'start(username = {username})')

        isWhitelisted = Bot.isUserWhitelisted(username)
        logger.debug(f'start(isWhitelisted = {isWhitelisted})')

        if not isWhitelisted:
            await update.message.reply_text(
                Strings.translate('not_whitelisted'),
            )
            return

        BotUsersDatabase.addUserIfNotExists(
            update.message.from_user.username,
            update.message.chat.id
        )

        await update.message.reply_text(
            Strings.translate('welcome'),
        )

    def runBot() -> None:
        token = Bot.__getToken()

        BotUsersDatabase.init(drop=False)

        application = Application.builder().token(token).build()

        # conv_handler = ConversationHandler(
        #     entry_points=[CommandHandler("start", start)],
        #     states={
        #         ERRORS: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
        #         METRICS: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
        #         LOCATION: [
        #             MessageHandler(filters.LOCATION, location),
        #             CommandHandler("skip", skip_location),
        #         ],
        #         BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        #     },
        #     fallbacks=[CommandHandler("cancel", cancel)],
        # )

        application.add_error_handler(Bot.error_handler)

        application.add_handler(CommandHandler("start", Bot.start))

        # application.add_handler(conv_handler)

        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    Bot.runBot()
