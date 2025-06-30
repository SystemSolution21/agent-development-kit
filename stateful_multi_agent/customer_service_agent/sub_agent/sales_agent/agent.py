from typing import Any
from datetime import datetime

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from .course_info import COURSE_ID, COURSE_NAME


# Get current time
def get_current_time() -> dict[str, str]:
    """Get the current time."""
    return {"current_time": datetime.now().strftime(format="%Y-%m-%d %H:%M:%S")}


def purchase_course(tool_context: ToolContext) -> dict[str, Any]:
    """
    Simulates purchasing the AI Marketing Platform course.
    Updates state with purchase information.
    """
    # Get current time
    current_time: str = get_current_time()["current_time"]

    # Get current purchased courses from state
    current_purchased_courses: Any = tool_context.state.get(
        key="purchased_courses", default=[]
    )

    # Check user owns the course
    courses_id: list[str] = [
        course["id"] for course in current_purchased_courses if isinstance(course, dict)
    ]
    if COURSE_ID in courses_id:
        return {
            "status": "error",
            "message": f"You already own the {COURSE_NAME} course.",
        }

    # Create,add and update the new course purchase in state
    new_purchased_course: list[dict[str, Any]] = []
    for course in current_purchased_courses:
        if isinstance(course, dict) and "id" in course:
            new_purchased_course.append(course)
    # Add the new course
    new_purchased_course.append({"id": COURSE_ID, "purchase_date": current_time})
    # Update state
    tool_context.state["purchased_courses"] = new_purchased_course

    # Get and update current interaction history
    current_interaction_history: Any = tool_context.state.get(
        key="interaction_history", default=[]
    )
    current_interaction_history.append(
        {
            "action": "purchase_course",
            "id": COURSE_ID,
            "timestamp": current_time,
        }
    )
    tool_context.state["interaction_history"] = current_interaction_history

    return {
        "status": "success",
        "message": f"You have successfully purchased the course {COURSE_NAME}!",
        "id": COURSE_ID,
        "timestamp": current_time,
    }


# Create the sales agent
sales_agent = Agent(
    name="sales_agent",
    model="gemini-2.0-flash",
    description="Sales agent for the AI Marketing Platform course",
    instruction="""
    You are a sales agent for the AI Developer Accelerator community, specifically handling sales
    for the AI Marketing Platform course.

    <user_info>
    Name: {user_name}
    </user_info>

    <purchase_info>
    Purchased Courses: {purchased_courses}
    </purchase_info>

    <interaction_history>
    {interaction_history}
    </interaction_history>

    Course Details:
    - Name: AI Marketing Platform
    - Price: $149
    - Duration: 6 weeks of content, self-paced learning
    - Value Proposition: Learn to build AI-powered marketing automation apps
    - Includes: 6 weeks of group support with weekly coaching calls

    When users ask about pricing or duration:
    - The course costs $149 (one-time payment, not a subscription)
    - The course content takes approximately 6 weeks to complete at a comfortable pace
    - Users have lifetime access to the content
    - The course includes 6 weeks of group support with weekly coaching calls

    When interacting with users:
    1. Check if they already own the course (check purchased_courses above)
       - Course information is stored as objects with "id" and "purchase_date" properties
       - The course id is "ai_marketing_platform"
    2. If they own it:
       - Remind them they have access
       - Ask if they need help with any specific part
       - Direct them to course support for content questions
    
    3. If they don't own it:
       - Explain the course value proposition
       - Mention the price ($149) and duration (6 weeks)
       - If they want to purchase:
           - Use the purchase_course tool
           - Confirm the purchase
           - Ask if they'd like to start learning right away

    4. After any interaction:
       - The state will automatically track the interaction
       - Be ready to hand off to course support after purchase
    """,
    tools=[purchase_course],
)
