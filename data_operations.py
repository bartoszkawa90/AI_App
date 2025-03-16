import yfinance as yf
import pandas as pd


def download_stock_training_data(stock: str, file1: str, file2:str, period='3y', interval='1wk'):
    """
    Function for downloading data about stock prices from last 3 years, function splits data into two
    chunks (training data and validation data), chunks are being saved into separated files
    NOTE: Different period or interval can be selected but for main purposes of this project it should not be
    :param stock: Stock name
    :param file1: File for training data (from 3yr ago to 1yr ago)
    :param file2: File for validation data (from 1yr ago to now)
    :param period: time period for data
    :param interval: time interval for stock data
    :return: None
    """
    # Download data
    stock = yf.download(stock, period=period, interval=interval)

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


def download_stock_data(stock: str, file: str,period: str, interval: str):
    """
    Function for downloading data about stock from last two years
    :param stock: Stock name
    :param file: file path to save csv
    :param period: time period for stock data
    :param interval: File for validation data (from 1yr ago to now)
    :return: None
    """
    # Download data
    stock = yf.download(stock, period=period, interval=interval)

    # Convert index to datetime (just in case)
    stock.index = pd.to_datetime(stock.index)

    # Get today's date and calculate cutoff dates
    today = pd.Timestamp.today()
    one_year_ago = today - pd.DateOffset(years=1)

    # Save to files
    with open(file, "a") as csv_1:
        csv_1.write('Date,Close,High,Low,Open,Volume \n')
    stock.to_csv(file, header=False, mode='a')


def get_stock_data_from_csv(file: str, column: str) -> dict:
    """Function for extracting data from prepared csv stock file, function returns data from one column with additional
     information about date and time
    :param file: Stock name
    :param column: File for training data (from 3yr ago to 1yr ago)
    :return: dict
    """
    df = pd.read_csv(file)
    close_data = getattr(df, column)
    date = getattr(df, "Date")
    data = {}
    for daytime, value in zip(date, close_data):
        data[daytime] = value
    return data


# ### TEST
# if __name__ == '__main__':
#     for idx, stock in enumerate(stocks[:3]):
#         download_stock_data(stock[0], f"/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/"
#                                  f"actions_data/train/train{idx}_{stock[1]}.csv",
#                        f"/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/"
#                        f"actions_data/verify/verify{idx}_{stock[1]}.csv")
# 
#     data = get_stock_data_from_csv('/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/actions_data/train/train0_Aon plc Class A.csv', 'Close')
