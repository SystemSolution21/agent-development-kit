# Agent Instruction and Configuration Management System

This system provides a clean, modular approach to managing agent instructions and configurations for multi-agent systems built with Google's Agent Development Kit (ADK).

## Key Features

- **Separation of Concerns**: Cleanly separates agent logic, configuration, and instructions
- **Template-Based Instructions**: Uses Jinja2 templates for flexible, modular instructions
- **Environment-Specific Configuration**: Supports different configurations for development, staging, and production
- **Dynamic Agent Creation**: Creates agents and sub-agents on demand from configuration
- **Instruction Composition**: Builds instructions from reusable components
- **Tool Registry**: Dynamically loads tools based on configuration

## Project Structure

```
multi_agent_config_system/
│
├── agent_config/                  # Core configuration management
│   ├── __init__.py
│   ├── config_manager.py          # Manages loading and rendering configurations
│   └── agent_factory.py           # Creates agent instances from configurations
│
├── config/                        # Configuration files
│   └── agents/                    # Agent-specific configurations
│       ├── customer_service.yaml  # Main agent configuration
│       ├── policy_agent.yaml
│       ├── sales_agent.yaml
│       └── ...
│
├── templates/                     # Instruction templates
│   ├── shared/                    # Shared template components
│   │   ├── user_context.j2        # User context section
│   │   └── professional_tone.j2   # Professional tone guidelines
│   │
│   ├── customer_service/          # Customer service agent templates
│   │   ├── main.j2                # Main instruction template
│   │   └── specialized_agents.j2  # Specialized agents section
│   │
│   └── ...                        # Other agent templates
│
├── tools/                         # Tool implementations
│   ├── __init__.py
│   └── registry.py                # Tool registry for dynamic loading
│
├── main.py                        # Application entry point
└── README.md                      # Documentation
```

## Usage

1. Define agent configurations in YAML files
2. Create instruction templates using Jinja2
3. Initialize the configuration manager and agent factory
4. Create agents using the factory
5. Use the agents with ADK runners

## Benefits

- **Maintainability**: Easy to update instructions without changing code
- **Reusability**: Share common instruction components across agents
- **Flexibility**: Support different configurations per environment
- **Scalability**: Add new agents without modifying existing code
- **Collaboration**: Enable non-technical team members to edit instructions

## Example

```python
# Initialize configuration system
config_manager = AgentConfigManager(
    config_dir="config/agents",
    template_dir="templates",
    environment="production"
)

# Initialize agent factory
agent_factory = AgentFactory(config_manager)

# Create the root agent with state variables
customer_service_agent = agent_factory.create_agent(
    "customer_service",
    state_variables={
        "user_name": "John Doe",
        "purchased_courses": []
    }
)
```
