# Шаблон для Telegram бота на python 
> Основная библиотека [python-telegram-bot](https://python-telegram-bot.org/)

### Технические фичи
- Поддержка горизонтального масштабирвоания
    > ???
- Скорость работы
    > Используем асинхронку `async/await`
- Резервное копирование и восстановление
    > Делаем бекапы
- Балансировка нагрузки 
    > Используем nginx
- Мониторинг и логирование
    > Используем `logging` и ???
- Быстрое развертывание
    > Упаковываем бота в `docker-compose`
- Обработка ошибок
    > Делаем [error_handler](https://docs.python-telegram-bot.org/en/v20.6/examples.errorhandlerbot.html)

### Продуктовые фичи
- Система ролей
- Уведомление пользователей

### Технические вопросы
- Как обращаться к боту с внешнего сервера?
- Может ли бот первым пичать пользователям?
- Можно ли создавать несколько инстансов бота?

## Getting started
1. `pip install -r requirements.txt`