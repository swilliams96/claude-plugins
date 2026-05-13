# Recipe Extraction — Reference

Follow this procedure for each meal during Phase 5 Step 1. Complete one meal fully before starting the next.

## Step 1: Get the ingredients

**If a ClickUp task ID is available:**
1. Call `clickup_get_task` with the task ID
2. If the description contains a `## Ingredients` block — parse it directly, skip the URL fetch
3. If the description is empty or contains only a URL — fetch the URL instead

**If fetching from a URL:**
- Call `web_fetch` on the recipe URL
- Extract: base serving size, every ingredient with quantity, unit, and preparation notes

**No-hallucination rule:** Only include ingredients explicitly listed in the source. Do not infer or add ingredients that "would normally be in this dish." If unsure, leave it out and flag with ❓.

## Step 2: Convert to metric

| Imperial | Metric |
|----------|--------|
| 1 oz | 28g |
| 1 lb | 454g |
| 1 fl oz | 30ml |
| 1 cup | 240ml |
| ½ cup | 120ml |
| ¼ cup | 60ml |
| 1 tbsp | 15ml |
| 1 tsp | 5ml |

Tbsp and tsp are acceptable to keep as-is for small spice quantities.

## Step 3: Scale quantities

```
scaled_qty = base_qty × (people_cooking_for / base_servings) × scale_factor
```

Round to sensible precision (e.g. 83g → 85g; 0.67 tsp → ¾ tsp).

Use ❓ to flag any ingredient where:
- Quantity is vague ("a handful", "some", "to taste", "a pinch")
- Unit is ambiguous or non-standard
- A judgement call was made

## Step 4: Save back to ClickUp (if task ID provided)

If the task description did NOT already have a `## Ingredients` block, silently save the extracted data back with `clickup_update_task`:

```markdown
[Recipe Name](https://original-url)

**Serves:** [base serving size]
**Cooked for:** [people_cooking_for] people (adjust as needed)

## Ingredients
- [base quantity in metric] [ingredient name, preparation note]
- ...

## Notes
[any useful cooking notes or tips]
```

Store at the **original base serving size** — not scaled. Only save if the description currently lacks a `## Ingredients` block.

## Output format

```
📋 [Meal Name] — per-recipe ingredient list
Serves (base): [N] | Cooking for: [N] | Scale factor: ×[N]
Source: [clickup | web_fetch from URL]

| Ingredient | Base qty | Scaled qty | Unit | Notes |
|---|---|---|---|---|
| chicken breast | 300g | 600g | g | diced |
| garlic | 2 cloves | 4 cloves | cloves | minced |
| chilli flakes | 1 tsp | 2 tsp | tsp | ❓ recipe said "a pinch" |
```

If the page fails to load or yields no parseable ingredients:

```
❌ [Meal Name] — extraction failed
Reason: [URL returned 404 / no readable recipe content / etc.]
Action needed: Please provide the ingredient list manually.
```
