# claude-plugins

Personal Claude Code plugin marketplace by [@swilliams96](https://github.com/swilliams96).

## Adding this marketplace

In Claude Code, run:

```
/plugin add marketplace github:swilliams96/claude-plugins
```

Once added, plugins from this marketplace can be installed individually via the Claude Code plugin manager.

## Plugins

Each plugin has two versions: a **Claude Code** plugin (with skills, agents, and MCP integration) and a **Claude.ai** project configuration (custom instructions and knowledge files for use in Claude.ai Projects).

| Plugin | Description | Claude Code | Claude.ai |
|--------|-------------|-------------|-----------|
| meal-planner | Weekly meal planner with ClickUp integration — plans meals, sources recipes, generates shopping lists | [claude-code/meal-planner](./claude-code/meal-planner) | [claude-ai/meal-planner](./claude-ai/meal-planner) |

## Structure

```
claude-code/        — Claude Code plugins (skills, agents, MCP)
└── meal-planner/

claude-ai/          — Claude.ai project configurations (custom instructions + knowledge files)
└── meal-planner/
```

The `.claude-plugin/marketplace.json` at the repo root registers this repo as a discoverable Claude Code marketplace.
