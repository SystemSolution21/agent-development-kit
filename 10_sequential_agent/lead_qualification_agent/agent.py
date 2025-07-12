"""
Sequential Agent with a Minimal Callback

This example demonstrates a lead qualification pipeline with a minimal
before_agent_callback that only initializes state once at the beginning.
"""

import logging
from datetime import datetime
from logging import Logger
from typing import Optional

from google.adk.agents import SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.sessions.state import State
from google.genai import types as genai_types

from utils.logger import AdkLogger

from .subagents.recommender import action_recommender_agent
from .subagents.scorer import lead_scorer_agent
from .subagents.validator import lead_validator_agent

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
        None
    """

    # Get session state
    state: State = callback_context.state
    # Get agent name
    agent_name: str = callback_context.agent_name
    # Timestamp
    timestamp: datetime = datetime.now()
    # Record start time in state
    state["start_time"] = timestamp

    # Log process start
    logger.info("===== Agent Execution Started =====")
    logger.info("Agent: %s", agent_name)
    logger.info("Timestamp: %s", timestamp.strftime(format="%Y-%m-%d %H:%M:%S"))
    logger.info("Workflows proceed to Lead Validator Agent.")

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
    # Get agent name
    agent_name: str = callback_context.agent_name
    # Timestamp
    timestamp: datetime = datetime.now()
    # Log process end
    logger.info("===== Agent Execution Completed =====")
    logger.info("Agent: %s", agent_name)
    logger.info("Timestamp: %s", timestamp.strftime(format="%Y-%m-%d %H:%M:%S"))
    if "start_time" in state:
        logger.info(
            "Total processing time: %.2f seconds",
            (timestamp - state["start_time"]).total_seconds(),
        )


# Create sequential lead qualification agent(root_agent) with minimal callback
root_agent = SequentialAgent(
    name="LeadQualificationAgent",
    description="A pipeline that validates, scores, and recommends actions for sales leads",
    sub_agents=[
        lead_validator_agent,
        lead_scorer_agent,
        action_recommender_agent,
    ],
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)
