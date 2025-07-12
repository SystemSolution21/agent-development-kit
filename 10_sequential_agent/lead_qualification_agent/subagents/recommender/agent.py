"""
Action Recommender Agent

This agent is responsible for recommending appropriate next actions
based on the lead validation and scoring results.
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
logger: Logger = AdkLogger.setup(module_name=__name__, level=logging.INFO)


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

    return None


# Create recommender agent
action_recommender_agent = LlmAgent(
    name="ActionRecommenderAgent",
    model="gemini-2.0-flash",
    instruction="""You are an Action Recommendation AI.
    
    Based on the lead information and scoring:
    
    - For invalid leads: Suggest what additional information is needed
    - For leads scored 1-3: Suggest nurturing actions (educational content, etc.)
    - For leads scored 4-7: Suggest qualifying actions (discovery call, needs assessment)
    - For leads scored 8-10: Suggest sales actions (demo, proposal, etc.)
    
    Format your response as a complete recommendation to the sales team.
    
    Lead Score:
    {lead_score}

    Lead Validation Status:
    {validation_status}
    """,
    description="Recommends next actions based on lead validation and scoring results.",
    output_key="action_recommendation",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
