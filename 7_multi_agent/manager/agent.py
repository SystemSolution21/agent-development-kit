from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .specialist.funny_nerd.agent import funny_nerd
from .specialist.news_analyst.agent import news_analyst
from .specialist.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time

# Create the root agent
root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="A manager agent that can manage other agents.",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agent:
    - stock_analyst
    - funny_nerd

    You also have access to the following tools:
    - news_analyst
    - get_current_time
    """,
    sub_agents=[funny_nerd, stock_analyst],
    tools=[
        AgentTool(agent=news_analyst),
        get_current_time,
    ],
)
