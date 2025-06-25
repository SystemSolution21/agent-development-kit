import os
import requests
from datetime import datetime
from typing import Any
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

# Load environment variables
load_dotenv()


def get_weather_data(city: str, tool_context: ToolContext) -> dict:
    """Get current weather data for a specified city using OpenWeatherMap API.

    Args:
        city: The name of the city to get weather for
        tool_context: Context for accessing and updating session state

    Returns:
        A dictionary containing weather information or error details
    """
    print(f"--- Tool: get_weather_data called for city {city} ---")

    # Get API key from environment variables
    api_key: str | None = os.getenv(key="OPENWEATHER_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "error_message": "OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY in your .env file.",
        }

    try:
        # OpenWeatherMap API endpoint
        base_url = "http://api.openweathermap.org/data/2.5/weather"

        # Parameters for the API request
        params: dict[str, str] = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Celsius for temperature
        }

        # Make the API request
        response: requests.Response = requests.get(
            url=base_url, params=params, timeout=10
        )

        if response.status_code == 200:
            data: Any = response.json()

            # Extract relevant weather information
            weather_info: dict[str, Any] = {
                "status": "success",
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "description": data["weather"][0]["description"],
                "main_weather": data["weather"][0]["main"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"].get("deg", "N/A"),
                "visibility": data.get("visibility", "N/A"),
                "timestamp": datetime.now().strftime(format="%Y-%m-%d %H:%M:%S"),
            }

            # Update the state with the last queried city
            tool_context.state["last_weather_city"] = city
            tool_context.state["last_weather_data"] = weather_info

            return weather_info

        elif response.status_code == 404:
            return {
                "status": "error",
                "error_message": f"City '{city}' not found. Please check the spelling and try again.",
            }
        else:
            return {
                "status": "error",
                "error_message": f"Weather API request failed with status code: {response.status_code}",
            }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error_message": "Weather API request timed out. Please try again later.",
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Error fetching weather data: {str(object=e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error: {str(object=e)}",
        }


def get_weather_forecast(city: str, tool_context: ToolContext) -> dict:
    """Get 5-day weather forecast for a specified city using OpenWeatherMap API.

    Args:
        city: The name of the city to get forecast for
        tool_context: Context for accessing and updating session state

    Returns:
        A dictionary containing forecast information or error details
    """
    print(f"--- Tool: get_weather_forecast called for city {city} ---")

    # Get API key from environment variables
    api_key: str | None = os.getenv(key="OPENWEATHER_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "error_message": "OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY in your .env file.",
        }

    try:
        # OpenWeatherMap 5-day forecast API endpoint
        base_url = "http://api.openweathermap.org/data/2.5/forecast"

        # Parameters for the API request
        params: dict[str, str] = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Celsius for temperature
        }

        # Make the API request
        response: requests.Response = requests.get(
            url=base_url, params=params, timeout=10
        )

        if response.status_code == 200:
            data: Any = response.json()

            # Extract forecast information (next 5 days, every 3 hours)
            forecasts: list[dict[str, Any]] = []
            for item in data["list"][:8]:  # Get next 24 hours (8 * 3-hour intervals)
                forecast: dict[str, Any] = {
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "feels_like": item["main"]["feels_like"],
                    "humidity": item["main"]["humidity"],
                    "description": item["weather"][0]["description"],
                    "main_weather": item["weather"][0]["main"],
                    "wind_speed": item["wind"]["speed"],
                    "precipitation_probability": item.get("pop", 0)
                    * 100,  # Convert to percentage
                }
                forecasts.append(forecast)

            forecast_info: dict[str, Any] = {
                "status": "success",
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "forecasts": forecasts,
                "timestamp": datetime.now().strftime(format="%Y-%m-%d %H:%M:%S"),
            }

            # Update the state with the last forecast query
            tool_context.state["last_forecast_city"] = city
            tool_context.state["last_forecast_data"] = forecast_info

            return forecast_info

        elif response.status_code == 404:
            return {
                "status": "error",
                "error_message": f"City '{city}' not found. Please check the spelling and try again.",
            }
        else:
            return {
                "status": "error",
                "error_message": f"Weather forecast API request failed with status code: {response.status_code}",
            }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error_message": "Weather forecast API request timed out. Please try again later.",
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"Error fetching weather forecast: {str(object=e)}",
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Unexpected error: {str(object=e)}",
        }


# Create the weather analyst agent
weather_analyst = Agent(
    name="weather_analyst",
    model="gemini-2.0-flash",
    description="An agent that provides current weather information and forecasts for cities worldwide.",
    instruction="""You are a weather analyst agent that provides comprehensive weather information.
    
    When asked about weather:
    1. Use the get_weather_data tool to get current weather conditions for a specific city
    2. Use the get_weather_forecast tool to get weather forecasts for a specific city
    3. Format the response in a clear, user-friendly manner
    4. Include relevant details like temperature, humidity, wind conditions, and weather description
    5. If the user asks for a forecast, provide the upcoming weather predictions
    
    Example response format for current weather:
    "Current weather in [CITY], [COUNTRY]:
    🌡️ Temperature: [TEMP]°C (feels like [FEELS_LIKE]°C)
    🌤️ Conditions: [DESCRIPTION]
    💨 Wind: [WIND_SPEED] m/s
    💧 Humidity: [HUMIDITY]%
    🌏 Pressure: [PRESSURE] hPa
    
    Last updated: [TIMESTAMP]"
    
    Example response format for forecast:
    "Weather forecast for [CITY], [COUNTRY]:
    
    [TIME]: [TEMP]°C - [DESCRIPTION]
    [TIME]: [TEMP]°C - [DESCRIPTION]
    ..."
    
    If there's an error (like city not found or API issues), explain the problem clearly and suggest alternatives.
    
    Available cities: Any city worldwide (use proper city names)
    
    If the user asks about anything else that's not weather-related, 
    you should delegate the task to the manager agent.
    """,
    tools=[get_weather_data, get_weather_forecast],
)
