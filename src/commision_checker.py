from typing import List
import pickle
import os
import json

from selenium import webdriver
from requests import Session


class CommisionChecker:
    fname: str = ''
    session: Session = Session()

    def __init__(self, fname):
        self.fname = fname

    def check_session(self):
        if os.path.exists(self.fname):
            self.load()
        else:
            self.get_session()

    def get_commision(self, productid, price: List[str]):

        price = ','.join(price)

        url = 'https://portals.aliexpress.com/material/findProductById.do?productId={}&locale=en_US&currency=USD&price={}'.format(productid, price)

        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
        }

        req = self.session.get(url, headers=headers)
        self.save()
        return json.loads(req.text)

    def get_session(self):
        driver = webdriver.Chrome('./chromedriver.exe')
        url = "https://login.aliexpress.com/?flag=1&return_url=http%3A%2F%2Fportals.aliexpress.com%2Fwelcome.htm"
        driver.get(url)
        print("press enter if finish")
        input()

        cookies = self.parse_cookies(driver)
        self.session.get("https://portal.aliexpress.com", cookies=cookies)

        self.save()

    def parse_cookies(self, driver: webdriver.Chrome):
        cookies = driver.get_cookies()
        hasil = {}

        for cookie in cookies:
            hasil[cookie['name']] = cookie['value']

        return hasil

    def save(self):
        with open(self.fname, 'w+b') as out:
            pickle.dump(self.session, out)

    def load(self):
        with open(self.fname, 'rb') as out:
            self.session = pickle.load(out)


if __name__ == '__main__':
    checker = CommisionChecker('test.txt')
    checker.check_session()
    hasil = checker.get_commision('4000708838521', ["11.88", "66.42"])
    print(hasil)
