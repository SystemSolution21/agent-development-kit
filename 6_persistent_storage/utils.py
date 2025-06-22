from google.genai import types


# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


async def display_state(
    session_service, app_name, user_id, session_id, label="Current State"
) -> None:
    """Display the current state of the session in a formatted way."""
    try:
        session = await session_service.get_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
        )

        # Format the output with clear sections
        print(f"\n{'-' * 10} {label} {'-' * 10}")

        # Handle user name
        user_name = session.state.get("user_name", "Unknown")
        print(f"👤 User: {user_name}")

        # Handle reminders
        reminders = session.state.get("reminders", [])
        if reminders:
            print("📋Reminders:")
            for idx, reminder in enumerate(reminders, start=1):
                print(f"  {idx}. {reminder}")
        else:
            print("📋 No reminders found.")

        print("-" * (22 + len(label)))

    except Exception as e:
        print(f"Error displaying session state: {e}")


async def process_agent_response(event):
    """Process and display the agent response event."""
    # Log basic event info
    print(f"Event ID: {event.id}, Author: {event.author}")

    # Check specific event content parts
    has_specific_part = False
    if event.content and event.content.parts:
        # First, check if there are any function_call parts
        function_calls = []
        for part in event.content.parts:
            if hasattr(part, "function_call") and part.function_call:
                function_calls.append(part.function_call)

        # Process all parts
        for part in event.content.parts:
            if hasattr(part, "executable_code") and part.executable_code:
                # Access the actual code string via .code
                print(
                    f"  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```"
                )
                has_specific_part = True
            elif hasattr(part, "code_execution_result") and part.code_execution_result:
                # Access outcome and output correctly
                print(
                    f"  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}"
                )
                has_specific_part = True
            elif hasattr(part, "tool_response") and part.tool_response:
                # Print tool response information
                print(f"  Tool Response: {part.tool_response.output}")
                has_specific_part = True
            elif hasattr(part, "function_call") and part.function_call:
                # Handle function call parts
                print(
                    f"  Function Call: {part.function_call.name} with args: {part.function_call.args}"
                )
                has_specific_part = True
            # Also print any text parts found in any event for debugging
            elif hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"  Text: '{part.text.strip()}'")

    # Check final response
    final_response = None
    if event.is_final_response():
        # Extract text from final response if available
        if event.content and event.content.parts:
            text_parts = []
            for part in event.content.parts:
                if hasattr(part, "text") and part.text and not part.text.isspace():
                    text_parts.append(part.text.strip())

            if text_parts:
                final_response = " ".join(text_parts)

        if final_response:
            # Use colors and formatting to make the final response stand out
            print(
                f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ AGENT RESPONSE ═════════════════════════════════════════{Colors.RESET}"
            )
            print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
            print(
                f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n"
            )
        else:
            print(
                f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> Final Agent Response: [No text content in final event]{Colors.RESET}\n"
            )
    else:
        # For non-final events, don't print the fancy box
        pass

    return final_response


async def call_agent_async(runner, user_id, session_id, query):
    """Call the agent synchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(
        f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Running Query: {query} ---{Colors.RESET}"
    )

    final_response_text = None

    # Display state before processing the query
    await display_state(
        session_service=runner.session_service,
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
        label="State Before Processing",
    )

    # Process event and get final response
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content,
        ):
            response = await process_agent_response(event=event)
            if response:
                final_response_text = response
    except Exception as e:
        print(f"Error running agent: {e}")

    # Display state after processing the query
    await display_state(
        session_service=runner.session_service,
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
        label="State After Processing",
    )

    return final_response_text
