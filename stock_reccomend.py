import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import os

TICKERS = [
    'AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'META', 'TSLA', 'BRK-B', 'UNH', 'JNJ',
    'V', 'LLY', 'PG', 'XOM', 'MA', 'HD', 'MRK', 'ABBV', 'AVGO', 'CVX',
    'PEP', 'KO', 'JPM', 'WMT', 'ADBE', 'COST', 'CRM', 'BAC', 'TMO', 'PFE',
    'INTC', 'CSCO', 'ORCL', 'DIS', 'MCD', 'NKE', 'TXN', 'LIN', 'ACN', 'WFC',
    'ABT', 'AMGN', 'AMD', 'DHR', 'QCOM', 'NEE', 'UPS', 'PM', 'MS', 'HON',
    'UNP', 'IBM', 'CAT', 'GE', 'LOW', 'RTX', 'BLK', 'SBUX', 'MDT', 'GS',
    'CI', 'ELV', 'SPGI', 'PLD', 'BA', 'CB', 'ISRG', 'INTU', 'VRTX', 'MO',
    'ADI', 'BKNG', 'ZTS', 'DE', 'REGN', 'CSX', 'MMC', 'SO', 'TGT', 'BDX',
    'LMT', 'SYK', 'ADI', 'PNC', 'AON', 'AEP', 'FISV', 'NSC', 'GM', 'NOW',
    'FDX', 'ADP', 'TFC', 'ETN', 'HUM', 'USB', 'APD', 'GILD', 'C', 'KLAC'
]
stock_data = []

for ticker in TICKERS:
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo", interval="1d")

        # Calculate daily percent change and volatility
        hist['Daily Change'] = hist['Close'].pct_change()
        volatility = hist['Daily Change'].std()

        # Get fundamentals
        info = stock.info
        pe_ratio = info.get('trailingPE', None)
        eps = info.get('trailingEps', None)

        # Simple scoring system: prefer high EPS, low P/E, high volatility
        if pe_ratio is not None and eps is not None and pe_ratio > 0:
            score = (volatility * 100) + (eps / pe_ratio)  # Simple formula
            stock_data.append({
                'Ticker': ticker,
                'Volatility': round(volatility, 4),
                'EPS': round(eps, 2),
                'P/E Ratio': round(pe_ratio, 2),
                'Score': round(score, 4)
            })

    except Exception as e:
        print(f"Error with {ticker}: {e}")

# Sort by score
df = pd.DataFrame(stock_data)
df = df.sort_values(by='Score', ascending=False)

print("\n🔍 Top Volatile Stock Recommendations:\n")
print(df[['Ticker', 'Score', 'Volatility', 'EPS', 'P/E Ratio']])

# Export to Excel
today = datetime.today().strftime('%Y-%m-%d')
filename = f'stock_recommendations_{today}.xlsx'
df.to_excel(filename, index=False)
print(f"\n✅ Exported results to {filename}")

# Auto-open the file (Windows)
os.startfile(filename)


