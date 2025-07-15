"""CPU Information Agent

This agent is responsible for collecting and analyzing CPU information.
It uses the 'get_cpu_info' tool to collect data and then formats it into a
concise, clear section of a system report.
"""

import logging
from typing import Any, Callable

from google.adk.agents import LlmAgent

from ...utils.callbacks import create_after_tool_callback, create_before_tool_callback
from .tools import get_cpu_info

# Initialize logger
logger: logging.Logger = logging.getLogger(name=f"system_monitor.{__name__}")

# Create callbacks
before_tool_callback: Callable[..., Any] = create_before_tool_callback(logger=logger)
after_tool_callback: Callable[..., Any] = create_after_tool_callback(logger=logger)

# Create the CPU information agent
cpu_info_agent = LlmAgent(
    name="CpuInfoAgent",
    model="gemini-2.0-flash",
    instruction="""You are a CPU Information Agent.
    
    When asked for system information, you should:
    1. Use the 'get_cpu_info' tool to collect CPU data
    2. Analyze the returned dictionary data
    3. Format this information into a concise, clear section of a system report
    
    The tool will return a dictionary with:
    - result: Core CPU information
    - stats: Key statistical data about CPU usage
    - additional_info: Context about the data collection
    
    Format your response as a well-structured report section with:
    - CPU core information (physical vs logical)
    - CPU usage statistics
    - Any performance concerns (high usage > 80%)
    
    IMPORTANT: You MUST call the get_cpu_info tool. Do not make up information.
    """,
    description="Collects and analyzes CPU information",
    tools=[get_cpu_info],
    output_key="cpu_info",
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)
