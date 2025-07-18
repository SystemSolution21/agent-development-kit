"""
LinkedIn Post Refiner Agent

This agent refines LinkedIn posts based on review feedback.
"""

import logging
from typing import Any, Callable

from google.adk.agents.llm_agent import LlmAgent

from ...constant import GEMINI_MODEL
from ...utils.callbacks import create_after_model_callback, create_before_model_callback

# Initialize logger
logger: logging.Logger = logging.getLogger(name=f"linkedin_post_generation.{__name__}")

# Create callbacks
before_model_callback: Callable[..., Any] = create_before_model_callback(
    logger=logger,
    next_step_message="Refining LinkedIn post based on review feedback...",
)
after_model_callback: Callable[..., Any] = create_after_model_callback(logger=logger)

# Define the Post Refiner Agent
post_refiner = LlmAgent(
    name="PostRefinerAgent",
    model=GEMINI_MODEL,
    instruction="""You are a LinkedIn Post Refiner.

    Your task is to refine a LinkedIn post based on review feedback.
    
    ## INPUTS
    **Current Post:**
    {current_post}
    
    **Review Feedback:**
    {review_feedback}
    
    ## TASK
    Carefully apply the feedback to improve the post.
    - Maintain the original tone and theme of the post
    - Ensure all content requirements are met:
      1. Excitement about learning from the tutorial
      2. Specific aspects of ADK learned (at least 4)
      3. Brief statement about improving AI applications
      4. Mention/tag of @aiwithbrandon
      5. Clear call-to-action for connections
    - Adhere to style requirements:
      - Professional and conversational tone
      - Between 1000-1500 characters
      - NO emojis
      - NO hashtags
      - Show genuine enthusiasm
      - Highlight practical applications
    
    ## OUTPUT INSTRUCTIONS
    - Output ONLY the refined post content
    - Do not add explanations or justifications
    """,
    description="Refines LinkedIn posts based on feedback to improve quality",
    output_key="current_post",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
