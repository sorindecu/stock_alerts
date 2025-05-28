from stock_predictor_app import analyze_stock, ALERT_TARGETS

def run_daily_checks():
    for ticker in ALERT_TARGETS:
        try:
            print(f"Checking {ticker}...")
            analyze_stock(ticker)
        except Exception as e:
            print(f"Failed on {ticker}: {e}")

if __name__ == '__main__':
    run_daily_checks()
