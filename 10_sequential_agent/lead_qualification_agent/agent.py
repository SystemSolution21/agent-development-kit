"""
Sequential Agent with a Minimal Callback

This example demonstrates a lead qualification pipeline with a minimal
before_agent_callback that only initializes state once at the beginning.
"""

import logging
from typing import Any, Callable

from google.adk.agents import SequentialAgent

from utils.adk_logger import setup_adk_logging

from .callbacks import create_after_agent_callback, create_before_agent_callback
from .subagents.recommender import action_recommender_agent
from .subagents.scorer import lead_scorer_agent
from .subagents.validator import lead_validator_agent

# Initialize logger
setup_adk_logging()
# Get logger
logger: logging.Logger = logging.getLogger(name=f"adk_log.{__name__}")

# Create callbacks
before_agent_callback: Callable[..., Any] = create_before_agent_callback(
    logger=logger, next_step_message="Workflows proceed to Lead Validator Agent."
)

after_agent_callback: Callable[..., Any] = create_after_agent_callback(logger=logger)


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
