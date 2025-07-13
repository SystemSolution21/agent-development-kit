"""
Lead Validator Agent

This agent is responsible for validating if a lead has all the necessary information
for qualification.
"""

import logging
from typing import Any, Callable

from google.adk.agents import LlmAgent

from lead_qualification_agent.callbacks import (
    create_after_model_callback,
    create_before_model_callback,
)

# Get logger
logger: logging.Logger = logging.getLogger(name=f"adk_log.{__name__}")

# Create callbacks
before_model_callback: Callable[..., Any] = create_before_model_callback(logger=logger)
after_model_callback: Callable[..., Any] = create_after_model_callback(
    logger=logger, next_step_message="Workflows proceed to Lead Scorer Agent."
)


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
