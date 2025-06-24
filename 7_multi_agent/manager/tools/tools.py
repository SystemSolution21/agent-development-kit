from datetime import datetime


def get_current_time() -> dict:
    """Get the current time."""
    return {"current_time": datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")}
