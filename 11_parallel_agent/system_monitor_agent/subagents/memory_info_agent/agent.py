"""
Memory Information Agent

This agent is responsible for collecting and analyzing memory information.
"""

import logging
from typing import Any, Callable

from google.adk.agents import LlmAgent

from ...utils.callbacks import create_after_tool_callback, create_before_tool_callback
from .tools import get_memory_info

# Initialize logger
logger: logging.Logger = logging.getLogger(name=f"system_monitor.{__name__}")


# Create callbacks
before_tool_callback: Callable[..., Any] = create_before_tool_callback(logger=logger)
after_tool_callback: Callable[..., Any] = create_after_tool_callback(logger=logger)

# Create memory information agent
memory_info_agent = LlmAgent(
    name="MemoryInfoAgent",
    model="gemini-2.0-flash",
    instruction="""You are a Memory Information Agent.
    
    When asked for system information, you should:
    1. Use the 'get_memory_info' tool to gather memory data
    2. Analyze the returned dictionary data
    3. Format this information into a concise, clear section of a system report
    
    The tool will return a dictionary with:
    - result: Core memory information
    - stats: Key statistical data about memory usage
    - additional_info: Context about the data collection
    
    Format your response as a well-structured report section with:
    - Total and available memory
    - Memory usage statistics
    - Swap memory information
    - Any performance concerns (high usage > 80%)
    
    IMPORTANT: You MUST call the get_memory_info tool. Do not make up information.
    """,
    description="Gathers and analyzes memory information",
    tools=[get_memory_info],
    output_key="memory_info",
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)
