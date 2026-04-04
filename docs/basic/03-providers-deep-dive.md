# 03 – Providers Deep Dive

!!! abstract "Module Goals"
    Understand the three main providers, when to use each, and the difference between client-side and server-side agents.

## Provider Comparison

| Provider | Type | Persistence | Hosted Tools | Auth |
|----------|------|:-----------:|:------------:|------|
| `AzureOpenAIChatClient` | Client-side | :x: | :x: | API Key |
| `OpenAIChatClient` | Client-side | :x: | :x: | API Key |
| `AzureAIAgentsProvider` | Server-side | :white_check_mark: | :white_check_mark: | Azure Identity |

!!! info "When to use which?"
    - **AzureOpenAIChatClient** — Simple agents, quick prototyping, function tools only
    - **AzureAIAgentsProvider** — Production agents, hosted tools, persistent threads

## Code: AzureOpenAIChatClient

```python title="modules/03_providers_deep_dive/azure_openai_provider.py"
--8<-- "modules/03_providers_deep_dive/azure_openai_provider.py"
```

## Code: AzureAIAgentsProvider

```python title="modules/03_providers_deep_dive/azure_ai_provider.py"
--8<-- "modules/03_providers_deep_dive/azure_ai_provider.py"
```

!!! warning "Context Managers"
    `AzureAIAgentsProvider` **must** be used with `async with` for proper resource cleanup.

## Run It

```bash
uv run python modules/03_providers_deep_dive/azure_openai_provider.py
uv run python modules/03_providers_deep_dive/azure_ai_provider.py
```

## Exercises

- [ ] Create agents with both providers
- [ ] Compare response behavior between providers
- [ ] Try different model deployments

!!! tip "Next"
    [04 – Function Tools](04-function-tools.md)
