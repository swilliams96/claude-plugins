# Shopping List — Reference Guide

This file covers everything needed to generate the final shopping list in Phase 5.

---

## Grocery Store Sections

Categorise every ingredient into one of these sections. When in doubt, use the most logical section for where a UK supermarket (e.g. Sainsbury's, Tesco, Waitrose) would stock it.

### 🥦 Produce
Fresh fruit, vegetables, herbs, salad leaves, mushrooms, garlic, ginger (fresh), chillies (fresh), spring onions, lemons/limes/oranges

### 🥩 Meat & Fish
All fresh and frozen meat (chicken, beef, pork, lamb, turkey, sausages, bacon, chorizo, ham)
All fresh and frozen fish and seafood (salmon, prawns, tuna steak, cod, etc.)
Deli meats if bought from the butcher/fish counter

### 🧀 Dairy & Eggs
Milk, cream (single/double/soured), butter, cheese (all types), yoghurt, crème fraîche, eggs, cream cheese, mascarpone

### 🥫 Tins, Jars & Condiments
Tinned tomatoes, tinned beans/pulses, tinned fish (tuna, sardines), coconut milk, stock (jars/cartons), passata, pesto, tomato purée, soy sauce, fish sauce, sriracha, hot sauce, Worcestershire sauce, mustard, vinegar (all types), honey, maple syrup, miso paste, tahini, harissa, oils (olive oil, sesame oil, vegetable oil), jarred roasted peppers, capers, anchovies

### 🌾 Dried Goods & Pasta
Pasta (all dried), rice, noodles (dried), orzo, gnocchi (shelf-stable), couscous, quinoa, lentils (dried), flour, breadcrumbs, oats, panko, sugar, salt, dried spices and herbs, stock cubes/powder

### 🧴 Fridge & Deli
Fresh pasta, fresh gnocchi, tofu, tempeh, fresh ravioli, tortillas/wraps (fridge), hummus, antipasti, ready-made pastry, fresh soup, fresh pizza dough

### 🍞 Bakery
Bread (all types), rolls, pitta, naan, wraps (ambient), baguettes, tortilla chips, crackers

### 🧃 Drinks & Extras
Wine for cooking, anything else that doesn't fit above

---

## Aggregation Logic

### Step 1: Normalise units
Before combining, convert all quantities to a common base unit within each ingredient type:
- Weights: everything to **grams** (1 oz = 28g, 1 lb = 454g)
- Volumes: everything to **millilitres** (1 cup = 240ml, 1 fl oz = 30ml, 1 tbsp = 15ml, 1 tsp = 5ml)
- Count items (cloves, eggs, tins) stay as counts

### Step 2: Fuzzy match ingredient names
Group ingredients that clearly refer to the same thing:
- "garlic clove" = "cloves of garlic" = "garlic, minced" → "garlic"
- "double cream" ≠ "soured cream" (keep separate)
- "chicken breast" = "chicken breasts, diced" → "chicken breast"
- "tinned tomatoes" = "chopped tomatoes (tin)" → "tinned chopped tomatoes"

Do NOT combine things that are genuinely different (e.g. red onion ≠ white onion, basmati rice ≠ arborio rice).

### Step 3: Sum and re-express
After summing, express in sensible human units:
- Don't write "450ml double cream" — write "450ml double cream (approx. 2 pots)"
- "3 cloves garlic" is fine; "28 cloves garlic" should flag as "1–2 bulbs garlic"
- Round to nearest sensible packaging increment where helpful

### Step 4: Recipe attribution
After each aggregated item, list which recipes use it in brackets:
```
500g chicken breast (Chicken Stroganoff, One Pot Garlic Chicken)
```

---

## Unit Conversion Reference

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

**When to keep imperial:** Never. Always convert. Tbsp and tsp are acceptable to keep as-is for small quantities (spices etc.) since metric equivalents are less intuitive in a kitchen context.

---

## Pantry Staples — Flag but Don't Remove

These items are commonly found in most kitchens. Flag them with a ✓ symbol so the user can quickly scan and skip if they already have them. Do NOT remove them from the list.

**Common pantry staples to flag:**
- Olive oil, vegetable oil, sesame oil
- Salt, black pepper
- Garlic (if under 1 bulb total)
- Soy sauce, Worcestershire sauce
- Dried herbs and spices (unless the recipe requires a specific one in large quantity)
- Sugar (white, brown)
- Plain flour
- Stock cubes (if less than 2)
- Tinned tomatoes (if only 1 tin across the week)
- Butter (if under 50g)
- Eggs (if 1–2 only)

---

## Saving Ingredients Back to ClickUp

After extracting and parsing ingredients from a recipe URL, update the ClickUp task to cache them for future use.

**Call:** `clickup_update_task` with `task_id` and `markdown_description`

**Format to save:**
```markdown
[Recipe Name](https://original-url)

**Serves:** [base serving size from recipe, e.g. 2]
**Cooked for:** [number of people this week, e.g. 2]

## Ingredients
- [quantity in metric] [ingredient name, preparation note]
- ...

## Notes
[any useful notes from the recipe — cook time, tips, substitutions]
```

**Rules:**
1. Base serving size = what the original recipe says it serves (store this accurately)
2. Store ingredients at the **original recipe's serving size**, not scaled — scaling happens at runtime
3. All quantities must be in metric
4. Preparation notes are helpful (e.g. "diced", "finely sliced", "at room temperature") — include where present
5. Only overwrite the description if it currently contains just a URL or is empty. If the description already has a structured `## Ingredients` block, skip the save to avoid overwriting manual edits.

---

## Shopping List Output Format

Present the final shopping list like this:

```
🛒 Shopping List — Week of [date]

🥩 Meat & Fish
• 500g chicken breast (Tuscan Sausage Gnocchi, One Pot Garlic Chicken)
• 200g raw king prawns (Creamy Peanut & Prawn Noodles)
• 300g Italian sausages (Tuscan Sausage Gnocchi) ← batch cook ×2

🥦 Produce
• 2 red onions (Tuscan Sausage Gnocchi, Chorizo Gnocchi)
• 1 lemon (Salmon Poke Bowl)
• 200g cherry tomatoes (Baked Feta Orzo)
• ✓ garlic, 4 cloves (multiple recipes)

🧀 Dairy & Eggs
• 100ml double cream (Tuscan Sausage Gnocchi)
• ✓ butter, ~30g (Salmon Poke Bowl)

🌾 Dried Goods & Pasta
• 400g gnocchi (Chorizo Gnocchi)
• 250g orzo (Baked Feta Orzo)
• ✓ soy sauce (Salmon Poke Bowl)

🥫 Tins, Jars & Condiments
• 1 tin (400g) chopped tomatoes (Tuscan Sausage Gnocchi)
• 2 tbsp peanut butter (Creamy Peanut & Prawn Noodles)

🍞 Bakery
[nothing this week]

✓ = likely already in your pantry — check before buying
```

---

## Ambiguous Quantities — Flag with ❓

If an ingredient quantity cannot be expressed as a specific number with a unit, do **not** guess. Flag it instead:

| Vague phrasing | How to handle |
|---|---|
| "a handful" | ❓ handful [ingredient] — quantity unclear |
| "to taste" | ✓ [ingredient] (to taste) — treat as pantry staple |
| "a pinch" | ✓ [ingredient] (pinch) — treat as pantry staple |
| "some X" | ❓ [ingredient] — quantity not specified |
| "optional" | Include but mark as *(optional)* |
| No quantity given | ❓ [ingredient] — no quantity in recipe |

Present flagged items at the bottom in a dedicated section:

```
❓ Items to double-check (quantities were unclear in the recipe):
• chilli flakes — Tuscan Sausage Gnocchi (recipe said "a pinch", adjust to taste)
• fresh parsley — Salmon Poke Bowl (no quantity given)
```

---

## Verification Checklist (Step 3 of Phase 5)

After consolidating the list, run this check before presenting to the user. Do not skip this.

**Check 1 — Every item has a source recipe**
For each line in the final list, confirm it appears in one of the per-recipe blocks. If you find an item you cannot trace to a recipe, remove it silently.

**Check 2 — Every recipe is represented**
For each meal in the week's plan, at least one ingredient must be attributed to it. If a recipe has zero items:
> ⚠️ No ingredients found for [Recipe Name] — you may want to check this one manually.

**Check 3 — Quantities are plausible**
Scan for obvious scaling errors. Flag anything that looks wrong:
> ⚠️ Double-check: 28 cloves garlic (Tuscan Sausage Gnocchi) — this may be a scaling issue.

---

## Batch Cook Scaling

When a meal is flagged as a batch cook:
- `scale_factor` tells you how many times the recipe needs to be made (e.g. `2` = double up)
- Multiply all ingredient quantities by `(people_cooking_for / base_servings) × scale_factor`
- Mark batch cook items with `← batch cook ×N` on the shopping list

Example:
- Recipe base: serves 2
- Cooking for: 2 people
- Batch cook scale factor: 2
- Multiplier: (2/2) × 2 = **2×** all quantities
