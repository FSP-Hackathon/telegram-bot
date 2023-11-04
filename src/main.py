from api import runApi
from bot import Bot
import threading

def main() -> None:
    thread = threading.Thread(target = runApi)
    thread.start()
    
    Bot.runBot()

if __name__ == '__main__':
    main()
