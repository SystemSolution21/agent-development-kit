"""
Sequential Agent with a Minimal Callback

This example demonstrates a lead qualification pipeline with a minimal
before_agent_callback that only initializes state once at the beginning.
"""

import logging
from datetime import datetime
from logging import Logger

from google.adk.agents import SequentialAgent
from google.adk.agents.callback_context import CallbackContext

from utils.logger import AdkLogger

from .subagents.recommender import action_recommender_agent
from .subagents.scorer import lead_scorer_agent
from .subagents.validator import lead_validator_agent

# Initialize logger
logger: Logger = AdkLogger.get_logger(module_name=__name__, level=logging.INFO)


def before_agent_callback(callback_context: CallbackContext) -> None:
    """
    Simple callback that logs when the agent starts processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None
    """

    # Get agent name
    agent_name: str = callback_context.agent_name
    # Timestamp
    timestamp: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
    # Log process start
    logger.info("===== Agent Execution Started =====")
    logger.info("Agent: %s", agent_name)
    logger.info("Timestamp: %s", timestamp)


def after_agent_callback(callback_context: CallbackContext) -> None:
    """
    Simple callback that logs when the agent finishes processing a request.

    Args:
        callback_context: Contains state and context information

    Returns:
        None
    """

    # Get agent name
    agent_name: str = callback_context.agent_name
    # Timestamp
    timestamp: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
    # Log process end
    logger.info("===== Agent Execution Completed =====")
    logger.info("Agent: %s", agent_name)
    logger.info("Timestamp: %s", timestamp)


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
