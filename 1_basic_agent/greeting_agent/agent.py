from dotenv import load_dotenv

from google.adk.agents import Agent

# Load environment variables from .env file
load_dotenv()


# Create the root agent
root_agent = Agent(
    name="greeting_agent",
    description="A simple agent that greets the user.",
    model="gemini-2.0-flash",
    instruction=""""
    You are a helpful assistant that greets the user.
    Ask the user's name and then greet them by name.
    """,
)
