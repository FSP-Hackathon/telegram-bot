from api import runApi
from bot import Bot
import asyncio
import threading

def main() -> None:
    loop = asyncio.new_event_loop()

    thread = threading.Thread(target = Bot.runBot, args = (loop,))
    thread.start()
    runApi()

if __name__ == '__main__':
    main()
