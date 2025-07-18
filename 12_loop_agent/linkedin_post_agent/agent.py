"""
LinkedIn Post Generator Root Agent

This module defines the root agent for the LinkedIn post generation application.
It uses a sequential agent with an initial post generator followed by a refinement loop.
"""

import logging
from typing import Any, Callable

from google.adk.agents import LoopAgent, SequentialAgent

from .subagents.post_generator.agent import initial_post_generator
from .subagents.post_refiner.agent import post_refiner
from .subagents.post_reviewer.agent import post_reviewer
from .utils.callbacks import create_after_agent_callback, create_before_agent_callback
from .utils.linkedin_post_generation_logger import setup_logging

# Initialize logger
setup_logging()
logger: logging.Logger = logging.getLogger(name=f"linkedin_post_generation.{__name__}")

# Create callbacks for Refinement Loop Agent
before_loop_agent_callback: Callable[..., Any] = create_before_agent_callback(
    logger=logger,
    next_step_message="Workflows proceed to LinkedIn Post Reviewer Agent.",
)
after_loop_agent_callback: Callable[..., Any] = create_after_agent_callback(
    logger=logger
)

# Create the Refinement Loop Agent
refinement_loop = LoopAgent(
    name="PostRefinementLoop",
    max_iterations=5,
    sub_agents=[
        post_reviewer,
        post_refiner,
    ],
    description="Iteratively reviews and refines a LinkedIn post until quality requirements are met",
    before_agent_callback=before_loop_agent_callback,
    after_agent_callback=after_loop_agent_callback,
)

# Callbacks for root agent
before_agent_callback: Callable[..., Any] = create_before_agent_callback(
    logger=logger,
    next_step_message="Workflows proceed to LinkedIn Initial Post Generator.",
)
after_agent_callback: Callable[..., Any] = create_after_agent_callback(logger=logger)

# Create the Sequential Pipeline Agent
root_agent = SequentialAgent(
    name="LinkedInPostGenerationPipeline",
    sub_agents=[
        initial_post_generator,  # Step 1: Generate initial post
        refinement_loop,  # Step 2: Review and refine in a loop
    ],
    description="Generates and refines a LinkedIn post through an iterative review process",
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)
