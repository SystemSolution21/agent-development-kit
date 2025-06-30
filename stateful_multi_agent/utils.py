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
    session_service,
    app_name,
    user_id,
    session_id,
    entry,
):
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
        session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )

        # Get current interaction history
        interaction_history = session.state.get("interaction_history", [])

        # Check timestamp
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")

        # Add entry to interaction history
        interaction_history.append(entry)

        # Create updated state
        updated_state = session.state.copy()
        updated_state["interaction_history"] = interaction_history

        # Create new session with updated state
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=updated_state,
        )

    except Exception as e:
        print(f"Error updating interaction history: {e}")


async def add_agent_response_interaction_history(
    session_service,
    app_name,
    user_id,
    session_id,
    agent_name,
    response,
):
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


async def add_user_query_interaction_history(
    session_service,
    app_name,
    user_id,
    session_id,
    query,
):
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


async def display_state(
    session_service, app_name, user_id, session_id, label="Current State"
):
    """Display the current session state in a formatted way."""
    try:
        # Get the most up-to-date session
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        # Format the output with clear sections
        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # Handle the user name
        user_name = session.state.get("user_name", "Unknown")
        print(f"👤 User: {user_name}")

        # Handle purchased courses
        purchased_courses = session.state.get("purchased_courses", [])
        if purchased_courses and any(purchased_courses):
            print("📚 Courses:")
            for course in purchased_courses:
                if isinstance(course, dict):
                    course_id = course.get("id", "Unknown")
                    purchase_date = course.get("purchase_date", "Unknown date")
                    print(f"  - {course_id} (purchased on {purchase_date})")
                elif course:  # Handle string format for backward compatibility
                    print(f"  - {course}")
        else:
            print("📚 Courses: None")

        # Handle interaction history in a more readable way
        if (
            "interaction_history" in session.state
            and session.state["interaction_history"]
        ):
            print("📝 Interaction History:")
            for i, entry in enumerate(session.state["interaction_history"], 1):
                if entry.get("action") == "user_query":
                    timestamp = entry.get("timestamp", "Unknown time")
                    query = entry.get("query", "Unknown query")
                    print(f'  {i}. User query at {timestamp}: "{query}"')
                elif entry.get("action") == "agent_response":
                    timestamp = entry.get("timestamp", "Unknown time")
                    agent_name = entry.get("agent_name", "Unknown agent")
                    response_text = entry.get("response", "No response")
                    # Truncate long responses for display
                    if len(response_text) > 50:
                        response_text = response_text[:50] + "..."
                    print(
                        f'  {i}. {agent_name} response at {timestamp}: "{response_text}"'
                    )
                else:
                    # Generic fallback for other entry types
                    action = entry.get("action", "unknown")
                    timestamp = entry.get("timestamp", "Unknown time")
                    print(f"  {i}. {action} at {timestamp}")
        else:
            print("📝 Interaction History: None")

        # Show any additional state keys that might exist
        other_keys = [
            k
            for k in session.state.keys()
            if k not in ["user_name", "purchased_courses", "interaction_history"]
        ]
        if other_keys:
            print("🔑 Additional State:")
            for key in other_keys:
                print(f"  {key}: {session.state[key]}")

        print("-" * (22 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")


async def process_agent_response(event):
    """Process and display agent response events."""
    print(f"Event ID: {event.id}, Author: {event.author}")

    # Check for specific parts first
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"  Text: '{part.text.strip()}'")

    # Check for final response after specific parts
    final_response = None
    if not has_specific_part and event.is_final_response():
        if (
            event.content
            and event.content.parts
            and hasattr(event.content.parts[0], "text")
            and event.content.parts[0].text
        ):
            final_response = event.content.parts[0].text.strip()
            # Use colors and formatting to make the final response stand out
            print(
                f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ AGENT RESPONSE ═════════════════════════════════════════{Colors.RESET}"
            )
            print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
            print(
                f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n"
            )
        else:
            print(
                f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> Final Agent Response: [No text content in final event]{Colors.RESET}\n"
            )

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent asynchronously with the user's query."""

    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Running Query: {query} ---{Colors.RESET}"
    )
    final_response_text = None
    agent_name = None

    # Display state before processing the query
    await display_state(
        session_service=runner.session_service,
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
        label="State Before Processing",
    )

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Capture the agent name from the event if available
            if event.author:
                agent_name = event.author

            response = await process_agent_response(event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"{Colors.BG_RED}{Colors.WHITE}ERROR during agent run: {e}{Colors.RESET}")

    # Add the agent response to interaction history if we got a final response
    if final_response_text and agent_name:
        await add_agent_response_interaction_history(
            session_service=runner.session_service,
            app_name=runner.app_name,
            user_id=user_id,
            session_id=session_id,
            agent_name=agent_name,
            response=final_response_text,
        )

    # Display state after processing the message
    await display_state(
        session_service=runner.session_service,
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
        label="State AFTER processing",
    )

    # # Add debug state call
    # await debug_state(
    #     session_service=runner.session_service,
    #     app_name=runner.app_name,
    #     user_id=user_id,
    #     session_id=session_id,
    # )

    print(f"{Colors.YELLOW}{'-' * 30}{Colors.RESET}")
    return final_response_text


async def debug_state(session_service, app_name, user_id, session_id):
    """Debug function to print the raw state for troubleshooting."""
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        print("\n===== DEBUG: RAW STATE =====")
        print(f"Session ID: {session_id}")
        print(f"Raw state: {session.state}")
        print("=============================\n")
    except Exception as e:
        print(f"Error debugging state: {e}")
