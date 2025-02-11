from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





@dataclass
class URLs:
    google = 'https://www.google.com/'
    nasdaq = 'https://www.nasdaq.com/market-activity/stocks'

@dataclass
class WebElements:
    search_google = (By.XPATH, '//*[@id="APjFqb"]')
    search_nasdaq_button = (By.CSS_SELECTOR, 'body > div.dialog-off-canvas-main-canvas > div.page.with-primary-nav.with-jupiter-sticky-nav > div.header-group > header > nav > div.primary-nav__right > input')
    search_nasdaq_bar = (By.XPATH, '//*[@id="nasdaq-search-overlay-input"]')
    popup_nasdaq = (By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
    search_nasdaq_button = (By.XPATH, '//*[@id="nasdaq-search-overlay-modal"]/div[2]/div/div/div[2]/div/form/button')


class DataCollector:
    """"""
    def __init__(self, url: str, web_diver_mode: str = ''):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.click(WebElements.popup_nasdaq)

    def get(self) -> BeautifulSoup:
        self.soup = BeautifulSoup(requests.get(self.url).content, 'html5lib')
        return self.soup

    def input(self, locator: tuple, value: str):
        """"""
        for _ in range(3):
            try:
                element = self.driver.find_element(locator[0], locator[1])
                element.send_keys(value)
                break
            except Exception as e:
                print('Input failed')

    def click(self, locator: tuple):
        """"""
        try:
            wait = WebDriverWait(self.driver, 10)
            button = wait.until(EC.visibility_of_element_located((locator[0], locator[1])))
            button.click()
        except Exception as e:
            print(f'Button not clicked due to {e}')


def login_and_collect_multiple_data(dc: DataCollector, list_of_targets: List, selenium_mode: str):
    """"""
    # login and open search
    dc.click(WebElements.search_nasdaq_button)
    for idx, target in enumerate(list_of_targets):
        dc.input(WebElements.search_nasdaq_bar, '')
        dc.click(WebElements.search_nasdaq_button)



### TESTS
if __name__ == '__main__':
    dc = DataCollector(URLs.nasdaq)
    # login_and_collect_multiple_data(dc=dc, selenium_mode='')
    dc.click(WebElements.search_nasdaq_button)
    dc.input(WebElements.search_nasdaq_bar, 'Nvidia')
    dc.click(WebElements.search_nasdaq_button)
    _=0