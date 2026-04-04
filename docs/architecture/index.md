# Architecture

The Microsoft Agent Framework provides a layered, extensible architecture for building AI agent applications. This section contains detailed architecture diagrams and documentation.

!!! tip "Zoom any diagram"
    Click any diagram or Mermaid chart on this site to open it in a **fullscreen viewer** with zoom, pan, and drag support.

## Architecture Diagrams

<div class="grid cards" markdown>

-   :material-layers-outline:{ .lg .middle } **Core Architecture**

    ---

    Complete framework overview — User Layer → Providers → Agent Core → Tools → Workflows → Output.

    <div class="diagram-preview diagram-zoomable">
      <img src="diagrams/01-core-architecture.svg" alt="Core Architecture" loading="lazy">
    </div>

    [:octicons-download-16: Download .drawio](diagrams/01-core-architecture.drawio){ .md-button .md-button--primary }

-   :material-microsoft-azure:{ .lg .middle } **Azure Service Integration**

    ---

    Real-world multi-agent customer support system with Azure OpenAI, Cosmos DB, AI Search, Service Bus & more.

    <div class="diagram-preview diagram-zoomable">
      <img src="diagrams/02-azure-integration.svg" alt="Azure Service Integration" loading="lazy">
    </div>

    [:octicons-download-16: Download .drawio](diagrams/02-azure-integration.drawio){ .md-button .md-button--primary }

-   :material-arrow-decision-outline:{ .lg .middle } **Workflow Patterns**

    ---

    All 9 orchestration patterns: Sequential, Handoff, Concurrent, Supervisor, Agent-as-Tool, Sub-Workflows, HITL, A2A, Declarative.

    <div class="diagram-preview diagram-zoomable">
      <img src="diagrams/03-workflow-patterns.svg" alt="Workflow Patterns" loading="lazy">
    </div>

    [:octicons-download-16: Download .drawio](diagrams/03-workflow-patterns.drawio){ .md-button .md-button--primary }

-   :material-tools:{ .lg .middle } **Tools & MCP Ecosystem**

    ---

    Function Tools, Hosted Tools (Code Interpreter, Web Search), MCP Protocol flow, and the tool execution lifecycle.

    <div class="diagram-preview diagram-zoomable">
      <img src="diagrams/04-tools-mcp.svg" alt="Tools and MCP Ecosystem" loading="lazy">
    </div>

    [:octicons-download-16: Download .drawio](diagrams/04-tools-mcp.drawio){ .md-button .md-button--primary }

-   :material-cog-outline:{ .lg .middle } **Agent Internals & Components**

    ---

    Deep dive into ChatAgent internals — SystemMessage, RunContext, Tool Registry, Middleware Pipeline, Output Config, Providers, Streaming.

    <div class="diagram-preview diagram-zoomable">
      <img src="diagrams/05-agent-components.svg" alt="Agent Internals and Components" loading="lazy">
    </div>

    [:octicons-download-16: Download .drawio](diagrams/05-agent-components.drawio){ .md-button .md-button--primary }

</div>

---

## Framework Architecture Overview

```mermaid
graph TB
  subgraph UserLayer["👤 User Layer"]
    U[User / Application]
    Q[Natural Language Query]
  end

  subgraph Providers["☁️ Provider Layer"]
    AOAI[AzureOpenAI ChatClient]
    OAI[OpenAI ChatClient]
    AAP[AzureAIAgents Provider]
  end

  subgraph Agent["🤖 Core Agent Engine"]
    CA[ChatAgent]
    MW[Middleware Pipeline]
    TH[Conversation Threads]
    RH[Response Handler]
    MEM[Memory & Persistence]
  end

  subgraph Tools["🔧 Tools Ecosystem"]
    FT[Function Tools]
    HT[Hosted Tools]
    MT[MCP Tools]
    FS[File Search]
  end

  subgraph Workflows["🔀 Workflow Orchestration"]
    SEQ[Sequential]
    HO[Handoff]
    CON[Concurrent]
    SUP[Supervisor]
  end

  subgraph Output["📤 Output"]
    OT[Text]
    OP[Pydantic Model]
    OS[Streaming]
    OA[Agent-to-Agent]
  end

  U --> Q --> AOAI
  AOAI --> CA
  OAI --> CA
  AAP --> CA
  CA --> MW --> TH --> RH --> MEM
  CA --> FT
  CA --> HT
  CA --> MT
  RH --> SEQ
  RH --> HO
  RH --> CON
  RH --> SUP
  SEQ --> OT
  HO --> OP
  CON --> OS
  SUP --> OA
```

## Provider Model

| Provider | Execution | Tools Support | Use Case |
|----------|-----------|---------------|----------|
| **AzureOpenAIChatClient** | Client-side | Function Tools, MCP | Direct Azure OpenAI access |
| **OpenAIChatClient** | Client-side | Function Tools, MCP | OpenAI API access |
| **AzureAIAgentsProvider** | Server-side | All (incl. Hosted) | Full Azure AI Agents service |

## Workflow Patterns

```mermaid
graph LR
  subgraph Sequential
    W[Writer] --> R[Reviewer] --> E[Editor] --> P[Publisher]
  end
```

```mermaid
graph LR
  subgraph Handoff
    T[Triage] --> S[Sales]
    T --> Su[Support]
    T --> B[Billing]
    S --> F[Formatter]
    Su --> F
    B --> F
  end
```

```mermaid
graph TB
  subgraph Supervisor
    SP[Supervisor]
    SP --> PL[Planner]
    SP --> CO[Coder]
    SP --> TE[Tester]
    SP --> RE[Reviewer]
  end
```
