import datetime
import time
from scraper import Scraper
from telegram import TelegramBot
from helpers import pretty_availabilities

def main():
    """ Main program """
    print('lets start')
    today = datetime.datetime.now()
    bot = TelegramBot()
    scraper = Scraper(today)
    while(True):
        availabilities = scraper.execute()
        res = pretty_availabilities(availabilities)
        bot.send_message(res)
        time.sleep(300)
    return 0

if __name__ == "__main__":
    main()