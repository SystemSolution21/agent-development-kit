"""
Lead Validator Agent

This agent is responsible for validating if a lead has all the necessary information
for qualification.
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
    logger.info("Workflows proceed to Lead Scorer Agent.")

    return None


# Create validator agent
lead_validator_agent = LlmAgent(
    name="LeadValidatorAgent",
    model="gemini-2.0-flash",
    instruction="""You are a Lead Validation AI.
    
    Examine the lead information provided by the user and determine if it's complete enough for qualification.
    A complete lead should include:
    - Contact information (name, email or phone)
    - Some indication of interest or need
    - Company or context information if applicable
    
    Output ONLY 'valid' or 'invalid' with a single reason if invalid.
    
    Example valid output: 'valid'
    Example invalid output: 'invalid: missing contact information'
    """,
    description="Validates lead information for completeness.",
    output_key="validation_status",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
