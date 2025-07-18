"""
LinkedIn Post Reviewer Agent

This agent reviews LinkedIn posts for quality and provides feedback.
"""

import logging
from typing import Any, Callable

from google.adk.agents.llm_agent import LlmAgent

from ...constant import GEMINI_MODEL
from ...utils.callbacks import create_after_tool_callback, create_before_tool_callback
from .tools import count_characters, exit_loop

# Initialize logger
logger: logging.Logger = logging.getLogger(name=f"linkedin_post_generation.{__name__}")

# Create callbacks
before_tool_callback: Callable[..., Any] = create_before_tool_callback(logger=logger)
after_tool_callback: Callable[..., Any] = create_after_tool_callback(logger=logger)

# Define the Post Reviewer Agent
post_reviewer = LlmAgent(
    name="PostReviewer",
    model=GEMINI_MODEL,
    instruction="""You are a LinkedIn Post Quality Reviewer.

    Your task is to evaluate the quality of a LinkedIn post about Agent Development Kit (ADK).
    
    ## EVALUATION PROCESS
    1. Use the count_characters tool to check the post's length.
       Pass the post text directly to the tool.
    
    2. If the length check fails (tool result is "fail"), provide specific feedback on what needs to be fixed.
       Use the tool's message as a guideline, but add your own professional critique.
    
    3. If length check passes, evaluate the post against these criteria:
       - REQUIRED ELEMENTS:
         1. Mentions @aiwithbrandon
         2. Lists multiple ADK capabilities (at least 4)
         3. Has a clear call-to-action
         4. Includes practical applications
         5. Shows genuine enthusiasm
       
       - STYLE REQUIREMENTS:
         1. NO emojis
         2. NO hashtags
         3. Professional tone
         4. Conversational style
         5. Clear and concise writing
    
    ## OUTPUT INSTRUCTIONS
    IF the post fails ANY of the checks above:
      - Return concise, specific feedback on what to improve
      
    ELSE IF the post meets ALL requirements:
      - Call the exit_loop function
      - Return "Post meets all requirements. Exiting the refinement loop."
      
    Do not embellish your response. Either provide feedback on what to improve OR call exit_loop and return the completion message.
    
    ## POST TO REVIEW
    {current_post}
    """,
    description="Reviews post quality and provides feedback on what to improve or exits the loop if requirements are met",
    tools=[count_characters, exit_loop],
    output_key="review_feedback",
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)
