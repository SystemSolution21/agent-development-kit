"""
Lead Scorer Agent

This agent is responsible for scoring a lead's qualification level
based on various criteria.
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
    logger=logger, next_step_message="Workflows proceed to Action Recommender Agent."
)

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
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
