import asyncio
import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions.base_session_service import ListSessionsResponse
from google.adk.sessions.session import Session
from persistent_agent.agent import persistent_agent

from .utils import call_agent_async

# Load environment variables from .env file
load_dotenv()


# ===== Application constants =====
APP_NAME: str = "Persistent Agent"
USER_ID: str = "john_doe"


# ===== Initialize Persistent Session Service =====
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)


# ===== Define Initial State =====
initial_state: dict = {
    "user_name": "John Doe",
    "reminders": [],
}


# Main entrypoint
async def main_async() -> None:
    # ===== Session Management =====
    # Get existing sessions for the user
    existing_sessions: ListSessionsResponse = await session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    # Check existing sessions
    if existing_sessions and len(existing_sessions.sessions) > 0:
        # Most recent session
        SESSION_ID: str = existing_sessions.sessions[0].id
        print(f"Continuing existing session: {SESSION_ID}")
    else:
        # Create new session with initial state
        new_session: Session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
            session_id=str(object=uuid.uuid4()),
        )
        SESSION_ID: str = new_session.id
        print(f"Created new session: {SESSION_ID}")

    # ===== Agent Runner Setup =====
    runner = Runner(
        app_name=APP_NAME,
        agent=persistent_agent,
        session_service=session_service,
    )

    # ===== Interactive Conversation Loop =====
    print("\nWelcome to Persistent Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    # Start conversation
    while True:
        user_input: str = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print(
                "Ending conversation. Your remainders has been saved to the database."
            )
            break

        # process the user query
        await call_agent_async(
            runner=runner,
            user_id=USER_ID,
            session_id=SESSION_ID,
            query=user_input,
        )


# Run the async main function
if __name__ == "__main__":
    asyncio.run(main=main_async())
