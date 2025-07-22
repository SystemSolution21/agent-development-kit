import asyncio
import os
import uuid

import psycopg2

# import config  # Configuration
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions.base_session_service import ListSessionsResponse
from google.adk.sessions.session import Session
from persistent_agent.agent import persistent_agent
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from utility import call_agent_async

# Load environment variables from .env file
load_dotenv()


# ===== Validate Database Configuration =====
def validate_database_config() -> dict[str, str | None]:
    """Validate all required database configuration."""
    required_vars: dict[str, str | None] = {
        "PG_HOST": os.environ.get("PG_HOST"),
        "PG_PORT": os.environ.get("PG_PORT"),
        "PG_USER": os.environ.get("PG_USER"),
        "PG_PASSWORD": os.environ.get("PG_PASSWORD"),
        "PG_DBNAME": os.environ.get("PG_DBNAME"),
    }

    missing_vars: list[str] = [var for var, value in required_vars.items() if not value]

    if missing_vars:
        print(
            f"Error: Missing required environment variables: {', '.join(missing_vars)}"
        )
        print(
            "Please check your .env file and ensure all PostgreSQL variables are set."
        )
        exit(1)

    return required_vars


# Get validated database configuration
db_config: dict[str, str | None] = validate_database_config()
PG_HOST: str | None = db_config["PG_HOST"]
PG_PORT: str | None = db_config["PG_PORT"]
PG_USER: str | None = db_config["PG_USER"]
PG_PASSWORD: str | None = db_config["PG_PASSWORD"]
PG_DBNAME: str | None = db_config["PG_DBNAME"]

# ===== Validate Application Configuration =====
APP_NAME = str(os.environ.get("APP_NAME"))
USER_ID = str(os.environ.get("USER_ID"))
USER_NAME = str(os.environ.get("USER_NAME"))

if not all([APP_NAME, USER_ID, USER_NAME]):
    print("Error: APP_NAME, USER_ID, and USER_NAME must be set in environment.")
    exit(code=1)


# ===== Create Database if it doesn't exist =====
def create_database_not_exists() -> None:
    """Create the database if it doesn't exist."""
    try:
        # Connect to postgres database to create our target database
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASSWORD,
            database="postgres",  # Connect to default postgres db
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{PG_DBNAME}'")

        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {PG_DBNAME}")
            print(f"Created database: {PG_DBNAME}")
        else:
            print(f"Database {PG_DBNAME} already exists")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error creating database: {e}")
        exit(1)


# Create database if it doesn't exist
create_database_not_exists()

# ===== Initialize Persistent Session Service =====
DB_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"
session_service = DatabaseSessionService(db_url=DB_URL)


# ===== Define Initial State =====
initial_state: dict = {
    "user_name": USER_NAME,
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
    print(f"\nWelcome to {APP_NAME} Chat!")
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
