import logging
from typing import Any

from google.adk.tools.tool_context import ToolContext

from ...constant import MAX_POST_LENGTH, MIN_POST_LENGTH

# Initialize logger
logger: logging.Logger = logging.getLogger(name=f"linkedin_post_generation.{__name__}")


def count_characters(post: str, tool_context: ToolContext) -> dict[str, Any]:
    """
    Tool to count characters in the provided post and provide length-based feedback.
    Updates review_status in the state based on length requirements.

    Args:
        post: The post to analyze for character count
        tool_context: Context for accessing and updating session state

    Returns:
        Dict[str, Any]: Dictionary containing:
            - result: 'fail' or 'pass'
            - char_count: number of characters in post
            - message: feedback message about the length
    """
    char_count: int = len(post)
    # Log
    logger.info(msg="---Executing count_characters tool---")
    logger.info(msg=f"Checking post length: {char_count} characters")

    if char_count < MIN_POST_LENGTH:
        char_needed: int = MIN_POST_LENGTH - char_count
        tool_context.state["review_status"] = "fail"
        # Log
        logger.info(
            msg=f"Post is too short. Add {char_needed} more characters to reach minimum length of{MIN_POST_LENGTH}."
        )
        return {
            "result": "fail",
            "char_count": char_count,
            "char_needed": char_needed,
            "message": f"Post is too short. Add {char_needed} more characters to reach minimum length of{MIN_POST_LENGTH}.",
        }
    elif char_count > MAX_POST_LENGTH:
        char_excess = char_count - MAX_POST_LENGTH
        tool_context.state["review_status"] = "fail"
        # Log
        logger.info(
            msg=f"Post is too long. Remove {char_excess} characters to meet the maximum length of {MAX_POST_LENGTH}."
        )
        return {
            "result": "fail",
            "char_count": char_count,
            "char_excess": char_excess,
            "message": f"Post is too long. Remove {char_excess} characters to meet the maximum length of {MAX_POST_LENGTH}.",
        }
    else:
        # Log
        logger.info(msg="Post length is within the required range.")
        return {
            "result": "pass",
            "char_count": len(post),
            "message": f"Post length {char_count} characters is within the required range.",
        }


def exit_loop(tool_context: ToolContext) -> dict[Any, Any]:
    """
    This function is called ONLY when the post meets all quality requirements,
    signaling the iterative process should end.

    Args:
        tool_context: Context for tool execution

    Returns:
        Empty dictionary
    """
    # Log
    logger.info(msg="---Executing exit_loop tool---")
    logger.info(
        msg="Post review completed successfully. Exiting the refinement loop now."
    )
    # Set escalate to True to stop the LoopAgent
    tool_context.actions.escalate = True

    # Set escalate to True in the state
    tool_context.state["escalate"] = True

    # Return empty dictionary
    return {}
