"""
Synthesizer Agent

This agent is responsible for synthesizing the information collected by the
parallel agents into a comprehensive system health report.
"""

import logging
from typing import Any, Callable

from google.adk.agents import LlmAgent

from ...utils import create_after_model_callback, create_before_model_callback

# Initialize logger
logger: logging.Logger = logging.getLogger(name=f"system_monitor.{__name__}")

# Create callbacks
before_model_callback: Callable[..., Any] = create_before_model_callback(
    logger=logger, next_step_message="Synthesizing CPU, Memory and Disk information..."
)
after_model_callback: Callable[..., Any] = create_after_model_callback(logger=logger)

# Create synthesizer agent
synthesizer_agent = LlmAgent(
    name="SynthesizerAgent",
    model="gemini-2.0-flash",
    instruction="""You are a System Report Synthesizer.
    
    Your task is to create a comprehensive system health report by combining information from:
    - CPU information: {cpu_info}
    - Memory information: {memory_info}
    - Disk information: {disk_info}
    
    Create a well-formatted report with:
    1. An executive summary at the top with overall system health status
    2. Sections for each component with their respective information
    3. Recommendations based on any concerning metrics
    
    Use markdown formatting to make the report readable and professional.
    Highlight any concerning values and provide practical recommendations.
    """,
    description="Synthesizes all system information into a comprehensive report",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
