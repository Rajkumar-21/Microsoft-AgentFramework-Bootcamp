# Module 02: Hello Agent

## Learning Objectives
- Create your first ChatAgent with AzureOpenAIChatClient
- Understand the agent lifecycle: create → run → get response
- Learn basic agent instructions (system prompt)
- Run a simple single-turn conversation

## Key Concepts
- **`AzureOpenAIChatClient`** - Provider connecting to Azure OpenAI
- **`ChatAgent`** - Core agent abstraction
- **`create_agent(name, instructions)`** - Agent factory method
- **`agent.run(message)`** - Execute agent with a user message
- **`result.text`** - Extract response text

## Exercises
1. Create a basic "Hello World" agent
2. Experiment with different `instructions` (system prompts)
3. Create agents with different personalities
4. Print the full result object to understand its structure

## Files
- `main.py` - Basic Hello Agent example
