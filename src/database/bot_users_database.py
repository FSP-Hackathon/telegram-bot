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

BOT_USERS_DATABASE_DROP_FILE = '/sql/bot_users_database_drop.sql'
BOT_USERS_DATABASE_INIT_FILE = '/sql/bot_users_database_init.sql'
BOT_USERS_DATABASE_INSERT_FILE = '/sql/bot_users_database_insert.sql'

logger = logging.getLogger(__name__)
logging.getLogger(__name__).setLevel(logging.DEBUG)


class BotUsersDatabase:
    connection = None

    def __getData():
        user = os.getenv(BOT_USERS_DB_USER_KEY)
        password = os.getenv(BOT_USERS_DB_PASS_KEY)
        host = os.getenv(BOT_USERS_DB_HOST_KEY)
        port = os.getenv(BOT_USERS_DB_PORT_KEY)
        dbName = os.getenv(BOT_USERS_DB_NAME_KEY)

        return user, password, host, port, dbName

    def __checkInit():
        if BotUsersDatabase.connection == None:
            logger.error('Error! Missing BotUsersDatabase init() method!')
            return

    def __getCursor():
        return BotUsersDatabase.connection.cursor()

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

            path = os.path.dirname(os.path.realpath(__file__))

            if drop:
                with open(path + BOT_USERS_DATABASE_DROP_FILE, 'r') as file:
                    sql = file.read()
                    BotUsersDatabase.__getCursor().execute(sql)
                    BotUsersDatabase.connection.commit()

            with open(path + BOT_USERS_DATABASE_INIT_FILE, 'r') as file:
                sql = file.read()
                BotUsersDatabase.__getCursor().execute(sql)
                BotUsersDatabase.connection.commit()

        except (Exception, Error) as e:
            logging.error(f'Error while working with BotUsersDatabase! {e}')

    def addUserIfNotExists(username: str, chatId: str) -> None:
        logger.debug(f'addUserIfNotExists(username = {username}, chatId = {chatId})')
        BotUsersDatabase.__checkInit()
        path = os.path.dirname(os.path.realpath(__file__))

        logger.debug(f'addUserIfNotExists(path = {path}')

        with open(path + BOT_USERS_DATABASE_INSERT_FILE, 'r') as file:
            sql = file.read()
            logger.debug(f'addUserIfNotExists(sql = {sql}')
            BotUsersDatabase.__getCursor().execute(sql, (username, chatId))
            BotUsersDatabase.connection.commit()

    def setSelectedDatabase(username: str, selectedDatabase: str):
        logger.debug(
            f'setSelectedDatabase(username = {username}, selectedDatabase = {selectedDatabase})'
        )
        BotUsersDatabase.__checkInit()

        sql = f'UPDATE bot_users SET selected_db = %s WHERE username = %s'
        logger.debug(f'setSelectedDatabase(sql = {sql}')

        BotUsersDatabase.__getCursor().execute(sql, (username, selectedDatabase))
        BotUsersDatabase.connection.commit()

    def getAll():
        logger.debug(f'getAll()')
        BotUsersDatabase.__checkInit()

        sql = f'SELECT * FROM bot_users'
        cursor = BotUsersDatabase.__getCursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        logger.debug(f'getAll(result = {result})')        
        return result

    def getSelectedDatabase(username: str):
        logger.debug(f'getSelectedDatabase(username = {username})')
        BotUsersDatabase.__checkInit()

        sql = f'SELECT selected_db FROM bot_users WHERE username = %s'
        logger.debug(f'getSelectedDatabase(sql = {sql})')

        cursor = BotUsersDatabase.__getCursor()
        cursor.execute(sql, (username,))
        result = cursor.fetchone()

        logger.debug(f'getSelectedDatabase(result = {result})')
        
        if result == None:
            return None
        
        return result[0]

    def getChatIdByUsername(username: str):
        BotUsersDatabase.__checkInit()

        logger.debug(f'getChatIdByUsername(username = {username})')
        cursor = BotUsersDatabase.__getCursor()
    
        cursor.execute('SELECT * FROM bot_users')
        logger.debug(
            f'getChatIdByUsername(all = {cursor.fetchall()})',
        )

        cursor.execute(
            'SELECT chat_id FROM bot_users WHERE username = %s', (username,),
        )

        result = cursor.fetchone()

        logger.debug(f'getChatIdByUsername(result = {result})')
        
        if result == None:
            return None
        
        return result[0]
        
