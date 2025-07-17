"""Callbacks for logging agent and model execution."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions.state import State
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

# Create documentation directory
current_dir: Path = Path(__file__).parent.parent.resolve()
docs_dir: Path = current_dir / "docs"
docs_dir.mkdir(exist_ok=True)
doc_file: Path = docs_dir / "system_health_report.md"


def create_before_agent_callback(
    logger: logging.Logger, next_step_message: str = ""
) -> Callable:
    """Pre-execution logging for Before Agent Callback."""

    def before_agent_callback(
        callback_context: CallbackContext,
    ) -> Optional[LlmResponse]:
        """Logs agent execution start."""

        agent_name: str = callback_context.agent_name
        timestamp: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
        logger.info("===== Agent Execution Started =====")
        logger.info("Agent: %s", agent_name)
        logger.info("Timestamp: %s", timestamp)
        if next_step_message:
            logger.info(next_step_message)
        if callback_context.state.get(key="start_time") is None:
            callback_context.state["start_time"] = datetime.now()
        return None

    return before_agent_callback


def create_after_agent_callback(
    logger: logging.Logger, next_step_message: str = ""
) -> Callable:
    """Post-execution logging for After Agent Callback."""

    def after_agent_callback(callback_context: CallbackContext) -> None:
        """Logs agent execution completion."""

        state: State = callback_context.state
        agent_name: str = callback_context.agent_name
        timestamp: datetime = datetime.now()
        logger.info("===== Agent Execution Completed =====")
        logger.info("Agent: %s", agent_name)
        logger.info("Timestamp: %s", timestamp.strftime(format="%Y-%m-%d %H:%M:%S"))
        if next_step_message:
            logger.info(next_step_message)
        if "start_time" in state:
            logger.info(
                "Total processing time: %.2f seconds",
                (timestamp - state["start_time"]).total_seconds(),
            )
        return None

    return after_agent_callback


def create_before_model_callback(
    logger: logging.Logger, next_step_message: str = ""
) -> Callable:
    """Pre-execution logging for Before Model Callback."""

    def before_model_callback(
        callback_context: CallbackContext, llm_request: LlmRequest
    ) -> Optional[LlmResponse]:
        """Logs agent execution start."""

        agent_name: str = callback_context.agent_name
        timestamp: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
        logger.info("===== Agent Execution Started =====")
        logger.info("Agent: %s", agent_name)
        logger.info("Timestamp: %s", timestamp)

        # Log next step message
        if next_step_message:
            logger.info(next_step_message)

        # Record start time in state
        if callback_context.state.get(key="start_time") is None:
            callback_context.state["start_time"] = datetime.now()

        return None

    return before_model_callback


def create_after_model_callback(
    logger: logging.Logger, next_step_message: str = ""
) -> Callable:
    """Post-execution logging and system health report for After Model Callback."""

    def after_model_callback(
        callback_context: CallbackContext, llm_response: LlmResponse
    ) -> Optional[LlmResponse]:
        """Logs agent execution completion."""

        agent_name: str = callback_context.agent_name
        timestamp: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
        logger.info("===== Agent Execution Completed =====")
        logger.info("Agent: %s", agent_name)
        logger.info("Timestamp: %s", timestamp)
        if next_step_message:
            logger.info(next_step_message)
        if "cpu_info" and "memory_info" and "disk_info" in callback_context.state:
            logger.info(
                f"CPU Information: {callback_context.state['cpu_info'].strip('\n')[:200]}..."
            )
            logger.info(
                f"Memory Information: {callback_context.state['memory_info'].strip('\n')[:200]}..."
            )
            logger.info(
                f"Disk Information: {callback_context.state['disk_info'].strip('\n')[:200]}..."
            )

        # Write system health report to file
        with open(doc_file, "w") as f:
            if llm_response and llm_response.content and llm_response.content.parts:
                if isinstance(llm_response.content.parts[0].text, str):
                    f.write(llm_response.content.parts[0].text)

        return None

    return after_model_callback


def create_before_tool_callback(
    logger: logging.Logger, next_step_message: str = ""
) -> Callable:
    """Pre-execution logging for Before Tool Callback."""

    def before_tool_callback(
        tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
    ) -> Optional[dict]:
        """Logs tool execution start."""

        tool_name: str = tool.name
        timestamp: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
        logger.info("===== Tool Execution Started =====")
        logger.info("Tool: %s", tool_name)
        logger.info("Timestamp: %s", timestamp)
        if next_step_message:
            logger.info(next_step_message)

        return None

    return before_tool_callback


def create_after_tool_callback(
    logger: logging.Logger, next_step_message: str = ""
) -> Callable:
    """Post-execution logging for After Tool Callback."""

    def after_tool_callback(
        tool: BaseTool,
        args: dict[str, Any],
        tool_context: ToolContext,
        tool_response: dict,
    ) -> Optional[dict]:
        """Logs tool execution completion."""

        tool_name: str = tool.name
        timestamp: str = datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")
        logger.info("===== Tool Execution Completed =====")
        logger.info("Tool: %s", tool_name)
        logger.info("Timestamp: %s", timestamp)
        result = str(tool_response.get("result", tool_response))
        logger.info(f"Tool Response: {result[:100]}...")

        return tool_response

    return after_tool_callback
