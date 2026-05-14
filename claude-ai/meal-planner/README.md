# Meal Planner — Claude.ai Setup

A Claude.ai Project configuration for the meal planner. Provides the same 6-phase workflow as the Claude Code plugin, using Claude.ai's custom instructions and project knowledge files instead of the plugin/agent system.

## Prerequisites

### ClickUp MCP server

Connect the ClickUp MCP server in Claude.ai via **Settings → Integrations → MCP Servers** and authenticate with your ClickUp account.

The meal planner uses the following ClickUp data (these are personal to the account and are hardcoded in the instructions):

| Item | Value |
|------|-------|
| Workspace ID | `9014840350` |
| Personal space ID | `90143552998` |
| Meal Planning list ID | `901411723029` |

### Web search

Claude.ai needs access to web search for recipe sourcing (Phase 3). This is enabled by default in Claude.ai.

## Setup

### 1. Create a Project

In Claude.ai, create a new Project (e.g. "Meal Planner").

### 2. Add custom instructions

Open the project's **Custom Instructions** and paste the full contents of [`instructions.md`](./instructions.md).

### 3. Upload knowledge files

In the project's **Knowledge** section, upload both files from the `knowledge/` directory:

- [`knowledge/shopping-list.md`](./knowledge/shopping-list.md) — aggregation rules, formatting, and verification checklist for Phase 5
- [`knowledge/recipe-extraction.md`](./knowledge/recipe-extraction.md) — ingredient extraction, unit conversion, and scaling procedure for Phase 5

### 4. Start a conversation

Open a new chat in the project and say something like:

> "Let's plan this week's meals"

The instructions will guide the session through all six phases automatically.

## Differences from the Claude Code plugin

| Feature | Claude Code plugin | Claude.ai project |
|---|---|---|
| Skill auto-triggers | ✅ Automatic | ✅ Via custom instructions |
| Sub-agent dispatch | ✅ recipe-sourcer, recipe-extractor, consolidator | ❌ All logic is inline |
| ClickUp integration | ✅ Via MCP | ✅ Via MCP |
| Web search | ✅ Via web_search tool | ✅ Built into Claude.ai |
| Shopping list saved to ClickUp | ✅ | ✅ |
| Context isolation per phase | ✅ Separate agents | ❌ Single context |

The main practical difference is that without sub-agents, all phases run in a single conversation context. For most sessions this is fine; very long sessions with many recipes may require more careful prompting to stay on track.

## Files

```
claude-ai/meal-planner/
├── README.md               — this file
├── instructions.md         — paste into Project Custom Instructions
└── knowledge/
    ├── shopping-list.md    — upload to Project Knowledge
    └── recipe-extraction.md — upload to Project Knowledge
```
