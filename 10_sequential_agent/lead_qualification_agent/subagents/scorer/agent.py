"""
Lead Scorer Agent

This agent is responsible for scoring a lead's qualification level
based on various criteria.
"""

import logging
from datetime import datetime
from logging import Logger
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

from utils.logger import AdkLogger

# Initialize logger
logger: Logger = AdkLogger.get_logger(module_name=__name__, level=logging.INFO)


def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
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

    return None


def after_model_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
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
    logger.info("Workflows proceed to Lead Recommender Agent.")

    return None


# Create scorer agent
lead_scorer_agent = LlmAgent(
    name="LeadScorerAgent",
    model="gemini-2.0-flash",
    instruction="""You are a Lead Scoring AI.
    
    Analyze the lead information and assign a qualification score from 1-10 based on:
    - Expressed need (urgency/clarity of problem)
    - Decision-making authority
    - Budget indicators
    - Timeline indicators
    
    Output ONLY a numeric score and ONE sentence justification.
    
    Example output: '8: Decision maker with clear budget and immediate need'
    Example output: '3: Vague interest with no timeline or budget mentioned'
    """,
    description="Scores qualified leads on a scale of 1-10.",
    output_key="lead_score",
)
