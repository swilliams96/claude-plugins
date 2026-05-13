# claude-plugins

Personal Claude Code plugin marketplace by [@swilliams96](https://github.com/swilliams96).

## Adding this marketplace

In Claude Code, run:

```
/plugin add marketplace github:swilliams96/claude-plugins
```

Once added, plugins from this marketplace can be installed individually via the Claude Code plugin manager.

## Plugins

| Plugin | Description |
|--------|-------------|
| [meal-planner](./meal-planner) | Weekly meal planner with ClickUp integration — plans meals, sources recipes, generates shopping lists |

## Structure

Each plugin lives in its own subdirectory following the standard Claude Code plugin layout. The `.claude-plugin/marketplace.json` at the repo root registers this repo as a discoverable marketplace.
