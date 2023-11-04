import os
import logging
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

BOT_USERS_DB_USER_KEY = 'BOT_USERS_DB_USER'
BOT_USERS_DB_PASS_KEY = 'BOT_USERS_DB_PASS'
BOT_USERS_DB_HOST_KEY = 'BOT_USERS_DB_HOST'
BOT_USERS_DB_PORT_KEY = 'BOT_USERS_DB_PORT'
BOT_USERS_DB_NAME_KEY = 'BOT_USERS_DB_NAME'

BOT_USERS_DATABASE_DROP_FILE = 'src/database/sql/bot_users_database_drop.sql'
BOT_USERS_DATABASE_INIT_FILE = 'src/database/sql/bot_users_database_init.sql'
BOT_USERS_DATABASE_INSERT_FILE = 'src/database/sql/bot_users_database_insert.sql'

logger = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)


class BotUsersDatabase:
    cursor = None
    connection = None

    def __getData():
        user = os.getenv(BOT_USERS_DB_USER_KEY)
        password = os.getenv(BOT_USERS_DB_PASS_KEY)
        host = os.getenv(BOT_USERS_DB_HOST_KEY)
        port = os.getenv(BOT_USERS_DB_PORT_KEY)
        dbName = os.getenv(BOT_USERS_DB_NAME_KEY)

        return user, password, host, port, dbName

    def __checkInit():
        if BotUsersDatabase.cursor == None or BotUsersDatabase.connection == None:
            logger.error('Error! Missing BotUsersDatabase init() method!')
            return

    def init(drop=False) -> None:
        logger.debug(f'init(drop = {drop})')
        try:
            user, password, host, port, dbName = BotUsersDatabase.__getData()

            BotUsersDatabase.connection = psycopg2.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=dbName,
            )

            BotUsersDatabase.cursor = BotUsersDatabase.connection.cursor()

            if drop:
                with open(BOT_USERS_DATABASE_DROP_FILE, 'r') as file:
                    sql = file.read()
                    BotUsersDatabase.cursor.execute(sql)
                    BotUsersDatabase.connection.commit()

            with open(BOT_USERS_DATABASE_INIT_FILE, 'r') as file:
                sql = file.read()
                BotUsersDatabase.cursor.execute(sql)
                BotUsersDatabase.connection.commit()

        except (Exception, Error) as e:
            logging.error(f'Error while working with BotUsersDatabase! {e}')

    def addUserIfNotExists(username: str, chatId: str) -> None:
        BotUsersDatabase.__checkInit()

        with open(BOT_USERS_DATABASE_INSERT_FILE, 'r') as file:
            sql = file.read()
            BotUsersDatabase.cursor.execute(sql, (username, chatId))
            BotUsersDatabase.connection.commit()

    def getChatIdByUsername(username: str):
        BotUsersDatabase.__checkInit()

        logger.debug(f'getChatIdByUsername(username = {username})')
        
        BotUsersDatabase.cursor = BotUsersDatabase.connection.cursor()

        BotUsersDatabase.cursor.execute('SELECT * FROM bot_users')
        logger.debug(f'getChatIdByUsername(all = {BotUsersDatabase.cursor.fetchall()})')

        BotUsersDatabase.cursor.execute(
            'SELECT * FROM bot_users WHERE username = %s', (username,),
        )
        
        result = BotUsersDatabase.cursor.fetchone()

        logger.debug(f'getChatIdByUsername(result = {result})')

        return result
