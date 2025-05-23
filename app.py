import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src directory to path
sys.path.append(os.path.abspath("src"))

from data.data_collector import DataCollector
from visualization.plotter import Plotter
from models.cash_allocation import CashAllocationModel, RiskTolerance

# Set page config
st.set_page_config(
    page_title="MSCapital - Liquidity Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary: #4FC3F7;
        --background: #0E1117;
        --card-bg: rgba(255, 255, 255, 0.05);
        --text-color: #ffffff;
        --hover-color: #4FC3F7;
    }
    .stApp {
        background: var(--background);
        color: var(--text-color);
        font-family: 'Segoe UI', sans-serif;
    }
    .metric-card {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3 {
        color: var(--hover-color) !important;
        margin-bottom: 1rem !important;
    }
    .divider {
        height: 2px;
        background: linear-gradient(90deg, var(--hover-color) 0%, transparent 100%);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
try:
    data_collector = DataCollector()
    plotter = Plotter()
    cash_model = CashAllocationModel()
except Exception as e:
    st.error(f"Error initializing components: {str(e)}")
    st.stop()

# Sidebar
st.sidebar.title("📈 MSCapital")
st.sidebar.markdown("---")

# Date range selection
st.sidebar.subheader("Date Range")
end_date = datetime.now()
start_date = end_date - timedelta(days=3*365)  # 3 years default

selected_start = st.sidebar.date_input(
    "Start Date",
    value=start_date,
    max_value=end_date
)

selected_end = st.sidebar.date_input(
    "End Date",
    value=end_date,
    max_value=end_date
)

# Validate date range
if selected_start >= selected_end:
    st.error("Start date must be before end date")
    st.stop()

# Risk tolerance selection
st.sidebar.markdown("---")
st.sidebar.subheader("Risk Tolerance")
risk_tolerance = st.sidebar.selectbox(
    "Select Risk Tolerance",
    [RiskTolerance.LOW, RiskTolerance.MEDIUM, RiskTolerance.HIGH],
    format_func=lambda x: x.value.capitalize()
)

# Main content
st.title("Market Liquidity Dashboard & Cash Allocation Tool")

# Fetch data
try:
    with st.spinner("Loading market data from CSV files..."):
        logger.info("Loading Nifty data...")
        nifty_data = pd.read_csv(os.path.join("data", "nifty50.csv"), skiprows=2)
        nifty_data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
        nifty_data['Date'] = pd.to_datetime(nifty_data['Date'])
        logger.info(f"Nifty data shape: {nifty_data.shape if not nifty_data.empty else 'Empty'}")
        
        logger.info("Loading VIX data...")
        vix_data = pd.read_csv(os.path.join("data", "india_vix_historical.csv"))
        vix_data.columns = ['Date', 'Close']  # VIX data only has Date and Close columns
        vix_data['Date'] = pd.to_datetime(vix_data['Date'])
        logger.info(f"VIX data shape: {vix_data.shape if not vix_data.empty else 'Empty'}")
        
        logger.info("Loading FII/DII data...")
        fii_dii_data = pd.read_csv(os.path.join("data", "fii_dii_flows.csv"))
        fii_dii_data['Date'] = pd.to_datetime(fii_dii_data['Date'])
        logger.info(f"FII/DII data shape: {fii_dii_data.shape if not fii_dii_data.empty else 'Empty'}")
        
        logger.info("Loading market breadth data...")
        breadth_data = pd.read_csv(os.path.join("data", "nifty_midcap100.csv"), skiprows=2)
        breadth_data.columns = ['Date', 'Close', 'High', 'Low', 'Open', 'Volume']
        breadth_data['Date'] = pd.to_datetime(breadth_data['Date'])
        logger.info(f"Market breadth data shape: {breadth_data.shape if not breadth_data.empty else 'Empty'}")
        
        # Check if any data is empty
        if nifty_data.empty:
            st.error("Failed to load Nifty data. Please check your data file.")
        if vix_data.empty:
            st.error("Failed to load VIX data. Please check your data file.")
        if fii_dii_data.empty:
            st.error("Failed to load FII/DII data. Please check your data file.")
        if breadth_data.empty:
            st.error("Failed to load market breadth data. Please check your data file.")
            
except Exception as e:
    logger.error(f"Error loading market data: {str(e)}")
    st.error(f"Error loading market data: {str(e)}")
    st.error("Please check if your data files are properly configured and accessible.")
    st.stop()

# Display key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    if not nifty_data.empty:
        try:
            last_price = float(nifty_data['Close'].iloc[-1])
            price_change = float(nifty_data['Close'].pct_change().iloc[-1] * 100)
            st.metric(
                "Nifty 50",
                f"₹{last_price:,.2f}",
                f"{price_change:.2f}%"
            )
        except Exception as e:
            st.error(f"Error displaying Nifty metrics: {str(e)}")
            st.metric("Nifty 50", "Error", "Error")
    else:
        st.metric("Nifty 50", "N/A", "N/A")

with col2:
    if not vix_data.empty:
        try:
            last_vix = float(vix_data['Close'].iloc[-1])
            vix_change = float(vix_data['Close'].pct_change().iloc[-1] * 100)
            st.metric(
                "India VIX",
                f"{last_vix:.2f}",
                f"{vix_change:.2f}%"
            )
        except Exception as e:
            st.error(f"Error displaying VIX metrics: {str(e)}")
            st.metric("India VIX", "Error", "Error")
    else:
        st.metric("India VIX", "N/A", "N/A")

with col3:
    if not fii_dii_data.empty:
        try:
            fii_sum = float(fii_dii_data['FII'].iloc[-30:].sum())
            fii_mean = float(fii_dii_data['FII'].iloc[-30:].mean())
            st.metric(
                "FII Flow (30d)",
                f"₹{fii_sum:,.2f} Cr",
                f"{fii_mean:,.2f} Cr/day"
            )
        except Exception as e:
            st.error(f"Error displaying FII metrics: {str(e)}")
            st.metric("FII Flow (30d)", "Error", "Error")
    else:
        st.metric("FII Flow (30d)", "N/A", "N/A")

with col4:
    if not breadth_data.empty:
        try:
            last_breadth = float(breadth_data['Close'].iloc[-1])
            breadth_diff = float(breadth_data['Close'].pct_change().iloc[-1] * 100)
            st.metric(
                "Nifty Midcap 100",
                f"₹{last_breadth:,.2f}",
                f"{breadth_diff:.2f}%"
            )
        except Exception as e:
            st.error(f"Error displaying market breadth metrics: {str(e)}")
            st.metric("Nifty Midcap 100", "Error", "Error")
    else:
        st.metric("Nifty Midcap 100", "N/A", "N/A")

# Create plots
st.markdown("---")
st.subheader("Market Indicators")

# Volatility plot
if not vix_data.empty and not nifty_data.empty:
    volatility_fig = plotter.create_volatility_plot(vix_data, nifty_data)
    st.plotly_chart(volatility_fig, use_container_width=True)
else:
    st.warning("Unable to display volatility plot due to missing data")

# FII/DII plot
if not fii_dii_data.empty:
    fii_dii_fig = plotter.create_fii_dii_plot(fii_dii_data)
    st.plotly_chart(fii_dii_fig, use_container_width=True)
else:
    st.warning("Unable to display FII/DII plot due to missing data")

# Market breadth plot
if not breadth_data.empty:
    breadth_fig = plotter.create_market_breadth_plot(breadth_data)
    st.plotly_chart(breadth_fig, use_container_width=True)
else:
    st.warning("Unable to display market breadth plot due to missing data")

# Cash Allocation Section
st.markdown("---")
st.subheader("Cash Allocation Recommendation")

if not any([vix_data.empty, fii_dii_data.empty, breadth_data.empty]):
    try:
        # Calculate cash allocation
        allocation = cash_model.calculate_cash_allocation(
            vix_data,
            fii_dii_data,
            breadth_data,
            risk_tolerance
        )
        
        # Display recommendation
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Recommended Cash Allocation")
            st.markdown(f"**{allocation['cash_allocation']}%** of portfolio")
            st.markdown(cash_model.get_allocation_recommendation(allocation['cash_allocation']))
        
        with col2:
            st.markdown("### Component Scores")
            st.markdown(f"VIX Score: {allocation['vix_score']}%")
            st.markdown(f"FII/DII Score: {allocation['fii_dii_score']}%")
            st.markdown(f"Market Breadth Score: {allocation['breadth_score']}%")
            st.markdown(f"Risk Tolerance: {allocation['risk_tolerance'].capitalize()}")
    except Exception as e:
        st.error(f"Error calculating cash allocation: {str(e)}")
else:
    st.warning("Unable to generate cash allocation recommendation due to missing data.")