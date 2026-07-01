# Module 02: Hello Agent

> **Scenario — Contoso Financial Expense Policy Assistant.** Your first agent answers
> employees from a fixed expense policy: grounded in explicit rules, bounded by a cap,
> and honest when a question falls outside policy.

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

## How to Run
```bash
cd modules/02_hello_agent
python main.py
```

## Files
- `main.py` - Grounded expense-policy assistant (single-turn)
