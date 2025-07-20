"""
This module defines a sample agent that utilizes tools.
It demonstrates how to create an agent with a custom tool and Google Search.
"""

from datetime import datetime

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search

# Load environment variables from .env file
load_dotenv()


# Define custom tool
def get_current_time() -> dict:
    """Get the current time."""
    return {"current_time": datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")}


# Create an agent with tool
root_agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    description="Tool agent",
    instruction="""
        You are a helpful assistant that can use the following tools:
        - google_search: Search the web""",
    tools=[
        google_search
    ],  # ADK currently supports only one built-in tool for a single agent.
    # tools=[get_current_time], # Custom tools.
    # tools=[get_current_time, google_search], # Cannot mix custom tools with built-in tools.
)
