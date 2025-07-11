import copy
import logging
from logging import Logger
from typing import Any, Optional

from google.adk.agents import LlmAgent
from google.adk.tools import BaseTool, ToolContext

from utils.logger import AdkLogger

# Initialize logger
logger: Logger = AdkLogger.get_logger(module_name=__name__, level=logging.INFO)


# --- Define Tools ---
def get_capital_city(country: str) -> dict[str, str]:
    """Get the capital city of a given country.

    Args:
        country: The name of the country

    Returns:
        A dictionary containing the capital city result
    """

    # Log the tool call
    logger.info(msg=f"[TOOL] Executing get_capital_city tool with country({country})")

    # Map countries with their capital cities
    country_capital: dict[str, str] = {
        "united states": "Washington, D.C.",
        "usa": "Washington, D.C.",
        "france": "Paris",
        "germany": "Berlin",
        "italy": "Rome",
        "spain": "Madrid",
        "japan": "Tokyo",
        "china": "Beijing",
        "india": "New Delhi",
        "brazil": "Brasilia",
        "australia": "Canberra",
        "canada": "Ottawa",
    }

    result: str = country_capital.get(
        country.lower(), f"No capital city found for {country}"
    )
    logger.info(f"[TOOL] get_capital_city tool returning result: {result}")
    return {"result": result}


# --- Define Before Tool Callbacks ---
def before_tool_callback(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> Optional[dict]:
    tool_name: str = tool.name
    logger.info(msg="===== Tool Execution Started =====")
    logger.info(
        msg=f"[BEFORE TOOL CALLBACK] Executing tool {tool_name} with args: {args}"
    )

    if tool_name == "get_capital_city" and args.get("country", "").lower() == "merica":
        logger.info(msg="[BEFORE TOOL CALLBACK] Converting 'merica' to 'United States'")
        args["country"] = "United States"
        logger.info(msg=f"[BEFORE TOOL CALLBACK] Modified arguments: {args}")
        return None

    if (
        tool_name == "get_capital_city"
        and args.get("country", "").lower() == "restricted"
    ):
        logger.info(
            msg="[BEFORE TOOL CALLBACK] Blocking request for restricted country"
        )
        return {"result": "Access to this information is restricted"}

    logger.info(f"[BEFORE TOOL CALLBACK] Proceeding with the tool {tool_name}")
    return None


# --- Define After Tool Callbacks ---
def after_tool_callback(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict
) -> Optional[dict]:
    tool_name: str = tool.name
    logger.info(
        msg=f"[AFTER TOOL CALLBACK] Executed tool {tool_name} with args: {args}"
    )
    logger.info(msg=f"[AFTER TOOL CALLBACK] Tool response: {tool_response}")

    # Check for USA capital city
    original_response: str = tool_response["result"].lower()
    if tool_name == "get_capital_city" and "washington" in original_response:
        logger.info(
            msg="[AFTER TOOL CALLBACK] DETECTED USA CAPITAL. adding patriotic notes!"
        )
        # Create modified response
        modified_response: dict[str, Any] = copy.deepcopy(tool_response)
        modified_response["result"] = (
            f"{original_response}. (Note: It is the capital of the United States of America.)"
        )
        modified_response["note_added_by_callback"] = True
        logger.info(msg=f"[AFTER TOOL CALLBACK] Modified response: {modified_response}")
        return modified_response

    logger.info(msg="[AFTER TOOL CALLBACK] No modifications made to response")
    return tool_response


# Create Agent
root_agent = LlmAgent(
    name="before_after_tool",
    model="gemini-2.0-flash",
    description="An agent that demonstrates tool callbacks by looking up capital cities",
    instruction="""
    You are a helpful geography assistant.

    Your job is to:
    - Find capital cities when asked using the get_capital_city tool
    - Use the exact country name provided by the user
    - ALWAYS call the get_capital_city tool for any country name provided by the user, even if the country is not recognized.
    - ALWAYS return the EXACT result from the tool, without changing it.
    - When reporting a capital, display it EXACTLY as returned by the tool

    Examples:
    - "What is the capital of France?" → Use get_capital_city with country="France"
    - "Tell me the capital city of Japan" → Use get_capital_city with country="Japan"
    """,
    tools=[get_capital_city],
    before_tool_callback=before_tool_callback,
    after_tool_callback=after_tool_callback,
)
