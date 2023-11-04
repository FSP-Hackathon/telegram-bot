from api import runApi
from bot import Bot


def main() -> None:
    runApi()
    Bot.runBot()


if __name__ == '__main__':
    main()
