# 20 – Declarative Agents

!!! abstract "Module Goals"
    Define agents in YAML instead of Python — separate configuration from code.

## Key Concepts

| Concept | Description |
|---------|-------------|
| YAML definition | Agent config as data |
| `agent.yaml` | Declarative agent file |
| Tool references | Register tools by name |
| Environment binding | Inject config at runtime |

## Example YAML

```yaml
name: TravelAgent
instructions: "You are a travel planning assistant..."
model: gpt-4o
tools:
  - search_flights
  - search_hotels
```

## Code

```python title="modules/20_declarative_agents/main.py"
--8<-- "modules/20_declarative_agents/main.py"
```

## Run It

```bash
uv run python modules/20_declarative_agents/main.py
```

## Exercises

- [ ] Define an agent entirely in YAML
- [ ] Load multiple agent definitions from files
- [ ] Create a YAML-defined multi-agent system

!!! tip "Next"
    [21 – Agent-to-Agent (A2A)](21-agent-to-agent.md)
