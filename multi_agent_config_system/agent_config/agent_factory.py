from typing import Dict, Any, List, Optional
from google.adk.agents import Agent

from .config_manager import AgentConfigManager

class AgentFactory:
    """Factory for creating agent instances from configurations."""
    
    def __init__(self, config_manager: AgentConfigManager):
        """Initialize the agent factory.
        
        Args:
            config_manager: The configuration manager to use
        """
        self.config_manager = config_manager
        self.agent_cache = {}  # Cache for created agents
        
    def create_agent(self, agent_id: str, state_variables: Optional[Dict[str, Any]] = None) -> Agent:
        """Create an agent instance from configuration.
        
        Args:
            agent_id: Identifier for the agent
            state_variables: Variables from the session state to include in rendering
            
        Returns:
            Configured Agent instance
        """
        # Check if we've already created this agent
        if agent_id in self.agent_cache:
            return self.agent_cache[agent_id]
            
        # Load the agent configuration
        config = self.config_manager.load_agent_config(agent_id)
        
        # Get the rendered instruction
        instruction = self.config_manager.get_agent_instruction(agent_id, state_variables)
        
        # Create sub-agents if needed
        sub_agents = []
        if "sub_agents" in config:
            for sub_agent_id in config["sub_agents"]:
                sub_agent = self.create_agent(sub_agent_id, state_variables)
                sub_agents.append(sub_agent)
        
        # Create tools if needed
        tools = self._load_tools(config.get("tools", []))
        
        # Create the agent
        agent = Agent(
            name=config["name"],
            model=config["model"],
            description=config["description"],
            instruction=instruction,
            sub_agents=sub_agents,
            tools=tools
        )
        
        # Cache the agent
        self.agent_cache[agent_id] = agent
        
        return agent
    
    def _load_tools(self, tool_ids: List[str]) -> List[Any]:
        """Load tools by their identifiers.
        
        Args:
            tool_ids: List of tool identifiers
            
        Returns:
            List of tool instances
        """
        # This is a simplified implementation
        # In a real system, you would load tools from a registry or factory
        from tools.registry import get_tool_by_id
        
        return [get_tool_by_id(tool_id) for tool_id in tool_ids]