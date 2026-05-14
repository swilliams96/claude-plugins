# meal-planner

A Claude Code plugin that acts as a conversational weekly meal planner. It draws on a ClickUp recipe database, searches the web for new ideas, and produces a consolidated, verified shopping list saved back to ClickUp.

## Prerequisites

### ClickUp MCP server

This plugin requires the ClickUp MCP server to be connected and authenticated in Claude Code. Configure it in your `.mcp.json` or Claude Code MCP settings.

The plugin is built around the following ClickUp data:

| Item | Value |
|------|-------|
| Workspace ID | `9014840350` |
| Personal space ID | `90143552998` |
| Meal Planning list ID | `901411723029` |

The Meal Planning list uses these statuses and fields:

- **Statuses:** `options` → `planned` → `cooked`
- **Tags:** `1 - breakfast`, `2 - lunch`, `3 - dinner`
- **Custom fields:** `Recipe link` (URL), `Type of Meal` (dropdown)

The plugin will automatically create a `Meal Planner` folder in your Personal space the first time a shopping list is generated.

## What it does

The meal planner runs through six phases each session:

1. **Last week review** — checks what was planned vs cooked and captures feedback
2. **Context gathering** — number of people, dietary needs, nights to cook, effort level
3. **ClickUp history check** — fetches recent cooked meals and the saved recipe pool to avoid repetition
4. **Slot filling** — works through the week conversationally; can suggest from your saved list, search the web for new ideas, or work with your own suggestions
5. **Plan confirmation** — shows the full week as a table, then syncs to ClickUp on approval
6. **Shopping list generation** — extracts and scales ingredients per recipe, consolidates into a single verified list by grocery section, and saves it as a ClickUp doc

## Components

### Skill

- **`skills/meal-planner/`** — the main orchestrating skill; triggers automatically on meal planning conversations

### Agents

| Agent | Role |
|-------|------|
| `recipe-sourcer` | Searches the web for recipe ideas matching the user's criteria |
| `recipe-extractor` | Fetches a recipe URL (or reads from ClickUp), normalises ingredients to metric, and scales for the number of people |
| `shopping-list-consolidator` | Aggregates all per-recipe ingredient blocks, runs a verification pass, and saves the final list to a ClickUp doc |

## Triggering the skill

The skill triggers automatically on natural phrases like:

- "let's plan this week's meals"
- "what should we eat this week"
- "I need to do a food shop"
- "help me plan dinners"
- "what should I cook tonight"
