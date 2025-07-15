import logging
from typing import Any, Callable

from google.adk.agents import LlmAgent

from ...utils.callbacks import create_after_tool_callback, create_before_tool_callback
from .tools import get_disk_info

# Initialize logger
logger: logging.Logger = logging.getLogger(name=f"system_monitor.{__name__}")

# Create callbacks
before_tool_callback: Callable[..., Any] = create_before_tool_callback(logger=logger)
after_tool_callback: Callable[..., Any] = create_after_tool_callback(logger=logger)

disk_info_agent = LlmAgent(
    name="DiskInfoAgent",
    model="gemini-2.0-flash",
    instruction="""You are a Disk Information Agent.
    
    When asked for system information, you should:
    1. Use the 'get_disk_info' tool to gather disk data
    2. Analyze the returned dictionary data
    3. Format this information into a concise, clear section of a system report
    
    The tool will return a dictionary with:
    - result: Core disk information including partitions
    - stats: Key statistical data about storage usage
    - additional_info: Context about the data collection
    
    Format your response as a well-structured report section with:
    - Partition information
    - Storage capacity and usage
    - Any storage concerns (high usage > 85%)
    
    IMPORTANT: You MUST call the get_disk_info tool. Do not make up information.
    """,
    description="Gathers and analyzes disk information",
    tools=[get_disk_info],
    output_key="disk_info",
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)
