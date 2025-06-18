import os
import random
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Load environment variables
load_dotenv()


# Setup openrouter model
model = LiteLlm(
    model="openrouter/openai/gpt-4.1",
    api_key=os.getenv(key="OPENROUTER_API_KEY"),
)

# Setup openai model
model = LiteLlm(
    model="openai/gpt-4.1",
    api_key=os.getenv(key="OPENAI_API_KEY"),
)

# Setup ollama model
model = LiteLlm(
    model="ollama_chat/llama3.2:3b",
)


# Define custom tool
def get_joke():
    """Get a random joke from a list of jokes."""
    jokes: list[str] = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "Why don't skeletons fight each other? They don't have the guts!",
    ]
    return random.choice(seq=jokes)


# Create agent
root_agent = Agent(
    name="joke_agent",
    model=model,
    description="An agent that can tell jokes.",
    instruction="""
    You are a helpful assistant that can tell jokes.
    You can use the `get_joke` tool to get a random joke.
    """,
    tools=[get_joke],
)
