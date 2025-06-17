# Agent-Development-Kit (ADK)

This repository contains examples for learning Google's Agent Development Kit (ADK), a powerful framework for building LLM-powered agents.

## Getting Started

### Setup Environment

Create virtual environment.

```bash
# Create virtual environment in the root directory (agent-development-kit)
uv init
uv venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate

# Install dependencies
uv add <PackageName>
```

### Setting Up API Keys

1. Create an account in Google Cloud <https://cloud.google.com/?hl=en>
2. Create a new project
3. Go to <https://aistudio.google.com/apikey>
4. Create an API key
5. Assign key to the project
6. Connect to a billing account
7. Add the API key to the .env file for each Agent folder

   ```
   GOOGLE_API_KEY=
   ```

## Examples Overview

Each example is designed to build upon the previous one, gradually introducing more complex concepts.

### 1. Basic Agent

Simplest form of ADK agents. Create a basic agent that can respond to user queries.

### 2. Tool Agent

Enhance agents with tools that allow them to perform actions beyond just generating text.

### 3. LiteLLM Agent

LiteLLM to abstract away LLM provider details and easily switch between different models.

### 4. Structured Outputs

Pydantic models with `output_schema` to ensure consistent, structured responses from agents.

### 5. Sessions and State

Maintain state and memory across multiple interactions using sessions.

### 6. Persistent Storage

Storing agent data persistently across sessions and application restarts.

### 7. Multi-Agent

Orchestrate multiple specialized agents working together to solve complex tasks.

### 8. Stateful Multi-Agent

Build agents that maintain and update state throughout complex multi-turn conversations.

### 9. Callbacks

Implement event callbacks to monitor and respond to agent behaviors in real-time.

### 10. Sequential Agent

Create pipeline workflows where agents operate in a defined sequence to process information.

### 11. Parallel Agent

Leverage concurrent operations with parallel agents for improved efficiency and performance.

### 12. Loop Agent

Build sophisticated agents that can iteratively refine their outputs through feedback loops.

## Official Documentation

For more detailed information, check out the official ADK documentation:

- <https://google.github.io/adk-docs/get-started/quickstart>
