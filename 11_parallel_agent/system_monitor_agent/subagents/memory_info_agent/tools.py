import time
from typing import Any

import psutil


def get_memory_info() -> dict[str, Any]:
    """
    Collect memory information including total, available, and usage statistics.
    Returns:
        dict[str, Any]:
            A dictionary containing memory information.
    """
    try:
        # Get memory information
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()

        memory_info = {
            "total_memory": f"{memory.total / (1024**3):.2f} GB",
            "available_memory": f"{memory.available / (1024**3):.2f} GB",
            "used_memory": f"{memory.used / (1024**3):.2f} GB",
            "memory_percent_used": f"{memory.percent:.1f}%",
            "swap_total": f"{swap.total / (1024**3):.2f} GB",
            "swap_used": f"{swap.used / (1024**3):.2f} GB",
            "swap_percent_used": f"{swap.percent:.1f}%",
        }

        # Calculate Stats
        memory_usage: float = memory.percent
        swap_usage: float = swap.percent
        high_memory_usage: bool = memory_usage > 80
        high_swap_usage: bool = swap_usage > 80

        # Format for ADK tool response
        return {
            "result": memory_info,
            "stats": {
                "memory_usage_percent": memory_usage,
                "swap_usage_percent": swap_usage,
                "total_memory_gb": memory.total / (1024**3),
                "available_memory_gb": memory.available / (1024**3),
            },
            "additional_info": {
                "data_structure": "dictionary",
                "collection_timestamp": time.time(),
                "performance_concerns": "High memory usage detected"
                if high_memory_usage or high_swap_usage
                else None,
            },
        }

    except Exception as e:
        return {
            "result": {"error": f"failed to get memory information: {str(object=e)} "},
            "stats": {"success": False},
            "additional_info": {"error_type": str(object=type(e).__name__)},
        }
