import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Fetch stock data
ticker = "AAPL"  # Change this to any stock symbol
stock = yf.Ticker(ticker)
data = stock.history(period="1y")  # Fetch past 1 year of data

# Step 2: Calculate moving averages
data["50-day MA"] = data["Close"].rolling(window=50).mean()
data["200-day MA"] = data["Close"].rolling(window=200).mean()

# Step 3: Plot stock price and moving averages
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label="Stock Price", color="blue")
plt.plot(data.index, data["50-day MA"], label="50-Day MA", color="orange")
plt.plot(data.index, data["200-day MA"], label="200-Day MA", color="red")

plt.title(f"{ticker} Stock Price & Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid()

# Show the plot
plt.show()
