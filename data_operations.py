import yfinance as yf
import pandas as pd


# def download_stock_training_data(stock: str, file1: str, file2:str, period='3y', interval='1d'):
#     """
#     Function for downloading data about stock prices from last 3 years, function splits data into two
#     chunks (training data and validation data), chunks are being saved into separated files
#     NOTE: Different period or interval can be selected but for main purposes of this project it should not be
#     :param stock: Stock name
#     :param file1: File for training data (from 3yr ago to 1yr ago)
#     :param file2: File for validation data (from 1yr ago to now)
#     :param period: time period for data
#     :param interval: time interval for stock data
#     :return: None
#     """
#     # Download data
#     stock = yf.download(stock, period=period, interval=interval)
#
#     # Convert index to datetime (just in case)
#     stock.index = pd.to_datetime(stock.index)
#
#     # Get today's date and calculate cutoff dates
#     today = pd.Timestamp.today()
#     one_year_ago = today - pd.DateOffset(years=1)
#
#     # Split into two chunks
#     chunk_1 = stock[stock.index < one_year_ago]  # 3 years ago to 1 year ago
#     chunk_2 = stock[stock.index >= one_year_ago]  # 1 year ago to now
#
#     # Save to files
#     with open(file1, "a") as csv_1, open(file2, "a") as csv_2:
#         csv_1.write('Date,Close,High,Low,Open,Volume \n')
#         csv_2.write('Date,Close,High,Low,Open,Volume \n')
#     chunk_1.to_csv(file1, header=False, mode='a')
#     chunk_2.to_csv(file2, header=False, mode='a')


def download_stock_training_data(stock: str, file1: str, file2: str, period='3y', interval='1d'):
    """
    Download stock data from yfinance and compute additional technical indicators.
    The data is split into two sets:
      - Training data: from 3 years ago to 1 year ago
      - Validation data: from 1 year ago to now

    The saved CSV files will include:
      Date, Close, High, Low, Open, Volume,
      MACD, CCI, ATR, BOLL, EMA20, MA5, MA10, MTM6, MTM12,
      ROC, SMI, WVAD, Exchange rate, Interest rate

    :param stock: Stock symbol (e.g. 'AAPL')
    :param file1: File path for training data CSV (3 years ago to 1 year ago)
    :param file2: File path for validation data CSV (1 year ago to now)
    :param period: Period for downloading data from yfinance (default is '3y')
    :param interval: Interval for the stock data (default is '1d')
    :return: None
    """
    # Download historical data
    df = yf.download(stock, period=period, interval=interval)

    # Compute technical indicators and extra features

    # MACD: Difference between the 12-period and 26-period EMA of the Close price.
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()

    # CCI (Commodity Channel Index): (Close - 20-day MA) divided by (0.015 * rolling 20-day std)
    df['CCI'] = (df['Close'] - df['Close'].rolling(window=20).mean()) / (0.015 * df['Close'].rolling(window=20).std())

    # ATR (Average True Range): Difference between the rolling 14-day max of High and min of Low.
    df['ATR'] = df['High'].rolling(window=14).max() - df['Low'].rolling(window=14).min()

    # BOLL (Bollinger Bands): 20-day MA plus 2 times 20-day standard deviation of Close.
    df['BOLL'] = df['Close'].rolling(window=20).mean() + 2 * df['Close'].rolling(window=20).std()

    # EMA20: 20-day Exponential Moving Average of Close.
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

    # MA5 and MA10: 5-day and 10-day Simple Moving Averages of Close.
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()

    # MTM6 and MTM12: Momentum computed as the difference in Close over 6 and 12 periods.
    df['MTM6'] = df['Close'].diff(periods=6)
    df['MTM12'] = df['Close'].diff(periods=12)

    # ROC (Rate Of Change): Percent change in Close over 12 periods.
    df['ROC'] = df['Close'].pct_change(periods=12)

    # SMI (Stochastic Momentum Index): Deviation of the Close from its 14-day MA normalized by
    # the range of High and Low over 14 days.
    df['SMI'] = (df['Close'] - df['Close'].rolling(window=14).mean()) / (
                df['High'].rolling(window=14).max() - df['Low'].rolling(window=14).min())

    # WVAD: (Close - Open) multiplied by Volume.
    df['WVAD'] = (df['Close'] - df['Open']) * df['Volume']

    # Exchange rate and Interest rate: placeholders (replace with actual data as needed).
    df['Exchange rate'] = 1.0
    df['Interest rate'] = 1.0

    # Reset the index so that the Date becomes a column.
    df.reset_index(inplace=True)

    # Define the desired order for the CSV columns, omitting "Predicted Close Price".
    desired_columns = [
        'Date', 'Close', 'High', 'Low', 'Open', 'Volume',
        'MACD', 'CCI', 'ATR', 'BOLL', 'EMA20',
        'MA5', 'MA10', 'MTM6', 'MTM12', 'ROC',
        'SMI', 'WVAD', 'Exchange rate', 'Interest rate'
    ]
    df = df[desired_columns]

    # Ensure the Date column is in datetime format for proper filtering.
    df['Date'] = pd.to_datetime(df['Date'])

    # Determine the cutoff date (one year ago from today).
    today = pd.Timestamp.today()
    one_year_ago = today - pd.DateOffset(years=1)

    # Split the data: training data from 3 years ago to 1 year ago,
    # and validation data from 1 year ago to now.
    chunk_1 = df[df['Date'] < one_year_ago]
    chunk_2 = df[df['Date'] >= one_year_ago]

    # Define the CSV header.
    header = ','.join(desired_columns) + '\n'

    # Write the header to each file and append the respective data chunks.
    with open(file1, "a") as csv_1, open(file2, "a") as csv_2:
        csv_1.write(header)
        csv_2.write(header)

    # Save the data without writing the header (since it was already written).
    chunk_1.to_csv(file1, header=False, index=False, mode='a')
    chunk_2.to_csv(file2, header=False, index=False, mode='a')


def download_stock_training_not_divided(stock: str, file: str, period='3y', interval='1d'):
    """
    Download stock data from yfinance and compute additional technical indicators.
    The data is split into two sets:
      - Training data: from 3 years ago to 1 year ago
      - Validation data: from 1 year ago to now

    The saved CSV files will include:
      Date, Close, High, Low, Open, Volume,
      MACD, CCI, ATR, BOLL, EMA20, MA5, MA10, MTM6, MTM12,
      ROC, SMI, WVAD, Exchange rate, Interest rate

    :param stock: Stock symbol (e.g. 'AAPL')
    :param file1: File path for training data CSV (3 years ago to 1 year ago)
    :param file2: File path for validation data CSV (1 year ago to now)
    :param period: Period for downloading data from yfinance (default is '3y')
    :param interval: Interval for the stock data (default is '1d')
    :return: None
    """
    # Download historical data
    df = yf.download(stock, period=period, interval=interval)

    # Compute technical indicators and extra features

    # MACD: Difference between the 12-period and 26-period EMA of the Close price.
    df['MACD'] = df['Close'].ewm(span=12, adjust=False).mean() - df['Close'].ewm(span=26, adjust=False).mean()

    # CCI (Commodity Channel Index): (Close - 20-day MA) divided by (0.015 * rolling 20-day std)
    df['CCI'] = (df['Close'] - df['Close'].rolling(window=20).mean()) / (0.015 * df['Close'].rolling(window=20).std())

    # ATR (Average True Range): Difference between the rolling 14-day max of High and min of Low.
    df['ATR'] = df['High'].rolling(window=14).max() - df['Low'].rolling(window=14).min()

    # BOLL (Bollinger Bands): 20-day MA plus 2 times 20-day standard deviation of Close.
    df['BOLL'] = df['Close'].rolling(window=20).mean() + 2 * df['Close'].rolling(window=20).std()

    # EMA20: 20-day Exponential Moving Average of Close.
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

    # MA5 and MA10: 5-day and 10-day Simple Moving Averages of Close.
    df['MA5'] = df['Close'].rolling(window=5).mean()
    df['MA10'] = df['Close'].rolling(window=10).mean()

    # MTM6 and MTM12: Momentum computed as the difference in Close over 6 and 12 periods.
    df['MTM6'] = df['Close'].diff(periods=6)
    df['MTM12'] = df['Close'].diff(periods=12)

    # ROC (Rate Of Change): Percent change in Close over 12 periods.
    df['ROC'] = df['Close'].pct_change(periods=12)

    # SMI (Stochastic Momentum Index): Deviation of the Close from its 14-day MA normalized by
    # the range of High and Low over 14 days.
    df['SMI'] = (df['Close'] - df['Close'].rolling(window=14).mean()) / (
                df['High'].rolling(window=14).max() - df['Low'].rolling(window=14).min())

    # WVAD: (Close - Open) multiplied by Volume.
    df['WVAD'] = (df['Close'] - df['Open']) * df['Volume']

    # Exchange rate and Interest rate: placeholders (replace with actual data as needed).
    df['Exchange rate'] = 1.0
    df['Interest rate'] = 1.0

    # Reset the index so that the Date becomes a column.
    df.reset_index(inplace=True)

    # Define the desired order for the CSV columns, omitting "Predicted Close Price".
    desired_columns = [
        'Date', 'Close', 'High', 'Low', 'Open', 'Volume',
        'MACD', 'CCI', 'ATR', 'BOLL', 'EMA20',
        'MA5', 'MA10', 'MTM6', 'MTM12', 'ROC',
        'SMI', 'WVAD', 'Exchange rate', 'Interest rate'
    ]
    df = df[desired_columns]

    # Ensure the Date column is in datetime format for proper filtering.
    df['Date'] = pd.to_datetime(df['Date'])

    # Define the CSV header.
    header = ','.join(desired_columns) + '\n'

    with open(file, "a") as csv:
        csv.write(header)
    df.to_csv(file, header=False, index=False, mode='a')


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
    # Read CSV
    df = pd.read_csv(file)
    # Collect specific column data and date
    close_data = getattr(df, column)
    date = getattr(df, "Date")
    data = {}
    # Pack date and data from column into dict
    for daytime, value in zip(date, close_data):
        data[daytime] = value
    return data


# ### TEST
# if __name__ == '__main__':
#     from list_of_actions import stocks
#     for idx, stock in enumerate(stocks[:20]):
#         # download_stock_training_data(stock[0], f"/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/"
#         #                          f"actions_data/train/train{idx}_{stock[1]}.csv",
#         #                f"/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/"
#         #                f"actions_data/verify/verify{idx}_{stock[1]}.csv")
#         download_stock_training_not_divided(stock[0], f"/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/"
#                                  f"actions_data/connected_training_data/{idx}_{stock[1]}.csv",)
#
#     # data = get_stock_data_from_csv('/Users/bartoszkawa/Desktop/REPOS/GitHub/AI_App/AI_App/actions_data/train/train0_Aon plc Class A.csv', 'Close')
