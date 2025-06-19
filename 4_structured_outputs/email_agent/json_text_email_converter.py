import json
from typing import Dict


def convert_email_json_to_text(email_json: Dict[str, str]) -> str:
    """
    Converts an email represented as a JSON object (dictionary) into a
    plain text string format.

    Args:
        email_json: A dictionary with "subject" and "body" keys,
                    representing the email content.

    Returns:
        A string formatted as a plain text email.
    """
    if not isinstance(email_json, dict):
        raise TypeError("Input must be a dictionary.")
    if "subject" not in email_json or "body" not in email_json:
        raise ValueError("Input dictionary must contain 'subject' and 'body' keys.")

    subject: str = email_json.get("subject", "")
    body: str = email_json.get("body", "")

    # Convert escaped newlines to actual newlines
    body = body.replace("\\n", "\n")

    return f"Subject: {subject}\n\n{body}"


if __name__ == "__main__":

    # Example usage with the provided JSON:
    email_data_json_string = """
    {
    "subject": "Project [Project Name] Deadline Extended",
    "body": "Dear Team,\\n\\nI am writing to inform you of an update regarding the deadline for Project [Project Name]. After careful consideration, we have decided to extend the deadline by two weeks.\\n\\nThe new deadline is now [New Deadline Date]. This extension is to ensure that everyone has sufficient time to complete their tasks thoroughly and to maintain the high quality of work we strive for.\\n\\nPlease adjust your schedules accordingly. If you foresee any challenges with the new deadline, please let me know as soon as possible so we can address them proactively.\\n\\nThank you for your continued hard work and dedication to this project.\\n\\nBest regards,\\n[Your Name]"
    }
    """
    print(f"\n{email_data_json_string}")

    # Convert the JSON string to a Python dictionary
    email_data_dict = json.loads(email_data_json_string)

    # Convert the dictionary to plain text email format
    plain_text_email: str = convert_email_json_to_text(email_json=email_data_dict)

    # Print the result
    print(f"\n{plain_text_email}")

    print("\n--- Another Example ---")

    # Example with a slightly different email to show flexibility
    another_email_data: Dict[str, str] = {
        "subject": "Quick Question",
        "body": "Hi there,\n\nJust wanted to ask a quick question about the report.\n\nThanks,\nAlex",
    }
    print(f"\n{another_email_data}")

    plain_text_another_email: str = convert_email_json_to_text(
        email_json=another_email_data
    )
    print(f"\n{plain_text_another_email}")
