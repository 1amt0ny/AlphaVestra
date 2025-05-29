# src/data/download_data.py

import yfinance as yf
import pandas as pd
import os

# Download stock data using yfinance
def download_stock_data(ticker, start_date, end_date, save_csv=True):
    """
    Downloads historical stock data for a given ticker and date range.
    
    Args:
        ticker (str): Stock ticker symbol (e.g. 'AAPL')
        start_date (str): Start date in format 'YYYY-MM-DD'
        end_date (str): End date in format 'YYYY-MM-DD'
        save_csv (bool): If True, saves data to data/raw/{ticker}.csv

    Returns:
        pd.DataFrame: Historical OHLCV stock data
    """
    print(f"Downloading {ticker} from {start_date} to {end_date}...")

    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        print(f"[!] No data found for {ticker}.")
        return None

    df.reset_index(inplace=True)

    if save_csv:
        output_path = os.path.join("data", "raw", f"{ticker}.csv")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.sort_values("Date", inplace=True)
        df.to_csv(output_path, index=False)
        print(f"[✓] Data saved to {output_path}")

    return df