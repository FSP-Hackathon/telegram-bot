# 🌠 Telegram бот на Python для мониторинга состояния БД
---

## 📦 Стек
- [pyTelegramBotAPI]([https://python-telegram-bot.org/](https://pypi.org/project/pyTelegramBotAPI/))
- psycopg2
- Flask
- logging
- python-dotenv

## 🛰️ Технические фичи
- Поддержка сбора метрик с нескольких БД
- Графики и дашборды
- Не только general информация, но так же логи + ошибки
- Сводка новостей за день
- Заранее подготовленные шорткаты (Кол-во строк в разных таблицах)
- Выбор из готовых, безопасность
- Система ролей в бота
- Подтверждение действий пользователей
- Быстрое развертывание

## ✨ Продуктовые фичи
- Система ролей
- Уведомление пользователей

## 📚 Архитектура
![Архитектура](https://i.imgur.com/N6tubej.png)

## User-Flow
![User-Flow](https://i.imgur.com/gDUInkX.png)

## 🚀 Getting started
1. `pip install -r requirements.txt`
2. `sudo python3 ./src/main.py`
