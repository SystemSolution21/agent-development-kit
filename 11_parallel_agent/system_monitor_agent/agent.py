"""
System Monitor Root Agent

This module defines the root agent for the system monitoring application.
It uses a parallel agent for system information collecting concurrently and a sequential
pipeline for synthesizing the total information.
"""

import logging
from typing import Any, Callable

from google.adk.agents import ParallelAgent, SequentialAgent

from .subagents.cpu_info_agent.agent import cpu_info_agent
from .subagents.disk_info_agent.agent import disk_info_agent
from .subagents.memory_info_agent.agent import memory_info_agent
from .subagents.synthesizer_agent.agent import synthesizer_agent
from .utils.callbacks import create_after_agent_callback, create_before_agent_callback
from .utils.system_monitor_logger import setup_logging

# Initialize logger
setup_logging()
logger: logging.Logger = logging.getLogger(name=f"system_monitor.{__name__}")

# Create callbacks
before_agent_callback: Callable[..., Any] = create_before_agent_callback(
    logger=logger,
    next_step_message="Workflows proceed to System Info Collector Parallel Agent.",
)

after_agent_callback: Callable[..., Any] = create_after_agent_callback(logger=logger)

# Create the parallel agent to collect system information concurrently
system_info_collector = ParallelAgent(
    name="SystemInfoCollector",
    sub_agents=[cpu_info_agent, memory_info_agent, disk_info_agent],
)

# Create the sequential agent to run the parallel agent and then the synthesizer agent
root_agent = SequentialAgent(
    name="SystemMonitorAgent",
    sub_agents=[system_info_collector, synthesizer_agent],
    description="A system monitoring agent that gathers system information and produces a comprehensive system health report.",
    before_agent_callback=before_agent_callback,
    after_agent_callback=after_agent_callback,
)
