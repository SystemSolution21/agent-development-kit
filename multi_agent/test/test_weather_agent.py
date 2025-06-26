#!/usr/bin/env python3
"""
Test script for the weather_analyst agent.
This script tests the weather agent functionality without requiring API keys.
"""

import os
import sys
from typing import Any
from unittest.mock import patch, MagicMock
from google.adk.tools.tool_context import ToolContext
from manager.specialist.weather_analyst.agent import (
    get_weather_data,
    get_weather_forecast,
)


def test_weather_agent_without_api() -> None:
    """Test the weather agent with mocked API responses."""

    # Create a mock tool context
    mock_context = MagicMock(spec=ToolContext)
    mock_context.state = {}

    # Mock successful weather API response
    mock_weather_response: dict[str, Any] = {
        "name": "New York",
        "sys": {"country": "US"},
        "main": {"temp": 22.5, "feels_like": 24.0, "humidity": 65, "pressure": 1013},
        "weather": [{"description": "partly cloudy", "main": "Clouds"}],
        "wind": {"speed": 3.5, "deg": 180},
        "visibility": 10000,
    }

    # Mock forecast API response
    mock_forecast_response: dict[str, Any] = {
        "city": {"name": "New York", "country": "US"},
        "list": [
            {
                "dt_txt": "2024-01-01 12:00:00",
                "main": {"temp": 23.0, "feels_like": 25.0, "humidity": 60},
                "weather": [{"description": "sunny", "main": "Clear"}],
                "wind": {"speed": 2.5},
                "pop": 0.1,
            }
        ]
        * 8,  # Simulate 8 forecast entries
    }

    print("Testing Weather Analyst Agent")
    print("=" * 40)

    # Test 1: Weather data without API key
    print("\n1. Testing without API key:")
    with patch.dict(os.environ, {}, clear=True):
        result: dict[str, Any] = get_weather_data(
            city="New York", tool_context=mock_context
        )
        print(f"Result: {result['status']}")
        print(f"Message: {result['error_message']}")
        assert result["status"] == "error"
        assert "API key not found" in result["error_message"]

    # Test 2: Weather data with mocked API
    print("\n2. Testing with mocked successful API response:")
    with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_key"}):
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_weather_response
            mock_get.return_value = mock_response

            result = get_weather_data(city="New York", tool_context=mock_context)
            print(f"Result: {result['status']}")
            print(f"City: {result['city']}, {result['country']}")
            print(f"Temperature: {result['temperature']}°C")
            print(f"Description: {result['description']}")
            assert result["status"] == "success"
            assert result["city"] == "New York"

    # Test 3: City not found
    print("\n3. Testing city not found:")
    with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_key"}):
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            result = get_weather_data("InvalidCity", mock_context)
            print(f"Result: {result['status']}")
            print(f"Message: {result['error_message']}")
            assert result["status"] == "error"
            assert "not found" in result["error_message"]

    # Test 4: Weather forecast
    print("\n4. Testing weather forecast:")
    with patch.dict(os.environ, {"OPENWEATHER_API_KEY": "test_key"}):
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_forecast_response
            mock_get.return_value = mock_response

            result = get_weather_forecast("New York", mock_context)
            print(f"Result: {result['status']}")
            print(f"City: {result['city']}, {result['country']}")
            print(f"Number of forecasts: {len(result['forecasts'])}")
            print(
                f"First forecast: {result['forecasts'][0]['datetime']} - {result['forecasts'][0]['temperature']}°C"
            )
            assert result["status"] == "success"
            assert len(result["forecasts"]) == 8

    print("\n" + "=" * 40)
    print("All tests passed! ✅")
    print("\nTo use the weather agent with real data:")
    print("1. Get a free API key from https://openweathermap.org/api")
    print("2. Add OPENWEATHER_API_KEY=your_key_here to your .env file")
    print("3. Run the agent using: adk web")


if __name__ == "__main__":
    test_weather_agent_without_api()
