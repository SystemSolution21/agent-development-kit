#!/usr/bin/env python3
"""
Integration test for the stock_analyst agent.
This test uses the real yfinance API.
"""

import os
import sys
import pytest
from typing import Any
from manager.specialist.stock_analyst.agent import get_stock_price


def test_get_stock_price_integration():
    """Test getting real stock data for known tickers."""
    # Test with a ticker that definitely exists
    ticker = "AAPL"
    result: dict[str, Any] = get_stock_price(ticker=ticker)

    # Verify the response structure and data
    assert (
        result["status"] == "success"
    ), f"Failed to get stock data: {result.get('error_message', 'Unknown error')}"
    assert result["ticker"] == "AAPL"
    assert "price" in result
    assert "time" in result
    assert isinstance(result["price"], (int, float))


def test_invalid_ticker():
    """Test behavior with an invalid ticker symbol."""
    ticker = "INVALIDTICKERSYMBOL123XYZ"
    result = get_stock_price(ticker=ticker)

    # Should return an error status
    assert result["status"] == "error"
    # finance can return different error message
    assert any(
        msg in result["error_message"]
        for msg in ["Error fetching stock data", "Current price not found"]
    )


if __name__ == "__main__":
    # Manual test execution
    print("\n=== Testing Stock Price Data ===")

    # Test multiple stocks
    for ticker in ["GOOG", "MSFT", "AMZN"]:
        stock_data: dict[Any, Any] = get_stock_price(ticker=ticker)
        if stock_data["status"] == "success":
            print(
                f"Current price for {ticker}: ${stock_data['price']} (as of {stock_data['time']})"
            )
        else:
            print(f"Error for {ticker}: {stock_data['error_message']}")
