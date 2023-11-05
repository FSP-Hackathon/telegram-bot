class Strings:
    current = 'ru'
    translations = {
        'ru': {
            'not_whitelisted': '⚠️ Извините, у вас недостаточно прав для взаимодействия с базами данных. Сообщите администратору, чтобы он добавил вас в белый список',
            'welcome': '😉 Добро пожаловать!',
            'internal_error': '❌ [INTERNAL_ERROR] Произошла ошибка!\n\n',
            'select_database': 'Выберите БД для дальнейшей работы',
            'selected_database': 'Теперь вы работаете с базой данных "',
            'current_database': 'Текущая выбранная база данных: "',
            'not_selected': 'База данных еще не выбрана!',
            'check_metrics': '📊 Посмотреть статистику'
        }
        # en = {}
        # us = {}
    }

    def translate(key: str) -> str:
        return Strings.translations[Strings.current][key]


    CHECK_USER_PATH = 'api/user/check'