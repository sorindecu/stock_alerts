import streamlit as st
import pandas as pd
from stock_predictor_app import analyze_stock, get_stock_data, create_features
import requests
import yfinance as yf

st.set_page_config(page_title="Stock Forecast Dashboard", layout="centered")
st.title("📈 Stock Forecast Dashboard")
st.markdown(
    "**Disclaimer:** This dashboard is for informational purposes only and does not constitute financial advice."
)

def fetch_news(ticker):
    url = f"https://finviz.com/quote.ashx?t={ticker}"
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        news = pd.read_html(response.text)
        headlines = news[5][[1, 2]].dropna().head(5)
        return headlines
    except Exception as e:
        return f"Failed to fetch news: {e}"

def fetch_earnings_date(ticker):
    try:
        stock = yf.Ticker(ticker)
        cal = stock.calendar
        if not cal.empty:
            earnings = cal.loc['Earnings Date'].values[0]
            return pd.to_datetime(earnings)
        return "No upcoming earnings found."
    except Exception as e:
        return f"Error fetching earnings: {e}"

ticker = st.text_input("Enter Stock Ticker", value="AAPL")
target_price = st.number_input("Set target sell price ($)", min_value=0.0, value=200.0, step=1.0)

if st.button("Analyze"):
    with st.spinner("Fetching and analyzing stock data..."):
        try:
            df = get_stock_data(ticker)
            df = create_features(df)
            prob, verdict, accuracy = analyze_stock(ticker)

            st.success(f"**Verdict**: {verdict}")
            st.metric(label="Probability of Increase", value=f"{prob:.2%}")
            st.metric(label="Cross-Val Accuracy", value=f"{accuracy:.2%}")

            st.subheader(f"Price Chart for {ticker}")
            st.line_chart(df['Adj Close'])

            st.subheader("Technical Indicators")
            st.write(df[['SMA_20', 'SMA_50', 'Momentum', 'Volatility',
                         'BB_upper', 'BB_lower', 'RSI_14']].tail(1))

            st.subheader("MACD Indicator")
            st.line_chart(df[['MACD', 'Signal']].dropna())

            st.subheader("Earnings Date")
            earnings_date = fetch_earnings_date(ticker)
            st.write(earnings_date)

            st.subheader("Latest News Headlines")
            news = fetch_news(ticker)
            st.write(news)

            if df['Adj Close'].iloc[-1] >= target_price:
                st.warning(f"📢 Target price of ${target_price:.2f} reached!")

        except Exception as e:
            st.error(f"Error: {e}")

        st.markdown(
            "**Reminder:** Past performance does not guarantee future results."
        )
