import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Step 1: Get S&P 500 stock symbols from Wikipedia
def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"id": "constituents"})
    tickers = []
    for row in table.find_all("tr")[1:]: 
        ticker = row.find_all("td")[0].text.strip() 
        tickers.append(ticker)

    return tickers

# Step 2: Fetch stock data (now runs in parallel)
def fetch_stock_data(ticker):

    yf_ticker = ticker.replace(".", "-")  # Fix Yahoo Finance tickers
    stock = yf.Ticker(yf_ticker)
    hist = stock.history(period="max")

    if hist.empty:
        return None  

    ath = hist["Close"].max()
    current_price = hist["Close"].iloc[-1]
    drop_percentage = ((ath - current_price) / ath) * 100

    return [ticker, current_price, ath, round(drop_percentage, 2)] if drop_percentage >= user_percentage else None


# Step 3: Run requests in parallel
def check_sp500_dip(percentage):
    tickers = get_sp500_tickers()
    
    with ThreadPoolExecutor(max_workers=10) as executor:  # Runs 10 requests at a time
        results = list(executor.map(fetch_stock_data, tickers))

    df = pd.DataFrame(results, columns=["Ticker", "Current Price", "ATH", "% Below ATH"])
    return df.sort_values(by="% Below ATH", ascending=False)

# Step 4: Get user input and run the program
try:
    user_percentage = float(input("Enter the percentage drop from ATH to filter stocks (e.g., 20 for 20%): "))
    print("Thank you, please wait a moment as I look for stocks that have dipped > " + str(user_percentage) + "%!" )
    sp500_dips = check_sp500_dip(user_percentage)

    if sp500_dips.empty:
        print("No stocks found that match the criteria.")
    else:
        print(sp500_dips)
except ValueError:
    print("Invalid input. Please enter a number.")
