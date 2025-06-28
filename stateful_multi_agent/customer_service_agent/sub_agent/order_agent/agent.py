from typing import Any
from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from sub_agent.sales_agent.course_info import (
    COURSE_ID,
    COURSE_NAME,
    COURSE_PRICE,
    COURSE_DURATION,
)


# Get current time
def get_current_time() -> dict[str, str]:
    """Get the current time."""
    return {"current_time": datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")}


def refund_course(tool_context: ToolContext) -> dict[str, Any]:

    # Course information
    course_id = COURSE_ID
    course_name = COURSE_NAME
    course_price = COURSE_PRICE

    # Get current time
    current_time: str = get_current_time()["current_time"]

    # Get current purchased courses from state
    current_purchased_courses: Any = tool_context.state.get(
        key="purchased_courses", default=[]
    )

    # Check user owns the course
    courses_id: list[str] = [
        course["id"]
        for course in current_purchased_courses
        if isinstance(course, dict) and "id" in course
    ]
    if course_id not in courses_id:
        return {
            "status": "error",
            "message": f"You do not own the course '{course_name}'. So it cannot be refunded.",
        }

    # Refund and update purchased courses in state
    update_purchased_courses: list[dict[str, Any]] = []
    for course in current_purchased_courses:
        # skip empty or non-valid course entries
        if not course or not isinstance(course, dict):
            continue
        # skip the course to be refunded
        if course.get("id") == course_id:
            continue
        # add the rest of the courses
        update_purchased_courses.append(course)
    # Update state
    tool_context.state["purchased_courses"] = update_purchased_courses

    # Get and update current interaction history
    current_interaction_history: Any = tool_context.state.get(
        key="interaction_history", default=[]
    )
    current_interaction_history.append(
        {
            "action": "refund_course",
            "id": course_id,
            "timestamp": current_time,
        }
    )
    # Update interaction history in state
    tool_context.state["interaction_history"] = current_interaction_history

    return {
        "status": "success",
        "message": f"""Successfully refunded the '{course_name}' course. ! 
         Your ${course_price} will be returned to your original payment method within 3-5 business days.""",
        "id": course_id,
        "timestamp": current_time,
    }


# Create the order agent
order_agent = Agent(
    name="order_agent",
    model="gemini-2.0-flash",
    description="Order agent for viewing purchase history and processing refunds",
    instruction="""
    You are the order agent for the AI Developer Accelerator community.
    Your role is to help users view their purchase history, course access, and process refunds.

    <user_info>
    Name: {user_name}
    </user_info>

    <purchase_info>
    Purchased Courses: {purchased_courses}
    </purchase_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    When users ask about their purchases:
    1. Check their course list from the purchase info above
       - Course information is stored as objects with "id" and "purchase_date" properties
    2. Format the response clearly showing:
       - Which courses they own
       - When they were purchased (from the course.purchase_date property)

    When users request a refund:
    1. Verify they own the course they want to refund ("{course_name}")
    2. If they own it:
       - Use the refund_course tool to process the refund
       - Confirm the refund was successful
       - Remind them the money will be returned to their original payment method
       - If it's been more than 30 days, inform them that they are not eligible for a refund
    3. If they don't own it:
       - Inform them they don't own the course, so no refund is needed

    Course Information:
    - id: "{course_id}"
    - name: "{course_name}"
    - price: ${course_price}
    - duration: {course_duration} weeks

    Example Response for Purchase History:
    "Here are your purchased courses:
    1. AI Marketing Platform
       - Purchased on: 2024-04-21 10:30:00
       - Full lifetime access"

    Example Response for Refund:
    "I've processed your refund for the {COURSE_NAME} course.
    Your ${COURSE_PRICE} will be returned to your original payment method within 3-5 business days.
    The course has been removed from your account."

    If they haven't purchased any courses:
    - Let them know they don't have any courses yet
    - Suggest talking to the sales agent about the AI Marketing Platform course

    Remember:
    - Be clear and professional
    - Mention our 30-day money-back guarantee if relevant
    - Direct course questions to course support
    - Direct purchase inquiries to sales
    """,
    tools=[refund_course, get_current_time],
)
