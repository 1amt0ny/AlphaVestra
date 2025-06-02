# src/data/download_data.py

import yfinance as yf
import pandas as pd
import os
import certifi
import ssl
import traceback
# from requests import Session

"""
Install yfinance if not already installed: pip install yfinance==0.2.28. 
This version of yfinance doesn't include curl_cffi.
curl_cffi is what keeps hijacking the HTTP requests.
"""
# Force SSL context globally — even for urllib-based calls inside yfinance
ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

def download_stock_data(ticker: str, start_date: str, end_date: str, save_csv: bool = True) -> pd.DataFrame:
    """
    Downloads historical stock data using Ticker().history() (more robust than yf.download).

    Args:
        ticker (str): Stock symbol like 'AAPL'
        start_date (str): 'YYYY-MM-DD'
        end_date (str): 'YYYY-MM-DD'
        save_csv (bool): Save raw CSV to data/raw/

    Returns:
        pd.DataFrame or None
    """
    print(f"📥 Downloading {ticker} using Ticker().history()...")

    try:
        # Patch yfinance to use custom session with headers
        import requests
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0 Safari/537.36"
        })
        yf.shared._requests = session  # <- patch the shared session

        # Fetch data using Ticker().history()
        ticker_obj = yf.Ticker(ticker)
        df = ticker_obj.history(start=start_date, end=end_date)

        if df.empty:
            print(f"[!] No data returned for {ticker}.")
            return None

        df.reset_index(inplace=True)
        df.sort_values("Date", inplace=True)

        if save_csv:
            output_path = os.path.join("data", "raw", f"{ticker}.csv")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False)
            print(f"[✓] Data saved to {output_path}")

        return df

    except Exception as e:
        print(f"[!] Failed to fetch history for {ticker}: {e}")
        traceback.print_exc()
        return None
    
