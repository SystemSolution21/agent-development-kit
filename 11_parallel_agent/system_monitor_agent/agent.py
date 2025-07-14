"""
System Monitor Root Agent

This module defines the root agent for the system monitoring application.
It uses a parallel agent for system information collecting concurrently and a sequential
pipeline for synthesizing the total information.
"""

from google.adk.agents import ParallelAgent, SequentialAgent

from .subagents.cpu_info_agent.agent import cpu_info_agent
from .subagents.disk_info_agent.agent import disk_info_agent
from .subagents.memory_info_agent.agent import memory_info_agent
from .subagents.synthesizer_agent.agent import synthesizer_agent

# Create the parallel agent to collect system information concurrently
system_info_collector = ParallelAgent(
    name="SystemInfoCollector",
    sub_agents=[cpu_info_agent, memory_info_agent, disk_info_agent],
)

# Create the sequential agent to run the parallel agent and then the synthesizer agent
root_agent = SequentialAgent(
    name="SystemMonitorAgent",
    sub_agents=[system_info_collector, synthesizer_agent],
)
