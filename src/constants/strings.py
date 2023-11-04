class Strings:
    current = 'ru'
    translations = {
        'ru': {
            'not_whitelisted': 'Извините, у вас недостаточно прав для взаимодействия с базами данных. Сообщите администратору, чтобы он добавил вас в белый список',
            'welcome': 'Добро пожаловать!',
            'internal_error': 'Произошла ошибка!\n\n[INTERNAL_ERROR]: ',
            'select_database': 'Выберите БД для дальнейшей работы',
        }
        # en = {}
        # us = {}
    }

    def translate(key: str) -> str:
        return Strings.translations[Strings.current][key]


    CHECK_USER_PATH = 'api/user/check'