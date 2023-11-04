from api import runApi
from bot import Bot
import threading

from monitoring_bot import MonitoringBot

def main() -> None:
    thread = threading.Thread(target = MonitoringBot.run)
    thread.start()
    
    runApi()

    thread.join()

if __name__ == '__main__':
    main()
