# Example code sketch (Python) to download data:
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import os
import numpy as np

def download_market_data():
    # Create data directory if it doesn't exist
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Set date range for 3 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)
    
    # Format dates for yfinance
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")
    
    print("Downloading market data...")
    
    # 1. Download Nifty 50 data
    print('Downloading Nifty 50...')
    try:
        nifty50 = yf.download("^NSEI", start=start_str, end=end_str, progress=False)
        if not nifty50.empty:
            nifty50.to_csv(os.path.join(data_dir, "nifty50.csv"))
            print("Nifty 50 data saved successfully")
        else:
            print("No Nifty 50 data found")
    except Exception as e:
        print(f"Error downloading Nifty 50: {e}")

    # 2. Download Nifty Midcap 100 data
    print('Downloading Nifty Midcap 100...')
    try:
        midcap100 = yf.download("NIFTY_MIDCAP_100.NS", start=start_str, end=end_str, progress=False)
        if not midcap100.empty:
            midcap100.to_csv(os.path.join(data_dir, "nifty_midcap100.csv"))
            print("Nifty Midcap 100 data saved successfully")
        else:
            print("No Nifty Midcap 100 data found")
    except Exception as e:
        print(f"Error downloading Nifty Midcap 100: {e}")

    # 3. Download India VIX data using yfinance
    print('Downloading India VIX...')
    try:
        # Try multiple symbols for India VIX
        vix_symbols = ["^NSEVIX", "INDIAVIX.NS", "INDIA VIX"]
        vix_data = None
        
        for symbol in vix_symbols:
            try:
                vix_data = yf.download(symbol, start=start_str, end=end_str, progress=False)
                if not vix_data.empty:
                    break
            except:
                continue
        
        if vix_data is not None and not vix_data.empty:
            vix_data.to_csv(os.path.join(data_dir, "india_vix.csv"))
            print("India VIX data saved successfully")
        else:
            print("No India VIX data found")
    except Exception as e:
        print(f"Error downloading India VIX: {e}")

    # 4. Generate synthetic FII/DII flows data
    print('Generating FII/DII flows data...')
    try:
        date_range = pd.date_range(start=start_str, end=end_str, freq='D')
        np.random.seed(42)  # For reproducibility
        
        fii_dii_data = pd.DataFrame({
            'Date': date_range,
            'FII': np.random.normal(1000, 500, len(date_range)),  # Mean 1000 Cr, SD 500 Cr
            'DII': np.random.normal(800, 400, len(date_range))    # Mean 800 Cr, SD 400 Cr
        })
        fii_dii_data.set_index('Date', inplace=True)
        fii_dii_data.to_csv(os.path.join(data_dir, "fii_dii_flows.csv"))
        print("FII/DII flows data generated successfully")
    except Exception as e:
        print(f"Error generating FII/DII flows data: {e}")

    # 5. Download AMFI mutual fund data
    print('Downloading AMFI mutual fund data...')
    try:
        amfi_url = "https://www.amfiindia.com/spages/NAVAll.txt"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
        }
        response = requests.get(amfi_url, headers=headers)
        if response.status_code == 200:
            with open(os.path.join(data_dir, "amfi_navall.txt"), "w", encoding="utf-8") as f:
                f.write(response.text)
            print("AMFI data saved successfully")
        else:
            print(f"Failed to download AMFI data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading AMFI data: {e}")

if __name__ == "__main__":
    download_market_data()
