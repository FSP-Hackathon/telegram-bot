from api import runApi
from bot import Bot
import asyncio

def main() -> None:
    asyncio.run(runApi())
    asyncio.run(Bot.runBot())

if __name__ == '__main__':
    main()
