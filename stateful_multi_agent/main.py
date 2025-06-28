import asyncio
import uuid

from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.sessions.session import Session

from customer_service_agent.agent import customer_service_agent

# Load environment variables from .env file
load_dotenv()

# ===== Application constants =====
APP_NAME: str = "Customer Support"
USER_ID: str = "john_doe"

# ===== Initialize State =====
initial_state: dict = {
    "user_name": "John Doe",
    "purchased_courses": [],
    "interaction_history": [],
}

# ===== Initialize In-Memory Session Service =====
session_service = InMemorySessionService()


# ===== Create Session =====
async def create_session() -> Session:
    session_id = str(object=uuid.uuid4())

    session: Session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
        state=initial_state,
    )
    print(f"\nSession created: Session ID: {session_id}")
    return session


# ===== Agent Runner Setup =====
async def agent_runner() -> Runner:
    runner = Runner(
        app_name=APP_NAME,
        agent=customer_service_agent,
        session_service=session_service,
    )
    return runner


# ===== Main Entrypoint =====
async def main_async() -> None:

    # Create Session
    session: Session = await create_session()

    # Agent Runner Setup
    runner: Runner = await agent_runner()

    # ===== Interactive Conversation Loop =====
    print("\nWelcome to the Customer Service Agent Chat!")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    # Start conversation
    while True:
        user_input: str = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation.")
            break

    # Update interaction history with the user's query
