# MSCapital - Market Liquidity Dashboard & Cash Allocation Tool

A comprehensive tool for monitoring market liquidity and guiding cash allocation in Indian equity portfolios. This dashboard provides insights into market conditions and helps investors make informed decisions about their cash positions.

## Features

### 1. Market Indicators
- Nifty 50 index tracking (Real-time data)
- India VIX (volatility index) monitoring (Real-time data)
- FII/DII flow analysis (Synthetic data for demonstration)
- Market breadth indicators (Synthetic data for demonstration)

### 2. Interactive Dashboard
- Interactive time series plots
- Customizable date ranges (up to 3 years)
- Real-time metric updates
- Risk tolerance settings (Low/Medium/High)

### 3. Cash Allocation Model
- Smart scoring system based on:
  - Market Volatility (VIX)
  - Institutional Flows (FII/DII)
  - Market Breadth
- Risk-adjusted recommendations (0-30% cash)
- Component-wise scoring breakdown

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/shashank-100/ms-developer-assessment-
cd mscapital
```

2. Install dependencies using uv:
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
- **Synthetic Data** (for demonstration):
  - FII/DII data: Simulated institutional flows
  - Market breadth data: Simulated advance-decline ratios

### 2. Why Synthetic Data?
- **FII/DII Data**:
  - Real data requires NSE membership and API access
  - Not available through public APIs
  - Synthetic data demonstrates the model's logic
- **Market Breadth**:
  - Real calculation needs data for all NSE stocks
  - Requires significant infrastructure
  - Synthetic data shows the concept

### 3. Cash Allocation Logic
The model recommends cash allocation (0-30%) based on:

1. **Market Volatility (VIX)**
   - Higher VIX = More cash recommended
   - Measures market fear/uncertainty

2. **Institutional Flows (FII/DII)**
   - Negative flows = More cash recommended
   - Tracks foreign and domestic institutional activity

3. **Market Breadth**
   - Poor breadth = More cash recommended
   - Measures overall market health

### 4. Risk Tolerance Levels
- **Low Risk**: More weight to VIX (40%)
- **Medium Risk**: Balanced weights (33% each)
- **High Risk**: More weight to FII/DII (40%)

## Project Structure

```
mscapital/
├── src/
│   ├── data/
│   │   └── data_collector.py    # Data fetching and processing
│   ├── visualization/
│   │   └── plotter.py          # Chart creation
│   └── models/
│       └── cash_allocation.py  # Cash allocation logic
├── app.py                      # Main Streamlit application
└── requirements.txt            # Project dependencies
```

## Data Sources

- **Real-Time Data**:
  - Nifty 50: Yahoo Finance (^NSEI)
  - India VIX: Yahoo Finance (INDIAVIX.NS)
- **Synthetic Data** (for demonstration):
  - FII/DII: Simulated institutional flows
  - Market Breadth: Simulated advance-decline ratios

## Future Improvements

- Integrate real FII/DII data with NSE API access
- Implement real market breadth calculation
- Add more market indicators
- Enhance visualization options

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
