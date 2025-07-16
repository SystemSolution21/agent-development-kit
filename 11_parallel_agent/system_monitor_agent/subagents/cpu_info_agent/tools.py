"""CPU Information Tools

This module contains tools for collecting and analyzing CPU information.
"""

import time
from typing import Any

import psutil


def get_cpu_info() -> dict[str, Any]:
    """
    Collect CPU information including core counts and usage statistics.
    Returns:
        dict[str, Any]:
            A dictionary containing CPU information.
    """
    try:
        # Get CPU information
        cpu_info: dict[str, Any] = {
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "cpu_usage_per_core": [
                f"Core {i}: {percent:.1f}%"
                for i, percent in enumerate(
                    iterable=psutil.cpu_percent(interval=1, percpu=True)
                )
            ],
            "avg_cpu_usage": f"{psutil.cpu_percent(interval=1):.1f}%",
        }

        # Get CPU usage statistics
        avg_usage: float = float(cpu_info["avg_cpu_usage"].strip("%"))
        high_usage: bool = avg_usage > 80

        # Format for ADK tool response
        return {
            "result": cpu_info,
            "stats": {
                "physical_cores": cpu_info["physical_cores"],
                "logical_cores": cpu_info["logical_cores"],
                "avg_usage_percent": avg_usage,
                "high_usage_alert": high_usage,
            },
            "additional_info": {
                "data_structure": "dictionary",
                "collection_timestamp": time.time(),
                "performance_concerns": "High CPU usage detected"
                if high_usage
                else None,
            },
        }

    except Exception as e:
        return {
            "result": {"error": f"failed to get CPU information: {str(object=e)} "},
            "stats": {"success": False},
            "additional_info": {"error_type": str(object=type(e).__name__)},
        }
