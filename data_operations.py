# import requests
# from bs4 import BeautifulSoup
# from dataclasses import dataclass
#
#
# @dataclass
# class URLs:
#     nasdaq = 'https://www.nasdaq.com/market-activity/stocks'
#
# def choose_period_sel():
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.common.keys import Keys
#     from time import sleep
#
#     driver = webdriver.Chrome()  # Or webdriver.Firefox()
#     driver.get(url)
#     sleep(10)
#     login_modal = driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')
#     login_modal.click()
#     sleep(3)
#     element = driver.find_element(By.XPATH,
#                                   "/html/body/div[2]/div/main/div[2]/article/div/div[2]/div/div[2]/div[2]/div[1]/div/div[1]/div[7]/button")
#     element.click()  # Simulate a click event
#
# class DataCollector:
#     @staticmethod
#     def collect_data(symbol: str):
#         """Fetches stock data from Nasdaq without using Selenium."""
#         url = f"https://www.nasdaq.com/market-activity/stocks/{symbol.lower()}"
#         headers = {"User-Agent": "Mozilla/5.0"}
#
#         response = requests.get(url, headers=headers)
#         if response.status_code != 200:
#             print("Failed to fetch data")
#             return None
#
#         soup = BeautifulSoup(response.content, 'html.parser')
#
#         # Extract stock price
#         name = soup.find("h1", {"class": "jupiter22-c-heading"}).text
#         table = soup.find("div", {"class": "table-group"})
#         chart = soup.find('div', {"class": "jupiter22-c-summary-chart__chart-container highcharts-light"})
#
#
#
#         price_element = soup.find("div", {"class": "symbol-page-header__pricing-price"})
#         stock_price = price_element.text.strip() if price_element else "Price not found"
#
#         return {"symbol": symbol, "price": stock_price}
#
#
# if __name__ == '__main__':
#     result = DataCollector.collect_data("NVDA")
#     print(result)


# ------------------------------------------------------------------------------------------------------------------------------------------------------

import yfinance as yf
import pandas as pd
from list_of_actions import stocks


def data_collector(stock: str, file1: str, file2:str):
    """
    Function for downloading data about stock prices from last 3 years, function splits data into two
    chunks (training data and validation data), chunks are being saved into separated files
    :param stock: Stock name
    :param file1: File for training data (from 3yr ago to 1yr ago)
    :param file2: File for validation data (from 1yr ago to now)
    :return: None
    """
    # Download data
    stock = yf.download(stock, period="3y", interval="1wk")

    # Convert index to datetime (just in case)
    stock.index = pd.to_datetime(stock.index)

    # Get today's date and calculate cutoff dates
    today = pd.Timestamp.today()
    one_year_ago = today - pd.DateOffset(years=1)

    # Split into two chunks
    chunk_1 = stock[stock.index < one_year_ago]  # 3 years ago to 1 year ago
    chunk_2 = stock[stock.index >= one_year_ago]  # 1 year ago to now

    # Save to files
    with open(file1, "a") as csv_1, open(file2, "a") as csv_2:
        csv_1.write('Date,Close,High,Low,Open,Volume \n')
        csv_2.write('Date,Close,High,Low,Open,Volume \n')
    chunk_1.to_csv(file1, header=False, mode='a')
    chunk_2.to_csv(file2, header=False, mode='a')


def extract_data(file: str, column: str) -> dict:
    """Function for extracting data from prepared csv stock file"""
    df = pd.read_csv(file)
    close_data = getattr(df, column).T[2:]
    date = getattr(df, column).T[2:]
    a=1


if __name__ == '__main__':
    for idx, stock in enumerate(stocks[:5]):
        data_collector(stock[0], f"/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/"
                                 f"actions_data/train/train{idx}_{stock[1]}.csv",
                                f"/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/"
                                f"actions_data/verify/verify{idx}_{stock[1]}.csv")

    # data = extract_data('/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/actions_data/train/train0_Aon plc Class A.csv', 'Close')
