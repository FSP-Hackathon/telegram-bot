from api import runApi
import threading
import argparse

from monitoring_bot import MonitoringBot

# TODO
# 1. Проврека на админа в каждом запросе +
# 2. Алертинг +
# 3. Интеграция WebView +
# 4. Шорткаты +
# 5. Базовая навигация с кнопками +
# 6. Получение списка доступных БД с сервера +
# 7. Менюшка на старте +
# 8. Рекомендации
# 9. Docker


def main(drop=False) -> None:
    thread = threading.Thread(target=MonitoringBot.run, args=(drop,))
    thread.start()

    runApi()

    thread.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", type=bool, default=False)

    args = parser.parse_args()

    main(drop=args.drop)
