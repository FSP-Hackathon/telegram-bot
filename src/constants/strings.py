class Strings:
    current = 'ru'
    translations = {
        'ru': {
            'not_whitelisted': '⚠️ Извините, у вас недостаточно прав для взаимодействия с базами данных. Сообщите администратору, чтобы он добавил вас в белый список',
            'welcome': '😉 Добро пожаловать!',
            'internal_error': '❌ Произошла ошибка в базе данных ',
            'select_database': 'Выберите БД для дальнейшей работы',
            'selected_database': 'Теперь вы работаете с базой данных "',
            'current_database': 'Текущая выбранная база данных: "',
            'not_selected': 'База данных еще не выбрана!',
            'check_metrics': '📊 Посмотреть статистику',
            'menu_databases': '🗃️ Доступные БД',
            'menu_current': '📂 Выбранная БД',
            'menu_debug': '⚙️ Для разработчиков',
            'menu_main': '🔍 В главное меню',
            'shortcut_restart': '🔄 Перезагрузить',
            'shortcut_backup': '📥 Создать бекап',
            'shortcut_terminate': '☠️ Прервать соединения',
            'shortcut_shutdown': '⛔ Выключить',
            'shortcut_restore': '♻️ Восстановить',
        }
        # en = {}
        # us = {}
    }

    def translate(key: str) -> str:
        return Strings.translations[Strings.current][key]


    CHECK_USER_PATH = 'api/user/check' # Находится ли юзер в вайтлисте
    DATABASES_PATH = 'api/user/databases' # Какие БД доступны юзеру
    DATABASE_USERS_PATH = 'api/database/users' # Какие юзеры имеют доступ к БД