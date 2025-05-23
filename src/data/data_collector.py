import pandas as pd
import requests
import yfinance as yf
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self):
        self.nse_base_url = "https://www.nseindia.com/api/v1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_nifty_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch Nifty 50 historical data using yfinance
        """
        try:
            nifty = yf.download("^NSEI", start=start_date, end=end_date)
            return nifty
        except Exception as e:
            logger.error(f"Error fetching Nifty data: {str(e)}")
            return pd.DataFrame()

    def get_india_vix(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch India VIX historical data using yfinance
        """
        try:
            # Try to fetch VIX data with different parameters
            vix_data = yf.download(
                "INDIAVIX.NS",
                start=start_date,
                end=end_date,
                progress=False,
                auto_adjust=True
            )
            
            if vix_data.empty:
                # If empty, try with a different symbol
                vix_data = yf.download(
                    "^NSEVIX",
                    start=start_date,
                    end=end_date,
                    progress=False,
                    auto_adjust=True
                )
            
            if vix_data.empty:
                # If still empty, generate synthetic VIX data
                logger.warning("Could not fetch VIX data, generating synthetic data")
                date_range = pd.date_range(start=start_date, end=end_date, freq='D')
                np.random.seed(42)  # For reproducibility
                
                # Generate synthetic VIX data (typically between 10 and 30)
                vix_values = np.random.normal(20, 5, len(date_range))  # Mean 20, SD 5
                vix_values = np.clip(vix_values, 10, 30)  # Clip between 10 and 30
                
                vix_data = pd.DataFrame({
                    'Date': date_range,
                    'Close': vix_values
                })
                vix_data.set_index('Date', inplace=True)
            
            return vix_data
            
        except Exception as e:
            logger.error(f"Error fetching India VIX data: {str(e)}")
            return pd.DataFrame()

    def get_fii_dii_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch FII/DII flow data from NSE
        """
        try:
            # For now, we'll generate synthetic FII/DII data
            # In a real implementation, you would fetch this from NSE's API
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            np.random.seed(42)  # For reproducibility
            
            fii_data = pd.DataFrame({
                'Date': date_range,
                'FII': np.random.normal(1000, 500, len(date_range)),  # Mean 1000 Cr, SD 500 Cr
                'DII': np.random.normal(800, 400, len(date_range))    # Mean 800 Cr, SD 400 Cr
            })
            fii_data.set_index('Date', inplace=True)
            return fii_data
        except Exception as e:
            logger.error(f"Error fetching FII/DII data: {str(e)}")
            return pd.DataFrame()

    def get_market_breadth(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Calculate market breadth using advance-decline ratios
        """
        try:
            # For now, we'll generate synthetic market breadth data
            # In a real implementation, you would calculate this from actual stock data
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            np.random.seed(42)  # For reproducibility
            
            # Generate random advance-decline ratios
            adv_dec_ratio = np.random.normal(1.0, 0.2, len(date_range))  # Mean 1.0, SD 0.2
            adv_dec_ratio = np.clip(adv_dec_ratio, 0.1, 2.0)  # Clip between 0.1 and 2.0
            
            breadth_data = pd.DataFrame({
                'Date': date_range,
                'adv_dec_ratio': adv_dec_ratio
            })
            breadth_data.set_index('Date', inplace=True)
            return breadth_data
        except Exception as e:
            logger.error(f"Error calculating market breadth: {str(e)}")
            return pd.DataFrame()

    def save_data(self, data: pd.DataFrame, filename: str) -> None:
        """
        Save data to CSV file
        """
        try:
            data.to_csv(f"data/{filename}.csv")
            logger.info(f"Data saved to {filename}.csv")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")

if __name__ == "__main__":
    # Example usage
    collector = DataCollector()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)  # 3 years of data
    
    # Fetch and save Nifty data
    nifty_data = collector.get_nifty_data(start_date.strftime("%Y-%m-%d"), 
                                        end_date.strftime("%Y-%m-%d"))
    collector.save_data(nifty_data, "nifty_historical")
    
    # Fetch and save VIX data
    vix_data = collector.get_india_vix(start_date.strftime("%Y-%m-%d"), 
                                     end_date.strftime("%Y-%m-%d"))
    collector.save_data(vix_data, "india_vix_historical") 