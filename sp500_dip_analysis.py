# yfiannce is used to get financial data on various tickers
# pandas is used to create a DataTable with the ticker information
# requests is used to fetch the HTML content of the Wikipedia page
# BeautifulSoup is used to extract text from the HTML content
# ThreadPoolExecutor is used to parallelize the data fetching
# matplotlib is used to create a bar graph visualizing the data 
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# Getting S&P 500 tickers from Wikipedia
def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
# finds the table on webpage containing all tickers
    table = soup.find("table")
    tickers = []
# appends each ticker to a list by finding first entry in each row
    for row in table.find_all("tr")[1:]: 
        ticker = row.find_all("td")[0].text.strip() 
        tickers.append(ticker)

    return tickers

# Fetch stock data with selected time range for calculation
def fetch_stock_data(ticker):
    yf_ticker = ticker.replace(".", "-")  # Yahoo Finance uses - instead of .
    stock = yf.Ticker(yf_ticker)
    
    # Fetch historical data based on the selected time range
    hist = stock.history(period=time_range)

    if hist.empty:
        return None  

    ath = hist["Close"].max()  # Calculate ATH within the selected time range
    current_price = hist["Close"].iloc[-1]
    drop_percentage = ((ath - current_price) / ath) * 100

    if drop_percentage >= user_percentage:
        return [ticker, current_price, ath, round(drop_percentage, 2)]
    return None

# Run requests in parallel to have program run faster
def check_sp500_dip(percentage):
    tickers = get_sp500_tickers()
    
    with ThreadPoolExecutor(max_workers=10) as executor:  # Runs 10 requests at a time
        results = list(executor.map(fetch_stock_data, tickers))
    
    df = pd.DataFrame([r for r in results if r], columns=["Ticker", "Current Price", "ATH", "% Below ATH"])
    return df.sort_values(by="% Below ATH", ascending=False)

# Visualize the results using Matplotlib
def visualize_results(df):
    if df.empty:
        print("No stocks found that match the criteria.")
        return
    
    # Create a horizontal bar chart
    plt.figure(figsize=(10, len(df) * 0.6))  
    bars = plt.barh(df["Ticker"], df["% Below ATH"], color="skyblue")
    
    # Add labels and title
    plt.xlabel("% Below ATH", fontsize=12)
    plt.ylabel("Ticker", fontsize=12)
    plt.title(f"Stocks Dipped > {user_percentage}% from ATH (Last {time_range})", fontsize=14)
    
    # Invert the y-axis to show the largest drop at the top
    plt.gca().invert_yaxis()
    
    # Add value labels to the bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height() / 2, f"{width:.2f}%", va="center", ha="left", fontsize=8)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# Get user input and run the program
try:
    user_percentage = float(input("Enter the percentage drop from ATH to filter stocks (e.g., 20 for 20%): "))
    
    # Display time range options
    print("Select a time range for ATH calculation:")
    print("1. 1D (1 Day)")
    print("2. 5D (5 Days)")
    print("3. 1M (1 Month)")
    print("4. 6M (6 Months)")
    print("5. YTD (Year-to-Date)")
    print("6. 1Y (1 Year)")
    print("7. 5Y (5 Years)")
    print("8. All (All Time)")
    
    time_range_choice = input("Enter the number corresponding to your choice: ")
    
    # Map the user's choice to dictionary
    time_range_map = {
        "1": "1d",
        "2": "5d",
        "3": "1mo",
        "4": "6mo",
        "5": "ytd",
        "6": "1y",
        "7": "5y",
        "8": "max"
    }
    
    time_range = time_range_map.get(time_range_choice, "max")  # Default to "max" if invalid choice
    
    print(f"Thank you, please wait a moment as I look for stocks that have dipped > {user_percentage}% in the last {time_range}!")
    sp500_dips = check_sp500_dip(user_percentage)

    # Visualize the results
    visualize_results(sp500_dips)

except ValueError:
    print("Invalid input. Please enter a number.")