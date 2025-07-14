from google.adk.agents import LlmAgent

disk_info_agent = LlmAgent(
    name="DiskInfoAgent",
    model="gemini-2.0-flash",
)
