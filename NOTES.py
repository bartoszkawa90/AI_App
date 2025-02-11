import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class URLs:
    nasdaq = 'https://www.nasdaq.com/market-activity/stocks'


class NasdaqScraper:
    @staticmethod
    def fetch_stock_data(symbol: str):
        """Fetches stock data from Nasdaq without using Selenium."""
        url = f"https://www.nasdaq.com/market-activity/stocks/{symbol.lower()}"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print("Failed to fetch data")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract stock price
        price_element = soup.find("div", {"class": "symbol-page-header__pricing-price"})
        stock_price = price_element.text.strip() if price_element else "Price not found"

        return {"symbol": symbol, "price": stock_price}


if __name__ == '__main__':
    result = NasdaqScraper.fetch_stock_data("NVDA")
    print(result)
