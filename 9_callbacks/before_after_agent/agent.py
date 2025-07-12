import logging
from datetime import datetime
from logging import Logger
from typing import Any, Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.genai import types as genai_types

from utils.logger import AdkLogger

# Initialize logger
logger: Logger = AdkLogger.setup(module_name=__name__, level=logging.INFO)


def before_agent_callback(
    callback_context: CallbackContext,
) -> Optional[genai_types.Content]:
    """
    Simple callback that logs when the agent starts processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None to continue with normal agent processing
    """

    # Get session state
    state: State = callback_context.state

    # Get timestamp
    timestamp: datetime = datetime.now()

    # Check and set agent name in state
    if "agent_name" not in state:
        state["agent_name"] = "SimpleChatAgent"

    # Initialize request count
    if "request_count" not in state:
        state["request_count"] = 1
    else:
        state["request_count"] += 1

    # Store request timestamp
    state["request_start_time"] = timestamp

    # Log the request
    logger.info("===== Agent Execution Started =====")
    logger.info("Request #%s", state["request_count"])
    logger.info("Agent: %s", state["agent_name"])
    logger.info("Timestamp: %s", timestamp)
    logger.info(
        "[Before Callback] Agent processing request #%s", state["request_count"]
    )

    return None


def after_agent_callback(callback_context: CallbackContext) -> None:
    """
    Simple callback that logs when the agent finishes processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None
    """

    # Get session state
    state: State = callback_context.state

    # Calculate request duration
    timestamp: datetime = datetime.now()
    duration: Any = None
    if "request_start_time" in state:
        duration: Any = (timestamp - state["request_start_time"]).total_seconds()

    # Log the request processing
    logger.info("===== Agent Execution Completed =====")
    logger.info("Request #%s", state.get(key="request_count", default="Unknown"))
    logger.info("Agent: %s", state.get(key="agent_name", default="Unknown"))
    logger.info("Timestamp: %s", timestamp)
    logger.info(
        "[After Callback] Agent finished processing request #%s",
        state.get(key="request_count", default="Unknown"),
    )
    if duration is not None:
        logger.info("[After Callback] processing took %.2f seconds", duration)

    return None


root_agent = LlmAgent(
    name="before_after_agent",
    model="gemini-2.0-flash",
    description="A basic agent that demonstrates before and after agent callbacks",
    instruction="""
    You are a friendly greeting agent. Your name is {agent_name}.
    
    Your job is to:
    - Greet users politely
    - Respond to basic questions
    - Keep your responses friendly and concise
    """,
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)
