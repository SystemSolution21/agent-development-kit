"""This agent orchestrates the pipeline by running the sub_agents in order."""

from google.adk.agents import SequentialAgent

from .subagents.agent import (
    code_refactor_agent,
    code_reviewer_agent,
    code_writer_agent,
)

# Create the SequentialAgent ---
root_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[code_writer_agent, code_reviewer_agent, code_refactor_agent],
    description="Executes a sequence of code writing, reviewing, and refactoring.",
)
