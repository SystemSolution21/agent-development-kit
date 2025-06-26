#!/usr/bin/env python3
"""
Test script for the stock_analyst agent.
This script tests the stock analyst functionality without requiring real market data.
"""

import sys
from pathlib import Path
from typing import Any
from unittest.mock import patch, MagicMock
from manager.specialist.stock_analyst.agent import get_stock_price


def test_stock_analyst_without_api() -> None:
    """Test the stock analyst with mocked API responses."""

    # Mock successful stock data response
    mock_stock_data = MagicMock()
    mock_stock_data.info = {"currentPrice": 175.34, "shortName": "Alphabet Inc."}

    print("Testing Stock Analyst Agent")
    print("=" * 40)

    # Test 1: Stock price with mocked API
    print("\n1. Testing with mocked successful API response:")
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.return_value = mock_stock_data

        result = get_stock_price(ticker="GOOG")
        print(f"Result: {result['status']}")
        print(f"Ticker: {result['ticker']}")
        print(f"Price: ${result['price']}")
        print(f"Time: {result['time']}")
        assert result["status"] == "success"
        assert result["ticker"] == "GOOG"
        assert result["price"] == 175.34

    # Test 2: Stock not found
    print("\n2. Testing stock not found:")
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.return_value = None

        result = get_stock_price(ticker="INVALID")
        print(f"Result: {result['status']}")
        print(f"Message: {result['error_message']}")
        assert result["status"] == "error"
        assert "Stock data not found" in result["error_message"]

    # Test 3: Current price not available
    print("\n3. Testing current price not available:")
    with patch("yfinance.Ticker") as mock_ticker:
        mock_stock_no_price = MagicMock()
        mock_stock_no_price.info = {"shortName": "Test Stock"}  # No currentPrice
        mock_ticker.return_value = mock_stock_no_price

        result = get_stock_price(ticker="TEST")
        print(f"Result: {result['status']}")
        print(f"Message: {result['error_message']}")
        assert result["status"] == "error"
        assert "Current price not found" in result["error_message"]

    # Test 4: Exception handling
    print("\n4. Testing exception handling:")
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.side_effect = Exception("API connection error")

        result = get_stock_price(ticker="AAPL")
        print(f"Result: {result['status']}")
        print(f"Message: {result['error_message']}")
        assert result["status"] == "error"
        assert "Error fetching stock data" in result["error_message"]

    print("\n" + "=" * 40)
    print("All tests passed! ✅")


if __name__ == "__main__":
    test_stock_analyst_without_api()
