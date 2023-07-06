import datetime
from app.scraper import Scraper
from app.telegram import TelegramBot
from app.helpers import pretty_availabilities

from fastapi import FastAPI

app = FastAPI()

@app.get("/field_of_the_day")
def read_root():
    return fields_of_the_day()

def fields_of_the_day():
    print('lets start')
    today = datetime.datetime.now()
    bot = TelegramBot()
    scraper = Scraper(today)
    availabilities = scraper.execute()
    res = pretty_availabilities(availabilities)
    bot.send_message(res)
    return 0
