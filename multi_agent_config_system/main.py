import asyncio
import time
from pathlib import Path

from agent_config.agent_factory import AgentFactory
from agent_config.config_manager import AgentConfigManager
from config.app_config_loader import load_app_config
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Load environment variables
load_dotenv()

# Load application configuration
app_config = load_app_config()

# Application constants from config
APP_NAME = app_config.app_name
USER_ID = app_config.default_user_id

# Initialize state from config
initial_state= {"user_name": app_config.default_user_name, **app_config.initial_state}

# Initialize session service
session_service = InMemorySessionService()

# Get the directory where this script is located
script_dir = Path(__file__).parent

# Initialize configuration system with paths from config
config_manager = AgentConfigManager(
    config_dir=str(script_dir / app_config.agents_config_dir),
    template_dir=str(script_dir / app_config.templates_dir),
    environment=app_config.environment,
)

# Initialize agent factory
agent_factory = AgentFactory(config_manager)


async def main_async() -> None:
    """Main entrypoint for the application."""

    # Create a new session
    new_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    session_id = new_session.id
    print(f"\nSession created: Session ID: {session_id}")

    # Create the root agent with state variables
    customer_service_agent = agent_factory.create_agent(
        "customer_service", state_variables=initial_state
    )

    # Create a runner
    runner = Runner(
        app_name=APP_NAME,
        agent=customer_service_agent,
        session_service=session_service,
    )

    # Interactive conversation loop
    print("\nWelcome to the Customer Service Agent Chat!")
    print("Type 'exit' or 'quit' to end the conversation.")

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        # Update interaction history
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

        if session and hasattr(session, "state"):
            # Add user query to interaction history
            interaction_history = session.state.get("interaction_history", [])
            interaction_history.append(
                {
                    "action": "user_query",
                    "query": user_input,
                    "timestamp": "2023-06-30 12:00:00",  # In a real app, use actual timestamp
                }
            )

            # Create updated state
            updated_state = session.state.copy()
            updated_state["interaction_history"] = interaction_history

            # Update session state by creating a new session with the same ID
            await session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id,
                state=updated_state,
            )

        # Process the user query
        new_message = types.Content(role="user", parts=[types.Part(text=user_input)])

        # Retry mechanism for API overload errors
        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                final_response_text = None
                async for event in runner.run_async(
                    user_id=USER_ID, session_id=session_id, new_message=new_message
                ):
                    if event.is_final_response():
                        if event.content and event.content.parts:
                            # Handle both text and function call parts
                            text_parts = [
                                part.text for part in event.content.parts
                                if hasattr(part, 'text') and part.text
                            ]
                            if text_parts:
                                final_response_text = "\n".join(text_parts)
                                print(f"\nAgent: {final_response_text}")
                            else:
                                print("\nAgent: [Processing your request...]")
                break  # Success, exit retry loop

            except Exception as e:
                error_type = type(e).__name__
                is_retryable = ("503" in str(e) or "overloaded" in str(e).lower()
                               or "UNAVAILABLE" in str(e))

                if is_retryable and attempt < max_retries - 1:
                    print(f"\n⚠️  Service temporarily unavailable (attempt {attempt + 1}/{max_retries})")
                    print(f"💡 Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    # Final attempt failed or non-retryable error
                    if "503" in str(e) or "overloaded" in str(e).lower():
                        print(f"\n❌ Service temporarily unavailable after {max_retries} attempts")
                        print("💡 The AI service is currently overloaded. Please try again later.")
                    elif "UNAVAILABLE" in str(e):
                        print(f"\n❌ Service unavailable: {e}")
                        print("💡 Please check your internet connection and try again.")
                    else:
                        print(f"\n❌ An error occurred ({error_type}): {e}")
                        print("💡 Please try rephrasing your request or try again later.")
                    break

        # In a real app, you would also update the interaction history with the agent's response


if __name__ == "__main__":
    asyncio.run(main_async())
