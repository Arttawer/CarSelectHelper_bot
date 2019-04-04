from bot import Bot

import logging

from telegram.ext import Updater
from telegram.ext import RegexHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

if __name__ == '__main__':
    bot = Bot()
    # bot.print_cars()
    bot.main()
