from api import runApi
from bot import Bot
import asyncio
import threading

def main() -> None:
    thread = threading.Thread(target = Bot.runBot())
    thread.start()
    runApi()

if __name__ == '__main__':
    main()
