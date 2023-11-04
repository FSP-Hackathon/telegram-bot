from api import runApi
from bot import Bot
from multiprocessing import Process

def main() -> None:
    api = Process(target=runApi())
    bot = Process(target=Bot.runBot())
    api.start()
    bot.start()    

if __name__ == '__main__':
    main()
