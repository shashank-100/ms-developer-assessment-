# MSCapital - Market Liquidity Dashboard & Cash Allocation Tool

A comprehensive tool for monitoring market liquidity and guiding cash allocation in Indian equity portfolios. This dashboard provides insights into market conditions and helps investors make informed decisions about their cash positions.

## Features

### 1. Market Indicators
- Nifty 50 index tracking (Real-time data)
- India VIX (volatility index) monitoring (Real-time data)
- FII/DII flow analysis (Synthetic data for demonstration)
- Nifty Midcap 100 tracking (Real-time data)

### 2. Interactive Dashboard
- Interactive time series plots
- Customizable date ranges (up to 3 years)
- Real-time metric updates
- Risk tolerance settings (Low/Medium/High)

### 3. Cash Allocation Model
- Smart scoring system based on:
  - Market Volatility (VIX)
  - Institutional Flows (FII/DII)
  - Midcap Market Momentum (Nifty Midcap 100)
- Risk-adjusted recommendations (0-30% cash)
- Component-wise scoring breakdown

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/shashank-100/ms-developer-assessment-
cd mscapital
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

The app will open in your default web browser at http://localhost:8501

## How It Works

### 1. Market Data Collection
- **Real Data**:
  - Nifty 50 data from Yahoo Finance (^NSEI)
  - India VIX data from Yahoo Finance (INDIAVIX.NS)
  - Nifty Midcap 100 data from Yahoo Finance (NIFTYMIDCAP100.NS)
- **Synthetic Data** (for demonstration):
  - FII/DII data: Simulated institutional flows

### 2. Data Sources
- **Market Indices**:
  - Yahoo Finance provides historical data for major indices
  - Data includes OHLCV (Open, High, Low, Close, Volume)
  - Daily data available for analysis
- **FII/DII Data**:
  - Historical institutional flow data
  - Tracks foreign and domestic institutional activity
  - Used to gauge market sentiment

### 3. Cash Allocation Logic
The model recommends cash allocation (0-30%) based on:

1. **Market Volatility (VIX)**
   - Higher VIX = More cash recommended
   - Measures market fear/uncertainty

2. **Institutional Flows (FII/DII)**
   - Negative flows = More cash recommended
   - Tracks foreign and domestic institutional activity

3. **Midcap Market Momentum (Nifty Midcap 100)**
   - Negative price momentum = More cash recommended
   - Measures broader market health through midcap performance
   - Uses 20-day price momentum to gauge market sentiment

### 4. Risk Tolerance Levels
- **Low Risk**: More weight to VIX (40%)
- **Medium Risk**: Balanced weights (33% each)
- **High Risk**: More weight to FII/DII (40%)

