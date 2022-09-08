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

    def load_page(self, page):
        url = f"https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{page}/c37l1700273"
        if page == 1:
            response = self.session.get(url=url)
        else:
            response = self.session.get(url=url, allow_redirects=False)
        response.raise_for_status()
        if response.status_code != 302:
            return response.text
        else:
            return ''

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
        item_beds = item.select_one("span.bedrooms")
        if item_beds:
            item_beds = item_beds.text.replace("\n", "").replace(" ", "").replace("Beds:", "")
        item_description = item.select_one("div.description").contents[0].strip()
        item_price = item.select_one("div.price").contents[0].strip()
        if item_price == "Please Contact":
            item_price = None
            item_currency = None
        else:
            item_price = item.select_one("div.price").contents[0].strip()[1:].replace(',', '')
            item_currency = item.select_one("div.price").contents[0].strip()[0]

        conn = engine.connect()
        ins_ad_query = ad_list.insert().values(
            image=item_image,
            title=item_title,
            date=item_date,
            location=item_location,
            beds=item_beds,
            description=item_description,
            price=item_price,
            currency=item_currency
        )
        conn.execute(ins_ad_query)
        conn.close()

    def run(self):
        page = 1
        while True:
            text = self.load_page(page)
            if text:
                self.parse_page(text)
            else:
                break
            page += 1
