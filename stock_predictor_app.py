import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import datetime
import smtplib
from email.message import EmailMessage
import os

LOOKBACK_DAYS = 180
FUTURE_DAYS = 30
MIN_PROBABILITY_TO_BUY = 0.7

ALERT_TARGETS = {
    'AAPL': 200.00,
    'NVDA': 1200.00,
    'MSFT': 450.00
}

EMAIL_SENDER = os.environ.get('ALERT_EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('ALERT_EMAIL_PASSWORD')
EMAIL_RECIPIENT = os.environ.get('ALERT_EMAIL_RECIPIENT')

def send_email_alert(subject, body):
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECIPIENT:
        print("Missing email credentials or recipient")
        return

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email alert sent.")
    except Exception as e:
        print(f"Error sending email: {e}")


def get_stock_data(ticker):
    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=LOOKBACK_DAYS + FUTURE_DAYS)

    try:
        # NEW: auto_adjust=True ensures adjusted close is returned as 'Close'
        data = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)

        if data is None or data.empty:
            raise ValueError(f"No data returned for ticker: {ticker}")

        # Now use the adjusted 'Close' directly as 'Adj Close'
        data['Adj Close'] = data['Close']

        data.dropna(inplace=True)
        return data

    except Exception as e:
        raise ValueError(f"Error fetching data for ticker '{ticker}': {e}")



def create_features(df):
    df['Return'] = df['Adj Close'].pct_change()
    df['Volatility'] = df['Return'].rolling(window=5).std()
    df['Momentum'] = df['Adj Close'] - df['Adj Close'].shift(5)
    df['SMA_20'] = df['Adj Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Adj Close'].rolling(window=50).mean()
    
    # MACD
    df['EMA_12'] = df['Adj Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Adj Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    df['Target'] = df['Adj Close'].shift(-FUTURE_DAYS) > df['Adj Close']
    df.dropna(inplace=True)
    return df




def train_model(df):
    features = ['Return', 'Volatility', 'Momentum', 'SMA_20', 'SMA_50']
    X = df[features]
    y = df['Target'].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    prob = model.predict_proba([X.iloc[-1]])[0][1]
    return model, prob, accuracy_score(y_test, model.predict(X_test))

def analyze_stock(ticker):
    df = get_stock_data(ticker)
    df = create_features(df)
    model, probability, accuracy = train_model(df)

    current_price = df['Adj Close'].iloc[-1]
    target_price = ALERT_TARGETS.get(ticker.upper())

    verdict = "BUY" if probability > MIN_PROBABILITY_TO_BUY else "HOLD or WAIT"
    print(f"\nStock: {ticker.upper()}")
    print(f"Current Price: ${current_price:.2f}")
    print(f"Model Accuracy: {accuracy:.2f}")
    print(f"Probability of price increase over {FUTURE_DAYS} days: {probability:.2f}")
    print(f"Recommendation: {verdict}")

    if target_price and current_price >= target_price:
        subject = f"Sell Alert: {ticker} has hit ${current_price:.2f}"
        body = f"{ticker.upper()} has reached the target price of ${target_price:.2f}. Current price is ${current_price:.2f}. Consider selling."
        send_email_alert(subject, body)

    return probability, verdict

if __name__ == '__main__':
    ticker_input = input("Enter stock ticker (e.g. AAPL): ").upper()
    analyze_stock(ticker_input)

