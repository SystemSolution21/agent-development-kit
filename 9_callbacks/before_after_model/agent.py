import copy
import logging
from datetime import datetime
from logging import Logger
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions.state import State
from google.genai import types

from utils.logger import AdkLogger

# Initialize logger
logger: Logger = AdkLogger.setup(module_name=__name__, level=logging.INFO)


def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    This callback runs before the model processes a request.
    It filters inappropriate content and logs request info.

    Args:
        callback_context: Contains state and context information
        llm_request: The LLM request being sent

    Returns:
        Optional LlmResponse to override model response
    """

    # Get state and agent name
    state: State = callback_context.state
    agent_name: str = callback_context.agent_name

    # Extract last user-message
    last_user_message: str = ""
    if llm_request.contents and len(llm_request.contents) > 0:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts and len(content.parts) > 0:
                if hasattr(content.parts[0], "text") and content.parts[0].text:
                    last_user_message = content.parts[0].text
                    break

    # Log the before-model-callback request
    logger.info("===== Model Request Started =====")
    logger.info("Agent: %s", agent_name)
    if last_user_message:
        logger.info(f"User message: {last_user_message[:100]}...")
    else:
        logger.info("User message: <empty>")
    logger.info("Timestamp: %s", datetime.now().strftime(format="%Y-%m-%d %H:%M:%S"))

    # Check for inappropriate content
    prohibit: list[str] = [
        "sucks",
        "hate",
        "bad",
        "horrible",
        "terrible",
        "awful",
    ]

    if last_user_message:
        for word in prohibit:
            if word in last_user_message.lower():
                # Log the blocked request
                logger.info(msg="===== Inappropriate Content Blocked =====")
                logger.info(msg=f"Blocked text containing prohibited word {word!r}")
                logger.info(
                    msg="[Before Model Callback] ⚠️ Request blocked due to inappropriate content."
                )

                # Return a response to skip the model call
                return LlmResponse(
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part(
                                text=f"""I cannot respond to messages containing inappropriate language. "
                                "Please rephrase your request without using words like '{word}'."""
                            )
                        ],
                    )
                )

    # Record start time in callback context state
    state["model_start_time"] = datetime.now()

    # Log request approval
    logger.info(msg="[Before Model Callback] ✓ Request approved for processing")

    return None


def after_model_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """
    Simple callback that replaces negative words with more positive alternatives.

    Args:
        callback_context: Contains state and context information
        llm_response: The LLM response received

    Returns:
        Optional LlmResponse to override model response
    """

    # Log the after-model-callback response
    logger.info(msg="===== After Model Callback Response Processing =====")

    # Check llm response and extract response text
    if not llm_response or not llm_response.content or not llm_response.content.parts:
        return None

    response_text: str = ""
    if llm_response and llm_response.content and llm_response.content.parts:
        for part in llm_response.content.parts:
            if hasattr(part, "text") and part.text:
                response_text += part.text

    if not response_text:
        return None

    # Modify the llm response text with words replacements
    replacements: dict[str, str] = {
        "problem": "challenge",
        "difficult": "complex",
        "bad": "challenging",
        "horrible": "challenging",
        "terrible": "challenging",
        "awful": "challenging",
        "sucks": "is a challenge",
        "hate": "dislike",
    }

    modified_text: str = response_text
    MODIFIED = False
    for word, replacement in replacements.items():
        if word in modified_text:
            modified_text = modified_text.replace(word, replacement)
            modified_text = modified_text.replace(
                word.capitalize(), replacement.capitalize()
            )
            MODIFIED = True

    if MODIFIED:
        # Log the modified response text
        logger.info(msg="[After Model Callback] ✓ Response modified")
        logger.info(msg=f"Modified response: {modified_text[:100]}...")

        # Create a new llm response with the modified text
        modified_parts = [copy.deepcopy(part) for part in llm_response.content.parts]
        for i, part in enumerate(modified_parts):
            if hasattr(part, "text") and part.text:
                modified_parts[i].text = modified_text

        return LlmResponse(
            content=types.Content(
                role="model",
                parts=modified_parts,
            )
        )

    # No modification, record state and return the original llm response
    callback_context.state["model_end_time"] = datetime.now()
    return None


# Create the root agent
root_agent = LlmAgent(
    name="content_filter_agent",
    model="gemini-2.0-flash",
    description="An agent that demonstrates model callbacks for content filtering and logging.",
    instruction="""
    You are a helpful assistant.
    
    Your job is to:
    - Answer user questions concisely
    - Provide factual information
    - Be friendly and respectful
    """,
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
