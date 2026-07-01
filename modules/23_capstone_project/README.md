# Module 23: Capstone Project

## 🎓 Capstone: Multi-Agent Enterprise Assistant

Build a complete end-to-end multi-agent application that combines everything you've learned.

## Project: Enterprise Knowledge Assistant

An intelligent assistant that:
1. **Triages** user requests (support, research, code help)
2. **Routes** to specialist agents via handoff workflow
3. **Uses tools** (function tools + hosted tools)
4. **Streams** responses in real-time
5. **Logs** everything via observability middleware
6. **Persists** conversations via threads
7. **Returns** structured outputs for analytics

## Architecture
```
                      ┌→ ResearchAgent (WebSearch + CodeInterpreter)
User → Triage Agent ──┤→ CodeAssistant (FunctionTools + Streaming) 
                      └→ SupportAgent  (Structured Outputs + Threads)
                              ↓
                      ObservabilityMiddleware → MetricsCollector
                              ↓
                      Final ResponseFormatter
```

## Requirements
- All 4 provider types (AzureOpenAI, AzureAIAgents)
- At least 3 specialist agents
- Function tools + Hosted tools
- Sequential + Handoff workflow patterns
- Agent-as-Tool for delegation
- Middleware pipeline (logging + security)
- Streaming responses
- Structured outputs
- Conversation threads
- Error handling

## Exercises
1. Design the architecture
2. Implement agent definitions
3. Build the workflow
4. Add middleware pipeline
5. Test end-to-end
6. Add monitoring and metrics

## Files
- `main.py` - Complete capstone application
- `agents.py` - Agent definitions
- `tools.py` - Custom function tools
- `middleware.py` - Middleware pipeline
- `models.py` - Pydantic models for structured outputs
