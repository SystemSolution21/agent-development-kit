from datetime import datetime
from typing import Any
import yfinance as yf
from google.adk.agents import Agent


def get_stock_price(
    ticker: str,
) -> dict:
    """Get the current stock price."""
    print(f"--- Tool: get_stock_price called for ticker {ticker} ---")

    try:
        # Get the stock data
        stock_data: yf.Ticker = yf.Ticker(ticker=ticker)

        if stock_data is None:
            return {"status": "error", "error_message": "Stock data not found"}

        # Get the current time
        current_time: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")

        # Get the current price
        current_price: Any | None = stock_data.info.get("currentPrice")

        if current_price is None:
            return {"status": "error", "error_message": "Current price not found"}

        return {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "time": current_time,
        }

    except Exception as e:
        return {"status": "error", "error_message": f"Error fetching stock data: {e}"}


# Create the root agent
stock_analyst = Agent(
    name="stock_analyst",
    model="gemini-2.0-flash",
    description="An agent that can analyze stock prices.",
    instruction="""You are a stock analyst agent that can analyze stock prices.
    
    When asked to analyze a stock:
    1. Use the get_stock_price tool to get the current stock price.
    2. Format the response to show each stock's current price and the time it was fetched
    3. If a stock price couldn't be fetched, mention this in your response
    
    Example response format:
    "Here are the current prices for your stocks:
    - GOOG: $175.34 (updated at 2024-04-21 16:30:00)
    - TSLA: $156.78 (updated at 2024-04-21 16:30:00)
    - META: $123.45 (updated at 2024-04-21 16:30:00)"
""",
    tools=[get_stock_price],
)
