"""Purchase tools for the agent config system."""

from datetime import datetime
from typing import Any

from config.app_config_loader import load_app_config
from google.adk.tools.tool_context import ToolContext

# Load configuration
_app_config = load_app_config()
_course_config = _app_config.courses["ai_marketing_platform"]

# Course constants from config
COURSE_ID = _course_config["id"]
COURSE_NAME = _course_config["name"]
COURSE_PRICE = _course_config["price"]
REFUND_POLICY_DAYS = _course_config["refund_policy_days"]


def get_current_time() -> str:
    """Get current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def purchase_course(tool_context: ToolContext) -> dict[str, Any]:
    """
    Simulates purchasing the AI Marketing Platform course.
    Updates state with purchase information.

    Args:
        tool_context: Context for accessing and updating session state

    Returns:
        Dictionary with purchase status and details
    """
    # Get current time
    current_time = get_current_time()

    # Get current purchased courses from state
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Check if user already owns the course
    courses_id = [
        course["id"]
        for course in current_purchased_courses
        if isinstance(course, dict) and "id" in course
    ]

    if COURSE_ID in courses_id:
        return {
            "status": "error",
            "message": f"You already own the {COURSE_NAME} course.",
        }

    # Create new course purchase entry
    new_course = {
        "id": COURSE_ID,
        "name": COURSE_NAME,
        "price": COURSE_PRICE,
        "purchase_date": current_time,
    }

    # Add the new course to purchased courses
    updated_courses = []
    for course in current_purchased_courses:
        if isinstance(course, dict) and "id" in course:
            updated_courses.append(course)

    updated_courses.append(new_course)

    # Update state with new purchase
    tool_context.state["purchased_courses"] = updated_courses

    # Add purchase to interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    current_interaction_history.append(
        {
            "action": "purchase_course",
            "course_id": COURSE_ID,
            "course_name": COURSE_NAME,
            "price": COURSE_PRICE,
            "timestamp": current_time,
        }
    )
    tool_context.state["interaction_history"] = current_interaction_history

    return {
        "status": "success",
        "message": f"🎉 Congratulations! You have successfully purchased the {COURSE_NAME} course for ${COURSE_PRICE}!",
        "course_id": COURSE_ID,
        "course_name": COURSE_NAME,
        "price": COURSE_PRICE,
        "purchase_date": current_time,
        "access_info": "You now have immediate access to all course materials and weekly coaching calls.",
    }


def refund_course(tool_context: ToolContext) -> dict[str, Any]:
    """
    Simulates refunding the AI Marketing Platform course.
    Updates state by removing the course from purchased_courses.

    Args:
        tool_context: Context for accessing and updating session state

    Returns:
        Dictionary with refund status and details
    """
    # Get current time
    current_time = get_current_time()

    # Get current purchased courses from state
    current_purchased_courses = tool_context.state.get("purchased_courses", [])

    # Check if user owns the course
    course_found = False
    purchase_date = None
    for course in current_purchased_courses:
        if isinstance(course, dict) and course.get("id") == COURSE_ID:
            course_found = True
            purchase_date = course.get("purchase_date")
            break

    if not course_found:
        return {
            "status": "error",
            "message": f"You don't own the {COURSE_NAME} course, so it cannot be refunded.",
        }

    # Check if within refund window (30 days)
    if purchase_date:
        try:
            purchase_datetime = datetime.strptime(purchase_date, "%Y-%m-%d %H:%M:%S")
            current_datetime = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
            days_since_purchase = (current_datetime - purchase_datetime).days

            if days_since_purchase > REFUND_POLICY_DAYS:
                return {
                    "status": "error",
                    "message": f"The refund window has expired. You purchased the course {days_since_purchase} days ago, but our refund policy only allows refunds within {REFUND_POLICY_DAYS} days of purchase.",
                }
        except ValueError:
            # If date parsing fails, allow the refund for demo purposes
            pass

    # Remove the course from purchased courses
    updated_courses = [
        course
        for course in current_purchased_courses
        if not (isinstance(course, dict) and course.get("id") == COURSE_ID)
    ]
    tool_context.state["purchased_courses"] = updated_courses

    # Add refund to interaction history
    current_interaction_history = tool_context.state.get("interaction_history", [])
    current_interaction_history.append(
        {
            "action": "refund_course",
            "course_id": COURSE_ID,
            "course_name": COURSE_NAME,
            "price": COURSE_PRICE,
            "timestamp": current_time,
        }
    )
    tool_context.state["interaction_history"] = current_interaction_history

    return {
        "status": "success",
        "message": f"✅ You have successfully refunded the {COURSE_NAME} course. Your ${COURSE_PRICE} will be returned to your original payment method within 5-7 business days.",
        "course_id": COURSE_ID,
        "course_name": COURSE_NAME,
        "refund_amount": COURSE_PRICE,
        "processing_time": "5-7 business days",
        "timestamp": current_time,
    }


def demo_purchase_link(tool_context: ToolContext) -> dict[str, Any]:
    """
    Provides a demo purchase link that actually triggers the purchase.
    This is for demonstration purposes.

    Args:
        tool_context: Context for accessing and updating session state

    Returns:
        Dictionary with demo link information
    """
    return {
        "status": "demo_link",
        "message": "🔗 Demo Purchase Link: Type 'PURCHASE_NOW' to simulate completing the purchase",
        "instructions": "In a real system, this would be a Stripe checkout link or similar payment processor.",
        "course_name": COURSE_NAME,
        "price": COURSE_PRICE,
    }
