📈 Stock Forecast & Alert System
A Python-based stock analysis tool that combines technical indicators with machine learning to forecast short-term price movements and trigger automated email alerts when target prices are reached.
What It Does

ML-Powered Forecasting: Uses logistic regression trained on historical price data to estimate the probability of a stock's price increasing over the next 30 days
Technical Analysis: Calculates SMA (20/50-day), MACD, momentum, and volatility indicators
Price Alerts: Sends automated email notifications when a stock hits a user-defined target price
Interactive Dashboard: Streamlit-based UI for exploring forecasts, charts, technical indicators, earnings dates, and latest news headlines

Tech Stack

Python — core language
scikit-learn — logistic regression model for price movement prediction
yfinance — historical stock data retrieval
pandas / numpy — data processing and feature engineering
Streamlit — interactive web dashboard
smtplib — automated email alerts
Finviz — news headline scraping

Project Structure
stock_predictor_app.py   → Core engine: data fetching, feature engineering, ML model, alerts
dashboard.py             → Streamlit dashboard for interactive analysis
Setup
bash# Clone the repo
git clone https://github.com/sorindecu/stock_alerts.git
cd stock_alerts

# Install dependencies
pip install -r requirements.txt

# (Optional) Set up email alerts
export ALERT_EMAIL_SENDER="your_email@gmail.com"
export ALERT_EMAIL_PASSWORD="your_app_password"
export ALERT_EMAIL_RECIPIENT="recipient@email.com"
Usage
Command Line
bashpython stock_predictor_app.py
# Enter a ticker when prompted (e.g., AAPL)
Example output:
Stock: AAPL
Current Price: $232.15
Model Accuracy: 0.78
Probability of price increase over 30 days: 0.73
Recommendation: BUY
Streamlit Dashboard
bashstreamlit run dashboard.py
Opens an interactive dashboard where you can:

Enter any stock ticker
Set a custom target sell price
View price charts, MACD, and technical indicators
Check upcoming earnings dates
Read latest news headlines

How the Model Works

Pulls 210 days of historical price data via yfinance
Engineers features: daily returns, 5-day volatility, momentum, SMA crossovers, MACD
Trains a logistic regression model to predict whether price will be higher in 30 days
Outputs a probability score — above 70% triggers a BUY recommendation

Disclaimer
This is a personal learning project and is not financial advice. The model uses basic logistic regression on a limited feature set and should not be used for actual trading decisions. Always do your own research.
License
MIT
