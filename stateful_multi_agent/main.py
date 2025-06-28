import asyncio

from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.sessions.session import Session

from customer_service_agent.agent import customer_service_agent
from .utils import add_user_query_to_interaction_history


# Load environment variables from .env file
load_dotenv()

# ===== Application constants =====
APP_NAME: str = "Customer Service"
USER_ID: str = "john_doe"

# ===== Initialize State =====
initial_state: dict = {
    "user_name": "John Doe",
    "purchased_courses": [],
    "interaction_history": [],
}

# ===== Initialize In-Memory Session Service =====
session_service = InMemorySessionService()


# ===== Main Entrypoint =====
async def main_async() -> None:

    # ===== Session Creation =====
    # Create a new session
    new_session: Session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    session_id: str = new_session.id
    print(f"\nSession created: Session ID: {session_id}")

    # ===== Agent Runner Setup =====
    # Create a runner
    runner = Runner(
        app_name=APP_NAME,
        agent=customer_service_agent,
        session_service=session_service,
    )

    # ===== Interactive Conversation Loop =====
    print("\nWelcome to the Customer Service Agent Chat!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        user_input: str = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        # Update interaction history with the user's query
        await add_user_query_to_interaction_history(
            session_service=session_service,
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            query=user_input,
        )
