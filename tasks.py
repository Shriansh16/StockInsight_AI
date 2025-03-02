from datetime import datetime

def get_financial_tasks(assets):
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    financial_tasks = [
        f"""Today is the {date_str}. 
        What are the current stock prices of {assets}, and how is the performance over the past 6 months in terms of percentage change? 
        Start by retrieving the full name of each stock and use it for all future requests.
        Prepare a figure of the normalized price of these stocks and save it to a file named normalized_prices.png. Include information about, if applicable: 
        * P/E ratio
        * Forward P/E
        * Dividends
        * Price to book
        * Debt/Eq
        * ROE
        * Analyze the correlation between the stocks
        Do not use a solution that requires an API key.
        If some of the data does not makes sense, such as a price of 0, change the query and re-try.""",

        """Investigate possible reasons of the stock performance leveraging market news headlines from Bing News or Google Search. Retrieve news headlines using python and return them. Use the full name stocks to retrieve headlines. Retrieve at least 10 headlines per stock. Do not use a solution that requires an API key. Do not perform a sentiment analysis.""",
    ]
    
    return financial_tasks

writing_tasks = [
    """Develop an engaging financial report using all information provided, include the normalized_prices.png figure,
    and other figures if provided.
    Mainly rely on the information provided. 
    Create a table comparing all the fundamental ratios and data.
    Provide comments and description of all the fundamental ratios and data.
    Compare the stocks, consider their correlation and risks, provide a comparative analysis of the stocks.
    Provide a summary of the recent news about each stock. 
    Ensure that you comment and summarize the news headlines for each stock, provide a comprehensive analysis of the news.
    Provide connections between the news headlines provided and the fundamental ratios.
    Provide an analysis of possible future scenarios. 
    """]