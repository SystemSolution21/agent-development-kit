import asyncio
from typing import Any
from datetime import datetime
from types import CoroutineType

from google.adk.sessions import InMemorySessionService
from google.adk.sessions.session import Session
from google.genai import types


# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


async def update_interaction_history(
    session_service: InMemorySessionService,
    app_name: str,
    user_id: str,
    session_id: str,
    entry: dict,
) -> None:
    """Add an entry to the interaction history in state.

    Args:
        session_service: The session service instance
        app_name: The application name
        user_id: The user ID
        session_id: The session ID
        entry: A dictionary containing the interaction data
            - requires 'action' key (e.g., 'user_query', 'agent_response')
            - other keys are flexible depending on the action type
    """
    try:
        # Get current session
        session: Session | None = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )

        # Get current interaction history
        interaction_history: list = (
            await session.state.get("interaction_history", []) if session else []
        )

        # Check timestamp
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")

        # Append entry to interaction history
        interaction_history.append(entry)

        # Update session state if session exists
        if session is not None:
            update_state: dict[str, Any] = session.state.copy()
            update_state["interaction_history"] = interaction_history

        # Create new session with updated state
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=update_state,
        )

    except Exception as e:
        print(f"Error updating interaction history: {e}")


async def add_agent_response_to_interaction_history(
    session_service: InMemorySessionService,
    app_name: str,
    user_id: str,
    session_id: str,
    agent_name: str,
    response: str,
) -> None:
    """Add the agent's response to the interaction history in the session state."""
    await update_interaction_history(
        session_service=session_service,
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        entry={
            "action": "agent_response",
            "agent_name": agent_name,
            "response": response,
        },
    )


async def add_user_query_to_interaction_history(
    session_service: InMemorySessionService,
    app_name: str,
    user_id: str,
    session_id: str,
    query: str,
) -> None:
    """Add the user's query to the interaction history in the session state."""
    await update_interaction_history(
        session_service=session_service,
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        entry={
            "action": "user_query",
            "query": query,
        },
    )
