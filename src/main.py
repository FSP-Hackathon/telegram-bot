from api import runApi
from bot import Bot
from multiprocessing import Process

def main() -> None:
    api = Process(target=runApi(), daemon=True)
    bot = Process(target=Bot.runBot(), daemon=True)
    api.start()
    bot.start()    

if __name__ == '__main__':
    main()
