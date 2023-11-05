from api import runApi
from bot import Bot
import threading
import argparse

from monitoring_bot import MonitoringBot

# TODO
# 1. Проврека на админа в кажом запросе
# 2. Алертинг
# 3. Интеграция WebView
# 4. Шорткаты
# 5. Базовая навигация с кнопками

def main(drop=False) -> None:
    thread = threading.Thread(target = MonitoringBot.run, args=(drop,))
    thread.start()
    
    runApi()

    thread.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--drop", type=bool, default=False)

    args = parser.parse_args()

    main(drop=args.drop)
