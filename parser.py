import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
from db import ad_list, engine


class Client:
    def __init__(self):
        ua = UserAgent()

        self.session = requests.Session()
        self.session.headers = {
            'accept': '*/*',
            'user-agent': ua.chrome
        }

    def load_page(self):
        url = "https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273"
        response = self.session.get(url=url)
        response.raise_for_status()
        return response.text

    def parse_page(self, text: str):
        soup = BeautifulSoup(text, "lxml")
        all_adds = soup.findAll(class_="search-item")
        for item in all_adds:
            self.parse_item(item=item)

    def parse_item(self, item):
        item_image = item.select_one("div.image").find("img").get("data-src")
        item_title = item.select_one("a.title ").text.strip()
        parse_date = item.select_one("div.location").select_one("span.date-posted").text
        try:
            item_date = datetime.strftime(datetime.strptime(parse_date, '%d/%m/%Y'), '%d/%m/%Y').replace("/", '-')
        except ValueError:
            item_date = parse_date
        item_location = item.select_one("div.location").find("span").text.strip()
        item_beds = item.select_one("span.bedrooms").text.replace("\n", "").replace(" ", "")[5:]
        item_description = item.select_one("div.description").contents[0].strip()
        item_price = item.select_one("div.price").contents[0].strip()

        conn = engine.connect()
        ins_ad_query = ad_list.insert().values(
            image=item_image,
            title=item_title,
            date=item_date,
            location=item_location,
            beds=item_beds,
            description=item_description,
            price=item_price
        )
        conn.execute(ins_ad_query)
        conn.close()

    def run(self):
        text = self.load_page()
        self.parse_page(text)
