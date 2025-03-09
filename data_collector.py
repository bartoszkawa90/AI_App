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

def data_collector(stock: str, file1: str, file2:str):
    # Download NVIDIA (NVDA) stock data for the last 3 years with weekly intervals
    stock = yf.download(stock, period="3y", interval="1wk")

    # Convert index to datetime (just in case)
    stock.index = pd.to_datetime(stock.index)

    # Get today's date and calculate cutoff dates
    today = pd.Timestamp.today()
    one_year_ago = today - pd.DateOffset(years=1)

    # Split into two chunks
    chunk_1 = stock[stock.index < one_year_ago]  # 3 years ago to 1 year ago
    chunk_2 = stock[stock.index >= one_year_ago]  # 1 year ago to now

    chunk_1.to_csv(file1)
    chunk_2.to_csv(file2)


if __name__ == '__main__':
    data_collector("NVDA", "/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/file1.csv",
                            "/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/file2.csv")
