from api import runApi
from bot import Bot
import threading

from monitoring_bot import MonitoringBot

# TODO
# 1. Проврека на админа в кажом запросе
# 2. Алертинг
# 3. Интеграция WebView
# 4. Шорткаты
# 5. Базовая навигация с кнопками

def main() -> None:
    thread = threading.Thread(target = MonitoringBot.run)
    thread.start()
    
    runApi()

    thread.join()

if __name__ == '__main__':
    main()
