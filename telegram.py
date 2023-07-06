import os
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

class TelegramBot:
    def __init__(self) -> None:
        self.bot_token = BOT_TOKEN
        self.chat_id = CHAT_ID
        self.url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage'

    def send_message(self, message) -> None:
        r = requests.post(self.url, json={
            'chat_id': self.chat_id,
            'parse_mode': 'MarkdownV2',
            'text': message
        })
        print(r.text)
        return r.text