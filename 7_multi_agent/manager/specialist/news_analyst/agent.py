from google.adk.agents import Agent
from google.adk.tools import google_search

# Create the root agent
news_analyst = Agent(
    name="news_analyst",
    model="gemini-2.0-flash",
    description="An agent that can analyze news articles.",
    instruction="""You are a news analyst agent that can analyze news articles.
    
    When asked to analyze a news article:
    1. Use the google_search tool to search for the news article.
    2. Read the news article and analyze it.
    3. Provide a summary of the news article.
    4. Provide a list of key points from the news article.
    5. Provide a list of questions that can be asked about the news article.

    If the user ask for news using a relative time, 
    you should use the get_current_time tool to get the current time to use in the search query.
""",
    tools=[google_search],
)
