import importlib
from typing import Callable

# Import tools
from .purchase_tools import demo_purchase_link, purchase_course, refund_course

# Registry of available tools
_TOOL_REGISTRY = {
    "purchase_course": purchase_course,
    "demo_purchase_link": demo_purchase_link,
    "refund_course": refund_course,
}


def register_tool(tool_id: str, tool_fn: Callable) -> None:
    """Register a tool function with the registry.

    Args:
        tool_id: Unique identifier for the tool
        tool_fn: The tool function
    """
    _TOOL_REGISTRY[tool_id] = tool_fn


def get_tool_by_id(tool_id: str) -> Callable:
    """Get a tool function by its identifier.

    Args:
        tool_id: Identifier for the tool

    Returns:
        The tool function

    Raises:
        KeyError: If tool_id is not registered
    """
    if tool_id not in _TOOL_REGISTRY:
        # Try to dynamically import the tool
        module_path, function_name = tool_id.rsplit(".", 1)
        try:
            module = importlib.import_module(module_path)
            tool_fn = getattr(module, function_name)
            register_tool(tool_id, tool_fn)
            return tool_fn
        except (ImportError, AttributeError) as e:
            raise KeyError(f"Tool not found: {tool_id}") from e

    return _TOOL_REGISTRY[tool_id]
