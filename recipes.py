"""
"What can I cook from my pantry?" matcher.

Uses the guided recipes in recipes_data.py as the source of truth, so a pantry
match links straight to the full step-by-step recipe page.
"""
from recipes_data import RECIPES


def _matches(pantry_name: str, ingredient: str) -> bool:
    a, b = pantry_name.strip().lower(), ingredient.strip().lower()
    return a in b or b in a


def suggest(pantry_names):
    """
    Given pantry item names, return (can_make, almost):
      can_make -> recipes where every ingredient is present
      almost   -> recipes missing only 1-2 ingredients (with `missing` list)
    Each entry keeps id/name/time/category so templates can link to the recipe page.
    """
    pantry_names = [p for p in pantry_names if p]
    can_make, almost = [], []

    for r in RECIPES:
        missing = [ing for ing in r["ingredients"]
                   if not any(_matches(p, ing) for p in pantry_names)]
        card = {"id": r["id"], "name": r["name"], "time": r["time"],
                "category": r["category"], "diet": r["diet"], "spice": r["spice"]}
        if not missing:
            can_make.append(card)
        elif len(missing) <= 2:
            almost.append({**card, "missing": missing})

    almost.sort(key=lambda r: len(r["missing"]))
    return can_make, almost
