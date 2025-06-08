# Stock Alerts Dashboard

This repository contains a simple stock analysis dashboard built with Streamlit. It uses `yfinance` to download historical prices, computes several technical indicators, and provides a basic logistic regression model to suggest buy, sell, or hold decisions with an estimated probability.

## Setup

1. Install Python 3.8+ and virtual environment tools.
2. Install the required dependencies:
   ```bash
   ./setup.sh
   ```
   This script installs packages listed in `requirements.txt`.

## Running the Dashboard

Start the Streamlit app:

```bash
streamlit run stock_dashboard.py
```

## Running Scheduled Checks

To run the scheduled daily stock checks in the console:

```bash
python stock_scheduler.py
```

## Notes

- Historical data and model predictions are for informational purposes only and are **not** financial advice.
- If you run into missing packages, ensure you've executed `setup.sh` or installed dependencies manually.
