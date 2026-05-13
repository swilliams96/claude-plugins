---
name: meal-planner
description: >
  Weekly meal planner with ClickUp integration, shopping list generation, and recipe ideation.
  Trigger this skill whenever the user mentions meal planning, planning meals for the week, deciding what
  to cook, figuring out dinners, making a shopping list, or anything related to food planning or grocery
  shopping. Also trigger when the user asks for recipe ideas, says they're stuck on what to cook, or wants
  to review their meal plan database. Even casual phrasing like "what should we eat this week", "I need to
  do a food shop", or "help me plan dinners" should trigger this skill immediately — do not wait for explicit
  confirmation before reading this file.
---

# Meal Planner Skill

**CRITICAL — Follow each phase in the exact order below. Do not skip phases. Do not combine steps from different phases. Do not proceed to the next phase without fully completing the current one. Use the specified agents at the points described — do not attempt to perform agent tasks inline.**

A conversational, multi-phase skill for planning the week's meals, drawing on a ClickUp recipe database, web searches for new ideas, and generating a structured grocery shopping list at the end.

## Prerequisites

- **ClickUp MCP server** must be connected and authenticated (workspace: `9014840350`, list ID: `901411723029`)
- **`web_search` and `web_fetch`** tools must be available (used by the `recipe-sourcer` and `recipe-extractor` agents)

**Quick-reference — ClickUp data model:**
- Workspace ID: `9014840350`
- Personal space ID: `90143552998`
- Meal Planning list ID: `901411723029`
- Statuses: `options` → `planned` → `cooked`
- Tags: `1 - breakfast`, `2 - lunch`, `3 - dinner`
- Custom fields:
  - `Recipe link` (ID: `235eab14-7375-408d-9626-e6b1bec9b3d9`) — URL field
  - `Type of Meal` (ID: `5301f733-c5f7-45ba-a238-af08f5cfe67d`) — dropdown: Breakfast / Lunch / Dinner / Snacks

---

## Phase 0 — Last Week Review

Before anything else, check what was planned for last week and whether it got cooked.

**Steps:**
1. Call `clickup_filter_tasks` with `list_ids: ["901411723029"]`, `statuses: ["planned"]`, `include_closed: false`, `order_by: "due_date"`, `reverse: false`
2. Also call with `statuses: ["cooked"]`, `include_closed: true`, filtering to tasks with a `due_date` in the last 7 days
3. Identify any meals that were **planned but not yet marked as cooked** — these are the ones to review

**If there are unreviewed planned meals:**

Present them warmly in a single message. Example:

> "Before we plan this week — last week you had:
> - Monday: Tuscan Sausage Gnocchi
> - Wednesday: Salmon Poke Bowl
>
> Did you end up making these? And how did they go — any you particularly loved or wouldn't rush to repeat?"

For each meal based on the user's response:

- **Cooked it:** call `clickup_update_task` — set `status: "cooked"` and `due_date` to when it was cooked
- **Skipped it:** leave status as-is (or ask if they want to carry it to this week)
- **Preference feedback:** append a `## Preferences` section to the task description:

```markdown
## Preferences
- ⭐ Loved it — would happily repeat (noted [date])
- 🔁 Good but tweak: [note]
- ❌ Wouldn't repeat — [reason]
```

These notes feed Phase 2 and 3: ❌ meals are excluded from suggestions; ⭐ meals are weighted higher.

**If no planned meals from last week**, skip this phase silently and go to Phase 1.

---

## Phase 1 — Context Gathering

Ask the user the following **in a single, friendly conversational message** (not a bulleted interrogation):

1. **How many people** are you cooking for this week?
2. **Any dietary requirements or things to avoid?** (intolerances, preferences, budget week, etc.)
3. **How many nights do you want to cook?** (default: 5 weeknights Mon–Fri)
4. **Any batch cooks planned?** (make extra one night to cover the next) — or suggest one if a slot naturally suits it
5. **Anything in the fridge/freezer that needs using up?**
6. **Effort level?** (quick & easy / normal / a weekend project or two)

Do NOT proceed to Phase 2 until you have answers to at least (1), (3), and (4). The rest can be defaulted if not provided.

---

## Phase 2 — ClickUp History Check

Fetch recent history before suggesting anything.

**Steps:**
1. Call `clickup_filter_tasks` with `list_ids: ["901411723029"]`, `statuses: ["cooked"]`, `include_closed: true`, `order_by: "due_date"`, `reverse: true`, `page: 0`
2. Extract the last ~6–8 meals cooked (by due_date). Note names and approximate dates.
3. Also call with `statuses: ["options"]` — this is the saved recipe pool.
4. Keep both lists in memory for Phase 3.

**Rules:**
- Avoid suggesting anything cooked in the last 2 weeks
- Prefer `options` recipes that haven't appeared recently
- Frequently cooked meals are known favourites — weight them higher
- Check `## Preferences` blocks: ❌ = exclude; ⭐ = weight higher; 🔁 = include with the tweak note

---

## Phase 3 — Slot Filling (Conversational)

Work through meal slots one or a few at a time. Default: **Monday–Friday dinners**. Add Sat/Sun if requested.

### If the user has their own ideas:
- Confirm/validate (note if cooked recently)
- Fetch ClickUp details if the recipe exists there
- Offer to add new recipes to ClickUp

### If the user wants suggestions from their saved list:
- Propose 2–3 options from the `options` pool, excluding recent meals
- Include: name, brief description, one-line reason it fits

### If the user wants new ideas or is stuck:
1. Ask 1–2 targeted narrowing questions (cuisine, effort, protein type, etc.)
2. **Dispatch the `meal-planner:recipe-sourcer` agent** with:
   - User criteria from the narrowing questions
   - Dietary restrictions from Phase 1
   - Meals to avoid from Phase 2 history
3. Present the agent's 2–3 returned options for the user to pick from

### Batch cook handling:
- Mark the following day as **"← Leftovers from [meal]"** — no separate recipe needed
- Internally record: `batch_cook: true`, `leftovers_day: [day]`, `scale_factor: [n]`

### Track each slot as:
```
{
  day: "Monday",
  meal_name: "Tuscan Sausage Gnocchi",
  clickup_task_id: "86b64271b",  // null if new
  recipe_url: "https://...",      // if available
  is_batch_cook: true,
  leftovers_day: "Tuesday",
  scale_factor: 2,
  servings_base: 2,
  source: "clickup" | "web" | "user"
}
```

---

## Phase 4 — Plan Confirmation & ClickUp Sync

Display the full week plan as a clear table:

```
Day        | Meal                            | Notes
-----------|---------------------------------|-----------------------
Monday     | Tuscan Sausage Gnocchi          | Batch cook (×2)
Tuesday    | ← Leftovers                     |
Wednesday  | Salmon Poke Bowl                |
Thursday   | Creamy Peanut & Prawn Noodles   |
Friday     | Chorizo Gnocchi                 |
```

Ask: *"Happy with this? Any changes before I save it and build the shopping list?"*

**On confirmation**, sync to ClickUp:
1. For meals with a `clickup_task_id`: call `clickup_update_task` — set `status: "planned"`, `due_date` to the assigned day
2. For new recipes: call `clickup_create_task` with:
   - `name`: recipe name
   - `status`: `"planned"`
   - `due_date`: assigned day
   - `tags`: `["3 - dinner"]` (or appropriate tag)
   - `custom_fields`: `Type of Meal` and `Recipe link` if available
   - `markdown_description`: recipe URL + any notes
3. For batch cooks: append `[Leftovers: {day}]` to the description

---

## Phase 5 — Shopping List Generation

**CRITICAL: Do not attempt to generate the consolidated shopping list until ALL per-recipe extractions are complete. Follow these steps in exact order.**

See `references/shopping-list.md` for full formatting rules, aggregation logic, categorisation, and verification checklist.

### Step 1: Extract ingredients per recipe (one at a time, sequentially)

For **each non-leftover meal** in the confirmed plan:

**Dispatch the `meal-planner:recipe-extractor` agent** with:
- `task_id`: ClickUp task ID (or null if new)
- `recipe_url`: recipe URL (if available)
- `meal_name`: name of the meal
- `people_cooking_for`: from Phase 1
- `scale_factor`: batch cook multiplier (1 if not a batch cook)

**Wait for each extraction to complete before dispatching the next.** Collect all returned per-recipe ingredient blocks.

### Step 2 & 3: Consolidate, verify, and save to ClickUp

Once all per-recipe blocks are in hand:

**Dispatch the `meal-planner:shopping-list-consolidator` agent** with:
- All per-recipe ingredient blocks from Step 1
- Full meal plan (day, meal name, batch cook notes)
- `week_label`: the date range for the week, e.g. "19–23 May 2025"
- `people_cooking_for`: from Phase 1

The agent will consolidate all ingredients, run the verification pass, create or find a "Meal Planner" folder in the Personal ClickUp space, create a shopping list doc, and return the formatted list plus the ClickUp doc URL.

**Present the final shopping list to the user**, then:
> "I've also saved your shopping list to ClickUp: [link]"

---

## Key Behaviours

- **Be conversational, not form-like.** Chat naturally; avoid presenting everything as numbered lists.
- **Check ClickUp first.** Always look in the saved recipe pool before going to web search.
- **Don't repeat recent meals.** Cross-reference cooked history on every suggestion.
- **Always confirm before writing to ClickUp.** Never sync without explicit user approval of the plan.
- **Handle partial data gracefully.** If a URL fails to load, tell the user and ask for ingredients manually.
- **Pantry staples.** Flag items the user likely already has with ✓ in the shopping list.

---

## Reference Files

- **`references/shopping-list.md`** — Grocery section categories, aggregation logic, unit conversions, pantry staples, verification checklist, and output format
