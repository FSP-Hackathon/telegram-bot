from api import runApi
from bot import Bot


def main() -> None:
    Bot.runBot()
    runApi()
    

if __name__ == '__main__':
    main()
