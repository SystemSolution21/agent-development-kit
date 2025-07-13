"""
Action Recommender Agent

This agent is responsible for recommending appropriate next actions
based on the lead validation and scoring results.
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
after_model_callback: Callable[..., Any] = create_after_model_callback(logger=logger)


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
