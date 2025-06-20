from google.adk.agents import Agent

# Create the root agent
question_answer_agent = Agent(
    name="question_answer_agent",
    description="An agent that can answer questions.",
    model="gemini-2.0-flash",
    instruction="""
    You are a helpful assistant that answers questions about the user's preferences.

    Here is some information about the user.
    Name:
    {user_name}
    Preferences:
    {user_preferences}
    """,
)
