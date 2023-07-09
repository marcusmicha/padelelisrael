import datetime
from fastapi import FastAPI
from app.scraper import Scraper
from app.telegram import TelegramBot
from app.verifier import Verifier

previous_availabilities = {}
app = FastAPI()


@app.get("/field_of_the_day")
def read_root():
    return fields_of_the_day()

def fields_of_the_day():
    global previous_availabilities
    print('lets start')
    today = datetime.datetime.now()
    bot = TelegramBot()
    scraper = Scraper(today)
    occupancies = scraper.execute()
    verifier = Verifier(occupancies, previous_availabilities=previous_availabilities)
    valid_availabilities, previous_avilabilities, notification = verifier.verify()
    if valid_availabilities:
        print('notif to send')
        print(notification)
        bot.send_notification(notification)
    return 0