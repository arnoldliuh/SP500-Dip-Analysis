# S&P 500 Stock Dip Analysis

## Overview
This Python program retrieves S&P 500 stock data and identifies stocks that have dropped below their all-time high by a user-designated percentage. The program fetches real-time stock data using the public Yahoo Finance API, extracts tickers from Wikipedia using BeautifulSoup, and finally visualizes the results with Matplotlib.

## Features
- Fetches S&P 500 tickers from Wikipedia.
- Retrieves historical stock data using Yahoo Finance
- Calculates ATH stock prices and compares it to the current price.
- Filters stocks that have dropped by a user-designated percentage.
- Runs parallelized requests for faster execution with such a large dataset.
- Provides visualization using a horizontal bar chart.

## Technologies Used
- Python (Data processing and logic)
- yfinance (Stock data retrieval)
- pandas (Data manipulation)
- requests & BeautifulSoup (Web scraping S&P 500 tickers)
- ThreadPoolExecutor (Parallel processing for efficiency)
- **Matplotlib** (Data visualization)

## Installation
Ensure you have Python installed (version 3.6+ recommended). Then, install the required dependencies:
pip install yfinance pandas requests beautifulsoup4 matplotlib

## Usage
1. Run the script:
   python sp500_dip_analysis.py
   
2. Enter the percentage drop from ATH to filter stocks (For example, "20" for 20%).
3. Choose a time range for ATH calculation from the following options:
   - `1D` (1 Day)
   - `5D` (5 Days)
   - `1M` (1 Month)
   - `6M` (6 Months)
   - `YTD` (Year-to-Date)
   - `1Y` (1 Year)
   - `5Y` (5 Years)
   - `All` (All Time)
4. After a few moments, the program will display a bar chart of stocks that meet the chosen criteria.

## Example Output
```
Enter the percentage drop from ATH to filter stocks (e.g., 20 for 20%): 15
Select a time range for ATH calculation:
1. 1D (1 Day)
2. 5D (5 Days)
3. 1M (1 Month)
4. 6M (6 Months)
5. YTD (Year-to-Date)
6. 1Y (1 Year)
7. 5Y (5 Years)
8. All (All Time)
Enter the number corresponding to your choice: 6
Thank you, please wait a moment as I look for stocks that have dipped > 15% in the last 1Y!
```
A bar chart will appear showing stocks that match the criteria.

## Notes
- If no stocks meet the criteria, the program will notify the user.
- **Yahoo Finance** replaces `.` with `-` in tickers, which is handled automatically.
- If Yahoo Finance lacks data for a stock, it is skipped.


---
### Author
Developed by [Arnold Liu](https://github.com/arnoldliuh)

