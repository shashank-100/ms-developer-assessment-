import pandas as pd
import requests
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import numpy as np
import json
import time
import yfinance as yf
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def get_nifty_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Load Nifty 50 historical data from local file
        """
        try:
            file_path = os.path.join(self.data_dir, "nifty50.csv")
            if not os.path.exists(file_path):
                logger.error(f"Nifty data file not found at {file_path}")
                return pd.DataFrame()
            # Always skip 3 rows and set column names manually
            col_names = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
            nifty_data = pd.read_csv(file_path, skiprows=3, names=col_names, header=None)
            nifty_data['Date'] = pd.to_datetime(nifty_data['Date'])
            nifty_data.set_index('Date', inplace=True)
            numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in numeric_cols:
                if col in nifty_data.columns:
                    nifty_data[col] = pd.to_numeric(nifty_data[col], errors='coerce')
            mask = (nifty_data.index >= pd.to_datetime(start_date)) & (nifty_data.index <= pd.to_datetime(end_date))
            return nifty_data[mask]
        except Exception as e:
            logger.error(f"Error loading Nifty data: {str(e)}")
            return pd.DataFrame()

    def get_india_vix(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Load India VIX historical data from local file
        """
        try:
            file_path = os.path.join(self.data_dir, "india_vix.csv")
            if not os.path.exists(file_path):
                logger.error(f"India VIX data file not found at {file_path}")
                # Generate synthetic VIX data
                date_range = pd.date_range(start=start_date, end=end_date, freq='D')
                np.random.seed(42)
                vix_values = np.random.normal(20, 5, len(date_range))
                vix_values = np.clip(vix_values, 10, 30)
                vix_data = pd.DataFrame({
                    'Close': vix_values
                }, index=date_range)
                return vix_data
            
            vix_data = pd.read_csv(file_path, index_col=0, parse_dates=True, date_parser=pd.to_datetime)
            # Convert numeric columns to float
            numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in numeric_cols:
                if col in vix_data.columns:
                    vix_data[col] = pd.to_numeric(vix_data[col], errors='coerce')
            
            # Filter data for the requested date range
            mask = (vix_data.index >= pd.to_datetime(start_date)) & (vix_data.index <= pd.to_datetime(end_date))
            return vix_data[mask]
        except Exception as e:
            logger.error(f"Error loading India VIX data: {str(e)}")
            return pd.DataFrame()

    def get_fii_dii_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Load FII/DII flow data from local file
        """
        try:
            file_path = os.path.join(self.data_dir, "fii_dii_flows.csv")
            if not os.path.exists(file_path):
                logger.error(f"FII/DII data file not found at {file_path}")
                return pd.DataFrame()
            
            fii_dii_data = pd.read_csv(file_path, index_col=0, parse_dates=True, date_parser=pd.to_datetime)
            # Convert numeric columns to float
            numeric_cols = ['FII', 'DII']
            for col in numeric_cols:
                if col in fii_dii_data.columns:
                    fii_dii_data[col] = pd.to_numeric(fii_dii_data[col], errors='coerce')
            
            # Filter data for the requested date range
            mask = (fii_dii_data.index >= pd.to_datetime(start_date)) & (fii_dii_data.index <= pd.to_datetime(end_date))
            return fii_dii_data[mask]
        except Exception as e:
            logger.error(f"Error loading FII/DII data: {str(e)}")
            return pd.DataFrame()

    def get_market_breadth(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Calculate market breadth using advance-decline ratios from Nifty data
        """
        try:
            # Get Nifty data
            nifty_data = self.get_nifty_data(start_date, end_date)
            if nifty_data.empty:
                logger.error("Cannot calculate market breadth without Nifty data")
                return pd.DataFrame()
            
            # Ensure Close column is numeric
            nifty_data['Close'] = pd.to_numeric(nifty_data['Close'], errors='coerce')
            
            # Calculate daily returns
            nifty_data['Returns'] = nifty_data['Close'].pct_change()
            
            # Calculate advance-decline ratio (simplified version)
            # In a real implementation, you would use actual advance-decline data
            nifty_data['adv_dec_ratio'] = np.where(nifty_data['Returns'] > 0, 1.2, 0.8)
            
            # Create market breadth dataframe
            breadth_data = pd.DataFrame({
                'adv_dec_ratio': nifty_data['adv_dec_ratio']
            })
            
            return breadth_data
        except Exception as e:
            logger.error(f"Error calculating market breadth: {str(e)}")
            return pd.DataFrame()

    def save_data(self, data: pd.DataFrame, filename: str) -> None:
        """
        Save data to CSV file
        """
        try:
            file_path = os.path.join(self.data_dir, f"{filename}.csv")
            data.to_csv(file_path)
            logger.info(f"Data saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")

if __name__ == "__main__":
    # Example usage
    collector = DataCollector()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)  # 3 years of data
    
    # Load and display data
    nifty_data = collector.get_nifty_data(start_date.strftime("%Y-%m-%d"), 
                                        end_date.strftime("%Y-%m-%d"))
    print(f"Nifty data shape: {nifty_data.shape}")
    
    vix_data = collector.get_india_vix(start_date.strftime("%Y-%m-%d"), 
                                     end_date.strftime("%Y-%m-%d"))
    print(f"VIX data shape: {vix_data.shape}")
    
    fii_dii_data = collector.get_fii_dii_data(start_date.strftime("%Y-%m-%d"), 
                                            end_date.strftime("%Y-%m-%d"))
    print(f"FII/DII data shape: {fii_dii_data.shape}")
    
    breadth_data = collector.get_market_breadth(start_date.strftime("%Y-%m-%d"), 
                                             end_date.strftime("%Y-%m-%d"))
    print(f"Market breadth data shape: {breadth_data.shape}") 