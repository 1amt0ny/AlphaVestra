# src/data/download_data.py

"""
Module: download_data
----------------------
Provides functionality to download historical daily stock data from Polygon.io,
convert it into a Pandas DataFrame, and optionally save it as a CSV file.

Usage:
    from src.data.download_data import download_stock_data

    df = download_stock_data("AAPL", "2023-01-01", "2023-06-01")
"""
import os
from dotenv import load_dotenv
from polygon import RESTClient
import pandas as pd

# -----------------------------------------------------------------------------
# Environment Setup
# -----------------------------------------------------------------------------

# Load environment variables from a .env file (if present)
load_dotenv()

# Fetch the Polygon API key from environment variables
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
if not POLYGON_API_KEY:
    raise ValueError("[!] POLYGON_API_KEY not set in environment variables.")

# -----------------------------------------------------------------------------
# Function: download_stock_data
# -----------------------------------------------------------------------------

def download_stock_data(ticker, start_date, end_date, save_csv=True):
    """
    Downloads historical daily stock data for a given ticker symbol from Polygon.io.

    The function retrieves OHLCV data between start_date and end_date (inclusive),
    converts it to a Pandas DataFrame, and optionally saves it as a CSV under data/raw/.

    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "TSLA").
        start_date (str): Start of date range, formatted as "YYYY-MM-DD".
        end_date (str): End of date range, formatted as "YYYY-MM-DD".
        save_csv (bool, optional): If True, saves the DataFrame to data/raw/{ticker}.csv.
                                   Defaults to True.

    Returns:
        pd.DataFrame: DataFrame containing columns ["Date", "Open", "High", "Low", "Close", "Volume"].
                      Returns None if no data is found or an error occurs.

    Raises:
        ValueError: If POLYGON_API_KEY is not set.
    """

    print(f"📥 Downloading {ticker} from Polygon.io...")

    try:
        # Initialize Polygon REST client with API key
        client = RESTClient(api_key=POLYGON_API_KEY)

        # Request 1-day aggregate bars between start_date and end_date
        bars = client.get_aggs(ticker, 1, "day", start_date, end_date)

        # If the API returns no data, inform the user and exit
        if not bars:
            print(f"[!] No data returned for {ticker}.")
            return None

        # Convert Polygon Agg objects to a list of dicts for DataFrame construction
        data = []
        for bar in bars:
            data.append({
                "Date": pd.to_datetime(bar.timestamp, unit='ms'), # Convert UNIX ms to pandas Timestamp
                "Open": bar.open,
                "High": bar.high,
                "Low": bar.low,
                "Close": bar.close,
                "Volume": bar.volume
            })

        # Create a DataFrame from the list of dicts
        df = pd.DataFrame(data)

        # If save_csv is True, write the DataFrame to data/raw/{ticker}.csv
        if save_csv:
            output_path = os.path.join("data", "raw", f"{ticker}.csv")
            os.makedirs(os.path.dirname(output_path), exist_ok=True) # Create directory if it doesn't exist
            df.to_csv(output_path, index=False)
            print(f"[✓] Saved to {output_path}")

        return df

    except Exception as e:
        # Catch and print any errors from Polygon API or data conversion
        print(f"[!] Polygon API error: {e}")
        return None
    