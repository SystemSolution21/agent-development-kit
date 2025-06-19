from dotenv import load_dotenv

from pydantic import BaseModel, Field
from google.adk.agents import Agent

# Load environment variables from .env file
load_dotenv()


# Define the structure of the email content with text output
class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    body: str = Field(
        description="The main content of the email. Should be well-formatted with the proper greeting, paragraphs and signature."
    )


# Create the agent with output_schema
root_agent = Agent(
    name="email_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an Email Generation Assistant.
        Your task is to generate a professional email based on the user's request.

        GUIDELINES:
        - Create an appropriate subject line (concise and relevant)
        - Write a well-structured email body with:
            * Professional greeting
            * Clear and concise main content
            * Appropriate closing
            * Your name as signature
        - Email tone should match the purpose (formal for business, friendly for colleagues)
        - Keep emails concise but complete
        - Use proper line breaks (\\n) in the email body for formatting
    """,
    description="Generates professional emails and formats them as plain text.",
    output_schema=EmailContent,
    output_key="email",
)
