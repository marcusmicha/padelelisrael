import datetime
import uvicorn
from fastapi import FastAPI
from app.scraper import Scraper
from app.telegram import TelegramBot
from app.verifier import Verifier

previous_availabilities = {}
app = FastAPI()


@app.get("/field_of_the_day")
def get_fields_of_the_day():
    return fields_of_the_day()

def fields_of_the_day():
    global previous_availabilities
    today = datetime.datetime.now()
    bot = TelegramBot()
    scraper = Scraper(today)
    occupancies = scraper.execute()
    verifier = Verifier(occupancies, previous_availabilities=previous_availabilities)
    valid_availabilities, previous_availabilities, notification = verifier.verify()
    if valid_availabilities:
        print('valid')
        bot.send_notification(notification)
    else:
        print('not valid')
    return 0

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)