from datetime import datetime


def get_financial_tasks(assets: str) -> list[str]:
    date_str = datetime.now().strftime("%Y-%m-%d")
    ticker_list = ", ".join(f'"{t.strip()}"' for t in assets.split(","))

    financial_task = f"""Today is {date_str}.
Fetch REAL stock data for the following tickers using yfinance: {assets}

You MUST use the yfinance library. Do NOT generate random or synthetic data under any circumstances.

Follow these steps in order:

STEP 1 — Fetch 6-month historical closing prices and compute % change:
Use yf.download with period='6mo' and auto_adjust=True. Drop rows where all values are NaN.
Compute 6-month % change as: ((last_price - first_price) / first_price) * 100
Print the result for each ticker.

STEP 2 — Fetch fundamental ratios using yf.Ticker(ticker).info for each ticker:
Retrieve and print: longName, currentPrice, trailingPE, forwardPE, dividendYield,
priceToBook, debtToEquity, returnOnEquity.
If a value is None, print None (do not fabricate values).

STEP 3 — Save the normalized price chart:
Normalize prices to base 100 at the start date: normalized = (data / data.iloc[0]) * 100
Plot all tickers on one figure, label axes, add legend and grid.
Save the figure to 'normalized_prices.png' using fig.savefig('normalized_prices.png').
Print "Figure saved as normalized_prices.png" after saving.
Use matplotlib.use('Agg') before importing pyplot to avoid display errors.

Execute and verify each step. Confirm the figure file was saved.
Reply TERMINATE when everything is done."""

    research_task = f"""Retrieve recent market news headlines for these stocks: {assets}
Use the full company name (e.g. "Alphabet Inc" not "GOOGL") for each search.

Use Google News RSS feed — no API key needed:
Construct the URL as: https://news.google.com/rss/search?q=COMPANY_NAME+stock&hl=en-US&gl=US&ceid=US:en
Use requests.get() with a timeout, parse with BeautifulSoup using the 'xml' feature.
Find all 'item' tags and extract the text of each 'title' tag.
Retrieve at least 10 headlines per stock.

IMPORTANT — encoding: When printing headlines, always sanitize output using:
    safe = headline.encode('ascii', errors='replace').decode('ascii')
    print(f"- {{safe}}")
This prevents UnicodeEncodeError on Windows terminals.

Print each company's headlines clearly labeled. Do not perform sentiment analysis.
Reply TERMINATE when everything is done."""

    return [financial_task, research_task]


writing_tasks = [
    """Write a comprehensive financial report in markdown based on ALL data provided in this conversation.

STRICT RULES — follow these exactly:
- Do NOT use any markdown image syntax such as ![...](...)  — images are handled separately.
- Do NOT wrap the output in a markdown code block (no ```markdown or ``` at start/end).
- Use the ACTUAL numbers from the conversation. Write the real values, not "N/A", unless the data truly was not available.
- Return only the final report text. No preamble, no "here is the report", no comments after.

The report MUST contain these sections in order:

## Financial Report

### 1. Stock Overview
Full company names, current prices, and 6-month percentage performance.

### 2. Fundamental Ratios
A markdown table comparing all stocks with these columns: P/E Ratio, Forward P/E, \
Dividend Yield, Price to Book, Debt/Equity, ROE.
Below the table, briefly describe what each ratio means.

### 3. Normalized Price Performance
Written description of relative price trends, volatility, and which stock \
outperformed or underperformed. Do not include the image — describe it in words.

### 4. Comparative Analysis & Correlation
Compare the stocks to each other. Discuss correlation, relative strength, and risk.

### 5. Recent News Summary
For each stock: summarize the key news themes and explain how the news connects \
to the fundamental ratios.

### 6. Future Scenarios
For each stock provide three scenarios:
- **Positive scenario**
- **Neutral scenario**
- **Negative scenario**"""
]
