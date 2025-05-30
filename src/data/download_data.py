# src/data/download_data.py

import yfinance as yf
import pandas as pd
import os
import certifi
import requests
from requests import Session

# Force proper SSL cert usage (fixes macOS curl:60 error)
os.environ["SSL_CERT_FILE"] = certifi.where()

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
    
    # Create a custom session with headers
    session = Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Apple Silicon Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
    })
    
    # For SSL verification issues
    session.verify = certifi.where()

    try:
        # Try with different parameters
        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False,
            threads=True
        )
        
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
        
    except Exception as e:
        print(f"[!] Error downloading {ticker}: {str(e)}")
        return None