import requests
from datetime import datetime, timedelta
import bs4 as bs
import re

class Scraper:
    def __init__(
            self, start_date: datetime,
            days_span:str = 0, place_ids:list = [4,5],
            key_id: str = 'hl90njda2b89k',
            url:str = 'https://padelisrael.matchpoint.com.es/Booking/Grid.aspx') -> None:
        self.start_date = start_date
        self.place_ids = place_ids
        self.days_span = days_span
        self.dates_to_scrape = self.get_dates_to_scrape()
        self.cookies = self.get_cookies()
        self.headers = self.get_headers()
        self.navigation_key = self.get_navigation_key(url, key_id)

    def get_good_format_date(self, date: datetime) -> str:
        return f"{date.day}/{date.month}/{date.year}"
    
    def get_dates_to_scrape(self) -> list:
        dates_to_scrape = []
        for i in range(self.days_span + 1):
            date_to_scrape = self.start_date + timedelta(days=i)
            dates_to_scrape.append(self.get_good_format_date(date_to_scrape))
        return dates_to_scrape
    
    def get_cookies(self) -> dict:
        cookies = {
            'ASP.NET_SessionId': 'sqyf3n551ivonf55vkquueqf',
            'Idioma': 'en-GB',
            'i18next': 'en-GB',
            'MPOpcionCookie': 'necesario',
        }
        return cookies
    
    def get_headers(self) -> dict:
        headers = {
            'authority': 'padelisrael.matchpoint.com.es',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json; charset=UTF-8',
            'cookie': 'ASP.NET_SessionId=sqyf3n551ivonf55vkquueqf; Idioma=en-GB; i18next=en-GB; MPOpcionCookie=necesario',
            'origin': 'https://padelisrael.matchpoint.com.es',
            'referer': 'https://padelisrael.matchpoint.com.es/Booking/Grid.aspx',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        return headers
    
    def get_navigation_key(self, url, id) -> str:
        html = requests.get(url).text
        soup = bs.BeautifulSoup(html, "html.parser")
        scripts = soup.find_all('script')
        for script in scripts:
            if id in script.text:
                tag = script.text.replace('\'', '')
                key = re.findall(f'(?<={id}=)(.+?)(?=;)', tag)[0]
                return key
    
    def request_field_by_date(self, date: str, field_id) -> requests.models.Response:
        json_data = {
            'idCuadro': field_id,
            'fecha': date,
            'key': self.navigation_key,
        }

        s = requests.Session() 
        response = s.post(
            'https://padelisrael.matchpoint.com.es/booking/srvc.aspx/ObtenerCuadro',
            cookies=self.cookies,
            headers=self.headers,
            json=json_data,
        )
        return response.json()
    
    def execute(self) -> dict:
        occupancies = {}
        for date in self.dates_to_scrape:
            occupancies[date] = {}
            for place_id in self.place_ids:
                res = self.request_field_by_date(date, place_id)
                field_name = res['d']['Nombre']
                occupancies[date][field_name] = {}
                for field in res['d']['Columnas']:
                    occupancies[date][field_name][field['TextoPrincipal']] = field
        return occupancies
    