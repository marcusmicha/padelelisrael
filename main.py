import datetime
from scraper import Scraper
from telegram import TelegramBot
from helpers import pretty_availabilities

def main():
    """ Main program """
    today = datetime.datetime.now()
    bot = TelegramBot()
    scraper = Scraper(today)
    availabilities = scraper.execute()
    res = pretty_availabilities(availabilities)
    bot.send_message(res)
    return 0

if __name__ == "__main__":
    main()