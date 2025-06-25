#!/usr/bin/env python3
"""
Integration test for the weather_analyst agent.
This test uses the real OpenWeatherMap API.
"""

import os
import sys
import pytest
from dotenv import load_dotenv
from typing import Any

# Add the parent directory to the path to import the agents
sys.path.append(os.path.dirname(os.path.abspath(path=__file__)))

from manager.specialist.weather_analyst.agent import (
    get_weather_data,
    get_weather_forecast,
)
from google.adk.tools.tool_context import ToolContext

# Load environment variables from .env file
load_dotenv()

# Skip all tests if API key is not available
pytestmark: pytest.MarkDecorator = pytest.mark.skipif(
    condition=os.getenv(key="OPENWEATHER_API_KEY") is None,
    reason="OPENWEATHER_API_KEY environment variable not set",
)


@pytest.fixture
def tool_context():
    """Create a mock tool context for testing."""

    class MockToolContext:
        def __init__(self) -> None:
            self.state: dict[str, Any] = {}

    return MockToolContext()


def test_get_weather_data_integration(tool_context):
    """Test getting real weather data for a known city."""
    # Test with a city that definitely exists
    city = "London"
    result: dict[str, Any] = get_weather_data(city=city, tool_context=tool_context)

    # Verify the response structure and data
    assert (
        result["status"] == "success"
    ), f"Failed to get weather data: {result.get('error_message', 'Unknown error')}"
    assert result["city"] == "London"
    assert "country" in result
    assert "temperature" in result
    assert "description" in result
    assert "humidity" in result
    assert isinstance(result["temperature"], (int, float))
    assert isinstance(result["humidity"], (int, float))

    # Verify state was updated
    assert tool_context.state["last_weather_city"] == city
    assert tool_context.state["last_weather_data"] == result


def test_get_weather_forecast_integration(tool_context):
    """Test getting real weather forecast for a known city."""
    city = "Paris"
    result = get_weather_forecast(city=city, tool_context=tool_context)

    # Verify the response structure and data
    assert (
        result["status"] == "success"
    ), f"Failed to get forecast: {result.get('error_message', 'Unknown error')}"
    assert result["city"] == "Paris"
    assert "country" in result
    assert "forecasts" in result
    assert len(result["forecasts"]) > 0

    # Check the first forecast entry
    first_forecast = result["forecasts"][0]
    assert "datetime" in first_forecast
    assert "temperature" in first_forecast
    assert "description" in first_forecast
    assert isinstance(first_forecast["temperature"], (int, float))

    # Verify state was updated
    assert tool_context.state["last_forecast_city"] == city
    assert tool_context.state["last_forecast_data"] == result


def test_invalid_city(tool_context):
    """Test behavior with an invalid city name."""
    city = "NonExistentCityXYZ123"
    result = get_weather_data(city=city, tool_context=tool_context)

    # Should return an error status
    assert result["status"] == "error"
    assert "not found" in result["error_message"].lower()


if __name__ == "__main__":
    # If API key is not set, print a helpful message
    if os.getenv("OPENWEATHER_API_KEY") is None:
        print("OPENWEATHER_API_KEY environment variable not set.")
        print("Please set it in your .env file to run integration tests.")
        print("Get a free API key from https://openweathermap.org/api")
        sys.exit(1)

    # Manual test execution
    context = tool_context()

    print("\n=== Testing Weather Data ===")
    weather = get_weather_data("Tokyo", context)
    if weather["status"] == "success":
        print(f"Current weather in {weather['city']}, {weather['country']}:")
        print(
            f"🌡️ Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)"
        )
        print(f"🌤️ Conditions: {weather['description']}")
        print(f"💨 Wind: {weather['wind_speed']} m/s")
        print(f"💧 Humidity: {weather['humidity']}%")
    else:
        print(f"Error: {weather['error_message']}")

    print("\n=== Testing Weather Forecast ===")
    forecast = get_weather_forecast("Berlin", context)
    if forecast["status"] == "success":
        print(f"Weather forecast for {forecast['city']}, {forecast['country']}:")
        for entry in forecast["forecasts"][:3]:  # Show first 3 forecasts
            print(
                f"{entry['datetime']}: {entry['temperature']}°C - {entry['description']}"
            )
    else:
        print(f"Error: {forecast['error_message']}")
