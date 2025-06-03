# src/data/download_data.py
from dotenv import load_dotenv
from polygon import RESTClient
import pandas as pd
import os

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
if not POLYGON_API_KEY:
    raise ValueError("[!] POLYGON_API_KEY not set in environment variables.")

def download_stock_data(ticker, start_date, end_date, save_csv=True):
    print(f"📥 Downloading {ticker} from Polygon.io...")

    try:
        client = RESTClient(api_key=POLYGON_API_KEY)
        bars = client.get_aggs(ticker, 1, "day", start_date, end_date)

        if not bars:
            print(f"[!] No data returned for {ticker}.")
            return None

        # # df = pd.DataFrame([bar._asdict() for bar in bars])
        # df = pd.DataFrame([vars(bar) for bar in bars])
        # df['t'] = pd.to_datetime(df['t'], unit='ms')
        # df.rename(columns={'t': 'Date'}, inplace=True)

        # Check actual keys returned by the Agg object
        data = []
        for bar in bars:
            data.append({
                "Date": pd.to_datetime(bar.timestamp, unit='ms'),
                "Open": bar.open,
                "High": bar.high,
                "Low": bar.low,
                "Close": bar.close,
                "Volume": bar.volume
            })

        df = pd.DataFrame(data)

        if save_csv:
            output_path = os.path.join("data", "raw", f"{ticker}.csv")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=False)
            print(f"[✓] Saved to {output_path}")

        return df

    except Exception as e:
        print(f"[!] Polygon API error: {e}")
        return None
    