# Shopping List — Reference Guide

Covers aggregation, formatting, verification, and output format for Phase 5.

---

## Grocery Store Sections

Categorise every ingredient into one of these sections. When in doubt, use the most logical section for where a UK supermarket (e.g. Sainsbury's, Tesco, Waitrose) would stock it.

### 🥦 Produce
Fresh fruit, vegetables, herbs, salad leaves, mushrooms, garlic, ginger (fresh), chillies (fresh), spring onions, lemons/limes/oranges

### 🥩 Meat & Fish
All fresh and frozen meat (chicken, beef, pork, lamb, turkey, sausages, bacon, chorizo, ham)
All fresh and frozen fish and seafood (salmon, prawns, tuna steak, cod, etc.)

### 🧀 Dairy & Eggs
Milk, cream (single/double/soured), butter, cheese (all types), yoghurt, crème fraîche, eggs, cream cheese, mascarpone

### 🥫 Tins, Jars & Condiments
Tinned tomatoes, tinned beans/pulses, tinned fish, coconut milk, stock, passata, pesto, tomato purée, soy sauce, fish sauce, sriracha, hot sauce, Worcestershire sauce, mustard, vinegar, honey, maple syrup, miso paste, tahini, harissa, oils, jarred peppers, capers, anchovies

### 🌾 Dried Goods & Pasta
Pasta (dried), rice, noodles (dried), orzo, gnocchi (shelf-stable), couscous, quinoa, lentils, flour, breadcrumbs, oats, panko, sugar, salt, dried spices and herbs, stock cubes

### 🧴 Fridge & Deli
Fresh pasta, fresh gnocchi, tofu, tempeh, tortillas/wraps (fridge), hummus, antipasti, ready-made pastry, fresh pizza dough

### 🍞 Bakery
Bread, rolls, pitta, naan, wraps (ambient), baguettes, tortilla chips, crackers

### 🧃 Drinks & Extras
Wine for cooking, anything else that doesn't fit above

---

## Aggregation Logic

### Step 1: Normalise units
- Weights → **grams** (1 oz = 28g, 1 lb = 454g)
- Volumes → **millilitres** (1 cup = 240ml, 1 fl oz = 30ml, 1 tbsp = 15ml, 1 tsp = 5ml)
- Count items (cloves, eggs, tins) stay as counts
- Tbsp/tsp acceptable to keep for small spice quantities

### Step 2: Fuzzy match ingredient names
Group variants of the same ingredient:
- "garlic clove" = "cloves of garlic" = "garlic, minced" → "garlic"
- "chicken breast" = "chicken breasts, diced" → "chicken breast"
- "tinned tomatoes" = "chopped tomatoes (tin)" → "tinned chopped tomatoes"

Do NOT combine genuinely different things (red onion ≠ white onion, basmati ≠ arborio, double cream ≠ soured cream).

### Step 3: Sum and re-express
- "450ml double cream" → "450ml double cream (approx. 2 pots)"
- "28 cloves garlic" → "1–2 bulbs garlic"
- Round to nearest sensible packaging increment

### Step 4: Recipe attribution
```
500g chicken breast (Tuscan Sausage Gnocchi, One Pot Garlic Chicken)
```

---

## Pantry Staples — Flag with ✓, Don't Remove

Flag these with ✓ so the user can skip if they already have them:
- Olive oil, vegetable oil, sesame oil
- Salt, black pepper
- Garlic (if under 1 bulb total)
- Soy sauce, Worcestershire sauce
- Dried herbs and spices (unless large quantity needed)
- Sugar, plain flour
- Stock cubes (if fewer than 2)
- Tinned tomatoes (if only 1 tin across the week)
- Butter (if under 50g), eggs (if 1–2 only)

---

## Ambiguous Quantities — Flag with ❓

| Vague phrasing | How to handle |
|---|---|
| "a handful" | ❓ handful [ingredient] — quantity unclear |
| "to taste" | ✓ [ingredient] (to taste) |
| "a pinch" | ✓ [ingredient] (pinch) |
| "some X" | ❓ [ingredient] — quantity not specified |
| "optional" | Include, mark *(optional)* |
| No quantity given | ❓ [ingredient] — no quantity in recipe |

Present flagged items in a dedicated section at the bottom:
```
❓ Items to double-check:
• chilli flakes — Tuscan Sausage Gnocchi (recipe said "a pinch")
• fresh parsley — Salmon Poke Bowl (no quantity given)
```

---

## Output Format

```
🛒 Shopping List — [date range]
Cooking for [N] people

🥩 Meat & Fish
• 500g chicken breast (Tuscan Sausage Gnocchi, One Pot Garlic Chicken)
• 300g Italian sausages (Tuscan Sausage Gnocchi) ← batch cook ×2

🥦 Produce
• 2 red onions (Tuscan Sausage Gnocchi, Chorizo Gnocchi)
• ✓ garlic, 4 cloves (multiple recipes)

[continue for each section with items; omit empty sections]

✓ = likely already in your pantry — check before buying

❓ Items to double-check:
• [ingredient] — [recipe] ([reason])
```

Include ⚠️ verification warnings after the list if any checks failed.

---

## Verification Checklist

Run all three checks before presenting. Do not skip.

**Check 1 — Every item has a source recipe**
Each line must trace to at least one per-recipe block. Remove any untraceable item silently.

**Check 2 — Every recipe is represented**
Each non-leftover meal must have at least one attributed item. If zero:
> ⚠️ No ingredients found for [Recipe Name] — please check manually.

**Check 3 — Quantities are plausible**
Flag obvious scaling errors:
> ⚠️ Double-check: 28 cloves garlic (Tuscan Sausage Gnocchi) — may be a scaling error.

---

## Batch Cook Scaling

```
scaled_qty = base_qty × (people_cooking_for / base_servings) × scale_factor
```

Mark batch cook items with `← batch cook ×N` on the shopping list.
