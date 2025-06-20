import asyncio
import uuid

from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.sessions.session import Session
from google.genai import types

from question_answer_agent.agent import question_answer_agent


# Load environment variables from .env file
load_dotenv()

# Instantiate a session service to manage user state
session_service_state = InMemorySessionService()

# Create user state
user_state: dict[str, str] = {
    "user_name": "Raju Limbu",
    "user_preferences": """
        I like to play Football, Cricket, and Badminton.
        My favorite food is Curry.
        My favorite TV show is Science Zero.
        Loves to travel, read books, and watch movies.
        I am a software engineer.
        """,
}


# Main Entrypoint
async def main(input_text: str) -> None:

    # Create session
    APP_NAME: str = "Raju Bot"
    USER_ID: str = "raju_limbu"
    SESSION_ID: str = str(object=uuid.uuid4())

    session_state: Session = await session_service_state.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=user_state,
    )

    print(f"Session created:\nSession ID: {SESSION_ID}")

    # Instantiate agent runner
    runner = Runner(
        app_name=APP_NAME,
        agent=question_answer_agent,
        session_service=session_service_state,
    )

    # Run the agent
    new_message = types.Content(role="user", parts=[types.Part(text=input_text)])

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"\nFinal response:\n{event.content.parts[0].text}")

    # Logging
    print("\n====== Final Session State ======")
    session: Session | None = await session_service_state.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    if session is not None and hasattr(session, "state"):
        for key, value in session.state.items():
            print(f"{key}: {value}")
    else:
        print("Session not found or has no state.")


# Run the async main function
if __name__ == "__main__":
    while True:
        input_text: str = input("Ask a question (press 'q' to quit): ")
        if input_text.lower() == "q":
            break

        asyncio.run(main=main(input_text=input_text))
