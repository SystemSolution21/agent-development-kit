# Multi-Agent System

This example demonstrates a multi-agent system with a manager agent that coordinates specialist agents.

## Agents

### Manager Agent

The manager agent is responsible for delegating tasks to the appropriate specialist agents based on the user's request.

### Specialist Agents

1. **Weather Analyst** - Provides current weather information and forecasts for cities worldwide using OpenWeatherMap API
2. **Stock Analyst** - Analyzes stock prices using Yahoo Finance API
3. **News Analyst** - Analyzes news articles using Google Search

## Setup

1. Copy `.env.example` to `.env` and fill in your API keys:
   - `GOOGLE_API_KEY`: Your Google API key for the Gemini model
   - `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key (get one free at <https://openweathermap.org/api>)

2. Install dependencies:

   ```bash
   uv add requests
   ```

## Usage

The manager agent will automatically delegate weather-related queries to the weather analyst, stock-related queries to the stock analyst, and news-related queries to the news analyst.

Example queries:

- "What's the weather like in New York?"
- "Get me the weather forecast for London"
- "What's the current price of AAPL stock?"
- "Find news about artificial intelligence"

## API Keys

### OpenWeatherMap API

1. Go to <https://openweathermap.org/api>
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file as `OPENWEATHER_API_KEY`

The free tier includes:

- 1,000 API calls per day
- Current weather data
- 5-day weather forecast
- Weather maps

## Reference

<https://github.com/bhancockio/agent-development-kit-crash-course/blob/main/7-multi-agent/README.md>
