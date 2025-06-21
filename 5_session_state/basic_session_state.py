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

# Application constants
APP_NAME: str = "John Bot"
USER_ID: str = "john_doe"

# Creates an in-memory session service to maintain state between interactions
memory_session_service = InMemorySessionService()

# Defines initial state with user information
initial_state: dict[str, str] = {
    "user_name": "John Doe",
    "user_preferences": """
        I like to play Football, Cricket, and Badminton.
        My favorite food is Curry.
        My favorite TV show is Science Zero.
        Loves to travel, read books, and watch movies.
        I am a software engineer.
        """,
}


# Creates a new session with a unique ID and initial state
async def create_session() -> str:
    # Generate session ID
    SESSION_ID: str = str(object=uuid.uuid4())
    # Create session
    session_service: Session = await memory_session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    print(f"Session created:\nSession ID: {SESSION_ID}")
    return SESSION_ID


# Agent runner
async def run_agent(SESSION_ID: str, input_text: str) -> None:

    runner = Runner(
        app_name=APP_NAME,
        agent=question_answer_agent,
        session_service=memory_session_service,
    )

    new_message = types.Content(role="user", parts=[types.Part(text=input_text)])

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"\nFinal response:\n{event.content.parts[0].text}")


# Logging session state
async def log_session_state(SESSION_ID: str) -> None:

    print("====== Session State ======")
    session: Session | None = await memory_session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    if session is not None and hasattr(session, "state"):
        for key, value in session.state.items():
            print(f"{key}: {value}")
    else:
        print("Session not found or has no state.")


# Main Entrypoint
async def main(input_text: str) -> None:

    # Create session
    SESSION_ID: str = await create_session()

    # Run agent
    await run_agent(SESSION_ID=SESSION_ID, input_text=input_text)

    # Log session state
    await log_session_state(SESSION_ID=SESSION_ID)


# Run the async main function
if __name__ == "__main__":
    while True:
        input_text: str = input("Ask a question (press 'q' to quit): ")
        if input_text.lower() == "q":
            break

        asyncio.run(main=main(input_text=input_text))
