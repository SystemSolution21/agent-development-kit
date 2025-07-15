"""
Disk Information Tools

This module contains tools for collecting disk information and structured it to be used by the agent.
"""

import time
from typing import Any

import psutil


def get_disk_info() -> dict[str, Any]:
    """
    Collect disk information including partitions and usage.
    Returns:
        dict[str, Any]:
    """
    try:
        # Get disk information
        disk_info: dict[str, Any] = {"partitions": []}
        partitions_over_threshold: list[str] = []
        total_space = 0
        used_space = 0

        for partition in psutil.disk_partitions():
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)

                # Track high usage partition
                if partition_usage.percent > 85:
                    partitions_over_threshold.append(
                        f"{partition.mountpoint} ({partition_usage.percent:.1f}%)"
                    )

                # Calculate total and used space
                total_space += partition_usage.total
                used_space += partition_usage.used

                disk_info["partitions"].append(
                    {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "filesystem_type": partition.fstype,
                        "total_size": f"{partition_usage.total / (1024**3):.2f} GB",
                        "used_size": f"{partition_usage.used / (1024**3):.2f} GB",
                        "free_size": f"{partition_usage.free / (1024**3):.2f} GB",
                        "usage_percent": f"{partition_usage.percent:.1f}%",
                    }
                )
            except (PermissionError, FileNotFoundError):
                # Some partitions may not be accessible
                pass

        # Calculate disk overall usage percent
        overall_usage_percent = (
            (used_space / total_space) * 100 if total_space > 0 else 0
        )

        # Format for ADK tool response
        return {
            "result": disk_info,
            "stats": {
                "partition_count": len(disk_info["partitions"]),
                "total_space_bg": f"{total_space / (1024**3):.2f} GB",
                "used_space_bg": f"{used_space / (1024**3):.2f} GB",
                "overall_usage_percent": overall_usage_percent,
                "partitions_with_high_usage": len(partitions_over_threshold),
            },
            "additional_info": {
                "data_structure": "dictionary",
                "collection_timestamp": time.time(),
                "high_usage_partitions": partitions_over_threshold
                if partitions_over_threshold
                else None,
            },
        }

    except Exception as e:
        return {
            "result": {"error": f"failed to get disk information: {str(object=e)}"},
            "stats": {"success": False},
            "additional_info": {"error_type": str(object=type(e).__name__)},
        }
