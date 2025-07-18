"""
LinkedIn Post Generator Agent

This agent generates the initial LinkedIn post before refinement.
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
    logger=logger, next_step_message="Generating initial LinkedIn post..."
)
after_model_callback: Callable[..., Any] = create_after_model_callback(logger=logger)

# Define the Initial Post Generator Agent
initial_post_generator = LlmAgent(
    name="InitialPostGenerator",
    model=GEMINI_MODEL,
    instruction="""You are a LinkedIn Post Generator.

    Your task is to create a LinkedIn post about an Agent Development Kit (ADK) tutorial by @aiwithbrandon.
    
    ## CONTENT REQUIREMENTS
    Ensure the post includes:
    1. Excitement about learning from the tutorial
    2. Specific aspects of ADK learned:
       - Basic agent implementation (basic-agent)
       - Tool integration (tool-agent)
       - Using LiteLLM (litellm-agent)
       - Managing sessions and memory
       - Persistent storage capabilities
       - Multi-agent orchestration
       - Stateful multi-agent systems
       - Callback systems
       - Sequential agents for pipeline workflows
       - Parallel agents for concurrent operations
       - Loop agents for iterative refinement
    3. Brief statement about improving AI applications
    4. Mention/tag of @aiwithbrandon
    5. Clear call-to-action for connections
    
    ## STYLE REQUIREMENTS
    - Professional and conversational tone
    - Between 1000-1500 characters
    - NO emojis
    - NO hashtags
    - Show genuine enthusiasm
    - Highlight practical applications
    
    ## OUTPUT INSTRUCTIONS
    - Return ONLY the post content
    - Do not add formatting markers or explanations
    """,
    description="Generates the initial LinkedIn post to start the refinement process",
    output_key="current_post",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
