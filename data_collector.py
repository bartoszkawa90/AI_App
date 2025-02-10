from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@dataclass
class URLs:
    google = 'https://www.google.com/'
    nasdaq = 'https://www.nasdaq.com/market-activity/stocks'

@dataclass
class WebElements:
    search_google = (By.XPATH, '//*[@id="APjFqb"]')
    search_nasdaq = (By.XPATH, '/html/body/div[2]/div[1]/div[1]/header/nav/div[2]/input')


class DataCollector:
    """"""
    def __init__(self, url: str):
        self.url = url
        r = requests.get(url)
        self.soup = BeautifulSoup(r.content, 'html5lib')
        self.driver = webdriver.Chrome()
        self.driver.get(url)

    def get(self) -> BeautifulSoup:
        self.soup = BeautifulSoup(requests.get(self.url).content, 'html5lib')
        return self.soup


### TESTS
if __name__ == '__main__':
    dc = DataCollector(URLs.google)
    _=0