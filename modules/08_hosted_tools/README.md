# Module 08: Hosted Tools

## Learning Objectives
- Use Azure-hosted tools: Code Interpreter, File Search, Web Search
- Understand the difference between local function tools and hosted tools
- Combine hosted tools with function tools

## Key Concepts
- **`HostedCodeInterpreterTool()`** - Execute Python code on Azure
- **`HostedFileSearchTool()`** - Search through vector stores
- **`HostedWebSearchTool(name="Bing")`** - Bing web search
- **Requires** `AzureAIAgentsProvider` (not AzureOpenAIChatClient)

## Exercises
1. Create an agent with Code Interpreter to solve math problems
2. Create an agent with Web Search for real-time information
3. Combine Code Interpreter + Web Search + custom functions

## Files
- `main.py` - Hosted tools examples (requires Azure AI Foundry)
