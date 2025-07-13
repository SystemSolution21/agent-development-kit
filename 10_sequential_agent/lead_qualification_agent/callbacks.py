"""
Shared callback functions for lead qualification subagents.
"""

import logging
from datetime import datetime
from typing import Callable, Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions.state import State


def create_before_model_callback(
    logger: logging.Logger, next_step_message: str = ""
) -> Callable:
    """Factory to create a pre-execution logging Before Model callback."""

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
    """Factory to create a post-execution logging After Model Callback."""

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
        return None

    return after_model_callback


def create_before_agent_callback(
    logger: logging.Logger, next_step_message: str = ""
) -> Callable:
    """Factory to create a pre-execution logging callback for Before Agent Callback."""

    def before_agent_callback(
        callback_context: CallbackContext,
    ) -> Optional[LlmResponse]:
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
    """Factory to create a post-execution logging callback for After Agent Callback."""

    def after_agent_callback(callback_context: CallbackContext) -> None:
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
